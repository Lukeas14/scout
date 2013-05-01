from django.db import models
from django.conf import settings


def create_uuid():
	import uuid
	return uuid.uuid1().hex[:12]

class Interview(models.Model):
	interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='interviewers')
	interviewee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interviewees')
	uuid = models.CharField(unique=True, default=create_uuid, max_length=255)
	time_added = models.DateTimeField(auto_now_add=True)
	time_modified = models.DateTimeField(auto_now=True)