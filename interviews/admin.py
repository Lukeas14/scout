from .models import SocialProfile, Interview, Video
from django.contrib import admin
from django.contrib.sites.models import Site

class InterviewAdmin(admin.ModelAdmin):
	date_hierarchy = 'time_added'
	list_display = ('interviewer', 'time_added')
	filter_horizontal = ('interviewee',)

class SocialProfileAdmin(admin.ModelAdmin):
	date_hierarchy = 'time_added'
	list_display = ('user', 'site', 'url', 'time_added')

class VideoAdmin(admin.ModelAdmin):
	date_hierarchy = 'time_added'
	list_display = ('user', 'interview', 'time_added')

admin.site.register(SocialProfile, SocialProfileAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Video, VideoAdmin)

admin.site.unregister(Site)