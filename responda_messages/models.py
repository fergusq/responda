from django.db import models
from django.conf import settings

# Create your models here.

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Message(models.Model):
	message_text = models.TextField()
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(AUTH_USER_MODEL)
	parent_message = models.ManyToManyField('self', related_name='replies', symmetrical=False)

	def __str__(self):
		return '"' + (self.message_text if len(self.message_text) < 30 else self.message_text[:30] + '...') + '"'
