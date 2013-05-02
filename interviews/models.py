from django.db import models
from django.conf import settings


def create_uuid():
	import uuid
	return uuid.uuid1().hex[:12]

class SocialProfile(models.Model):
	OTHER = 1
	FACEBOOK = 2
	TWITTER = 3
	LINKEDIN = 4
	AIRBNB = 5
	GOOGLEPLUS = 6
	EBAY = 7
	SITE_CHOICES = (
		(OTHER, 'Other'),
		(FACEBOOK, 'Facebook'),
		(TWITTER, 'Twitter'),
		(LINKEDIN, 'LinkedIn'),
		(AIRBNB, 'Airbnb'),
		(GOOGLEPLUS, 'Google+'),
		(EBAY, 'eBay'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='social_profiles')
	site = models.SmallIntegerField(choices=SITE_CHOICES, default=OTHER)
	url = models.URLField()
	time_added = models.DateTimeField(auto_now_add=True)
	time_modified = models.DateTimeField(auto_now=True)

	def get_site_from_url(self, url):
		from urlparse import urlparse

		url_host = urlparse(url).netloc.split('.')[-2:][0]

		social_sites = {
			'facebook': self.FACEBOOK,
			'twitter': self.TWITTER,
			'linkedin': self.LINKEDIN,
			'airbnb': self.AIRBNB,
			'google': self.GOOGLEPLUS,
			'ebay': self.EBAY
		}

		if url_host in social_sites:
			return social_sites[url_host]
		else:
			return self.OTHER

class Interview(models.Model):
	interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='interviewers')
	interviewee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interviewees')
	uuid = models.CharField(unique=True, default=create_uuid, max_length=255)
	time_added = models.DateTimeField(auto_now_add=True)
	time_modified = models.DateTimeField(auto_now=True)

class Video(models.Model):
	interview = models.ForeignKey(Interview)
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	uuid = models.CharField(max_length=255)
	thumb_url = models.URLField()
	small_thumb_url = models.URLField()
	video_url = models.URLField()
	time_added = models.DateTimeField(auto_now_add=True)
	time_modified = models.DateTimeField(auto_now=True)

