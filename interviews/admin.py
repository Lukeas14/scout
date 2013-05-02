from .models import SocialProfile, Interview, Video
from django.contrib import admin
from django.contrib.sites.models import Site

admin.site.unregister(Site)

admin.site.register(SocialProfile)
admin.site.register(Interview)
admin.site.register(Video)