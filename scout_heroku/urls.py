from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'interviews.views.home'),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	url(r'^createvid/(?P<username>[\w-]+)/$', 'connections.views.createvid'),
	url(r'^allset/(?P<interview_uuid>\w+)/$', 'connections.views.allset'),
	url(r'^(?P<identifier>[\w-]+)/$', 'connections.views.interview'),
	url(r'^respond/(?P<username>[\w-]+)/$', 'connections.views.interview_respond'),
	url(r'^response/(?P<username>[\w-]+)/$', 'connections.views.interview_response'),
	url(r'^validate/interview_respond', 'connections.views.validate_interview_respond')
)
