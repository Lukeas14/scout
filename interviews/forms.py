from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from django.forms.formsets import BaseFormSet
from django.contrib.auth import get_user_model

import re

class UserForm(forms.Form):
	name = forms.CharField(max_length=50, label='', error_messages={'required': 'Please enter your name.'})
	email = forms.EmailField(label='', error_messages={'required': 'Please enter your e-email address.'})

	def create_user(self):
		username = self.unique_slugify(get_user_model(), self.cleaned_data['name'], 'username')
		self.user = User.objects.create_user(username, self.cleaned_data['email'], settings.DEFAULT_PASSWORD)
		self.user.first_name = " ".join(self.cleaned_data['name'].split(' ')[:-1])
		self.user.last_name = " ".join(self.cleaned_data['name'].split(' ')[-1:])
		self.user.save()

		return self.user

	def unique_slugify(self, instance, value, slug_field_name='slug', queryset=None, slug_separator='-'):
		"""
		Calculates and stores a unique slug of ``value`` for an instance.

		``slug_field_name`` should be a string matching the name of the field to
		store the slug in (and the field to check against for uniqueness).

		``queryset`` usually doesn't need to be explicitly provided - it'll default
		to using the ``.all()`` queryset from the model's default manager.
		"""
		slug_len = instance._meta.get_field(slug_field_name).max_length

		# Sort out the initial slug, limiting its length if necessary.
		slug = slugify(value)
		if slug_len:
			slug = slug[:slug_len]
		slug = self._slug_strip(slug, slug_separator)
		original_slug = slug

		# Create the queryset if one wasn't explicitly provided and exclude the
		# current instance from the queryset.
		if queryset is None:
			queryset = instance.objects.all()

		# Find a unique slug. If one matches, at '-2' to the end and try again
		# (then '-3', etc).
		next = 2
		while not slug or queryset.filter(**{slug_field_name: slug}):
			slug = original_slug
			end = '%s%s' % (slug_separator, next)
			if slug_len and len(slug) + len(end) > slug_len:
				slug = slug[:slug_len-len(end)]
				slug = _slug_strip(slug, slug_separator)
			slug = '%s%s' % (slug, end)
			next += 1

		return slug


	def _slug_strip(self, value, separator='-'):
		"""
		Cleans up a slug by removing slug separator characters that occur at the
		beginning or end of a slug.

		If an alternate separator is used, it will also replace any instances of
		the default '-' separator with the new separator.
		"""
		separator = separator or ''
		if separator == '-' or not separator:
			re_sep = '-'
		else:
			re_sep = '(?:-|%s)' % re.escape(separator)
		# Remove multiple instances and if an alternate separator is provided,
		# replace the default '-' separator.
		if separator != re_sep:
			value = re.sub('%s+' % re_sep, separator, value)
		# Remove separator from the beginning and end of the slug.
		if separator:
			if separator != '-':
				re_sep = re.escape(separator)
			value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
		return value
   

class VideoForm(forms.Form):

	def clean(self):
		if not self.data["scout_video[video_uuid]"]:
			raise forms.ValidationError("Please record a video (Don't forget to click \"Accept\" at the end).")

class RespondForm(forms.Form):
	name = forms.CharField(max_length=50, label='Your Name')
	email = forms.EmailField(label='E-mail Address')

class SocialProfileForm(forms.Form):
	profile_url = forms.URLField(required=False, max_length=255, label='')

class BaseSocialProfileFormset(BaseFormSet):
	def clean(self):
		if any(self.errors):
			return
		
		profiles = []
		for form in self.forms:
			try:
				profile = form.cleaned_data['profile_url']
			except KeyError:
				continue

			if not profile:
				continue

			if profile in profiles:
				raise forms.ValidationError("Please remove all duplicate social profiles.")

			profiles.append(profile)

		if len(profiles) < settings.SOCIAL_PROFILES_REQUIRED:
			raise forms.ValidationError("Please enter at least %s social profiles." % (settings.SOCIAL_PROFILES_REQUIRED,))
