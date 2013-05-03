from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.defaults import page_not_found
from django.forms.formsets import formset_factory
from django import forms
from django.conf import settings
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context

from .models import SocialProfile, Interview, Video
from .forms import UserForm, RespondForm, SocialProfileForm, BaseSocialProfileFormset, VideoForm

def home(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		user_form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Your Name'})
		user_form.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'E-mail Address'})

		if user_form.is_valid():
			user = user_form.create_user()

			return redirect("/createvid/" + user_form.user.get_username() + "/")
	else:
		user_form = UserForm()
		user_form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Your Name'})
		user_form.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'E-mail Address'})

	return render(request, 'home.html', {'user_form': user_form})

def createvid(request, username):
	user = get_user_model().objects.get(username=username)
	error = ''

	if request.method == 'POST':
		video_form = VideoForm(request.POST)

		if video_form.is_valid():
			interview = Interview.objects.create(
				interviewer = user
			)

			video = Video.objects.create(
				interview = interview,
				user = user,
				uuid = request.POST['scout_video[video_uuid]'],
				thumb_url = request.POST['scout_video[qvga][thumb]'],
				small_thumb_url = request.POST['scout_video[qvga][small_thumb]'],
				video_url = request.POST['scout_video[qvga][video]']
			)

			send_mail(
				'Welcome to Scout',
				get_template('emails/welcome.txt').render(Context({'user': user, 'interview': interview, 'host': request.get_host()})),
				"Scout <%s>" % (settings.EMAIL_WEBMASTER),
				[user.email],
				fail_silently=True
			)

			return render(request, 'allset.html', {
				'interview': interview,
				'host': request.get_host()
			})

	else:
		video_form = VideoForm()

	return render(request, 'createvid.html', {
		'user': user,
		'error': error,
		'video_form': video_form,
		'camera_name': settings.CAMERA_NAME,
		'camera_uuid': settings.CAMERA_UUID
	})

def interview(request, identifier):
	try:
		#Public interview page
		user = get_user_model().objects.get(username=identifier)
		interview = Interview.objects.filter(interviewer=user)[:1][0]
		interview_video = interview.video_set.get(user=user)
	
		if not interview:	
			raise Http404

		return render(request, 'interview_public.html', {'user': user, 'interview': interview, 'interview_video': interview_video})

	except get_user_model().DoesNotExist:
		#Private interview page
		try:
			interview = Interview.objects.get(uuid=identifier)
			interviewer_video = interview.video_set.get(user=interview.interviewer)
			responses = interview.interviewee.order_by('-date_joined')

			if request.method == "POST":
				user_form = UserForm(request.POST)

				if user_form.is_valid():
					user = user_form.save_user(interview.interviewer)

					return redirect("/" + interview.uuid + "/")

			else:
				user_form = UserForm(initial={
					'name': interview.interviewer.get_full_name(),
					'email': interview.interviewer.email
				})

			user_form.fields['name'].label = "Your Name"
			user_form.fields['email'].label = "E-mail Address"
			
			return render(request, 'interview_private.html', {
				'interview': interview,
				'interviewer_video': interviewer_video,
				'responses': responses,
				'user_form': user_form,
				'host': request.get_host()
			})

		except Interview.DoesNotExist:
			raise Http404

def interview_respond(request, username):
	interviewer = get_object_or_404(get_user_model(), username=username)
	interview = Interview.objects.get(interviewer=interviewer)

	SocialProfileFormset = formset_factory(SocialProfileForm, extra=2, max_num=7, formset=BaseSocialProfileFormset)
	
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		user_form.fields['name'].label = "Your Name"
		user_form.fields['email'].label = "E-mail Address"
		socialprofile_formset = SocialProfileFormset(request.POST, request.FILES, prefix='respond')
		video_form = VideoForm(request.POST)

		if user_form.is_valid() and socialprofile_formset.is_valid() and video_form.is_valid():
			user = user_form.create_user()

			for socialprofile_form in socialprofile_formset.forms:
				try:
					socialprofile_form.cleaned_data['profile_url']
				except KeyError:
					continue

				social_profile = SocialProfile(
					user = user,
					url = socialprofile_form.cleaned_data['profile_url']
				)
				social_profile.site = social_profile.get_site_from_url(social_profile.url)
				social_profile.save()

			interview.interviewee.add(user)

			video = Video.objects.create(
				interview = interview,
				user = user,
				uuid = request.POST['scout_video[video_uuid]'],
				thumb_url = request.POST['scout_video[qvga][thumb]'],
				small_thumb_url = request.POST['scout_video[qvga][small_thumb]'],
				video_url = request.POST['scout_video[qvga][video]']
			)

			#Send email to interviewer
			send_mail(
				'New Interview Response on Scout',
				get_template('emails/new_response.txt').render(Context({'user': user, 'interviewer': interviewer, 'interview': interview, 'host': request.get_host()})),
				"Scout <%s>" % (settings.EMAIL_WEBMASTER),
				[interviewer.email],
				fail_silently=True
			)

			#Send email to interviewee
			send_mail(
				'Thanks for Your Response on Scout',
				get_template('emails/response_thank_you.txt').render(Context({'user': user, 'interviewer': interviewer, 'interview': interview, 'host': request.get_host()})),
				"Scout <%s>" % (settings.EMAIL_WEBMASTER),
				[user.email],
				fail_silently=True
			)

			return render(request, 'thankyou.html', {
				'interviewer': interviewer,
				'interview': interview
			})

	else:
		user_form = UserForm()
		user_form.fields['name'].label = "Your Name"
		user_form.fields['email'].label = "E-mail Address"
		socialprofile_formset = SocialProfileFormset(prefix='respond')
		video_form = VideoForm()

	return render(request, 'interview_respond.html', {
		'interviewer': interviewer,
		'interview': interview,
		'user_form': user_form,
		'socialprofile_formset': socialprofile_formset,
		'video_form': video_form,
		'camera_name': settings.CAMERA_NAME,
		'camera_uuid': settings.CAMERA_UUID
	})

def validate_interview_respond(request):
	response = {
		'status': 'failed'
	}

	if request.method == 'POST':
		SocialProfileFormset = formset_factory(SocialProfileForm, extra=2, max_num=7, formset=BaseSocialProfileFormset)
		user_form = UserForm(request.POST)
		socialprofile_formset = SocialProfileFormset(request.POST, request.FILES, prefix='respond')
		video_form = VideoForm(request.POST)

		if user_form.is_valid() and socialprofile_formset.is_valid() and video_form.is_valid():
			response['status'] = 'success'

		response['user_form'] = user_form.errors
		response['socialprofile_formset'] = socialprofile_formset.errors
		response['socialprofile_formset_nonform'] = socialprofile_formset.non_form_errors()
		response['video_form'] = video_form.errors

		return HttpResponse(simplejson.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")
	else:
		raise Http404

def interview_response(request, username):
	interviewee = get_object_or_404(get_user_model(), username=username)
	interview = Interview.objects.get(interviewee=interviewee)
	interview_video = interview.video_set.get(user=interviewee)

	return render(request, 'interview_response.html', {
		'interviewee': interviewee,
		'interview': interview,
		'interview_video': interview_video
	})