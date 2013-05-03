from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'interviews.views.home'),
	url(r'^admin/', include(admin.site.urls)),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	url(r'^createvid/(?P<username>[\w-]+)/$', 'interviews.views.createvid'),
	url(r'^(?P<identifier>[\w-]+)/$', 'interviews.views.interview'),
	url(r'^respond/(?P<username>[\w-]+)/$', 'interviews.views.interview_respond'),
	url(r'^response/(?P<username>[\w-]+)/$', 'interviews.views.interview_response'),
	url(r'^validate/interview_respond', 'interviews.views.validate_interview_respond')
)
