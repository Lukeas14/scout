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

def home(request):

	return render(request, 'home.html', {})