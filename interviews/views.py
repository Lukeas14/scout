from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.defaults import page_not_found
from django.forms.formsets import formset_factory
from django import forms
from django.conf import settings
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, Http404

from .models import SocialProfile, Interview, Video
from .forms import UserForm, RespondForm, SocialProfileForm, BaseSocialProfileFormset, VideoForm

def home(request):
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		user_form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Your Name'})
		user_form.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'E-mail Address'})

		if user_form.is_valid():
			user_form.create_user()

			return redirect("/createvid/" + user_form.user.get_username() + "/")
	else:
		user_form = UserForm()
		user_form.fields['name'].widget = forms.TextInput(attrs={'placeholder': 'Your Name'})
		user_form.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'E-mail Address'})

	return render(request, 'home.html', {'user_form': user_form})
