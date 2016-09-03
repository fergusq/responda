from django.db import models
from django.conf import settings

# Create your models here.

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Message(models.Model):
	message_text = models.TextField()
	pub_date = models.DateTimeField('date published')
	author = models.ForeignKey(AUTH_USER_MODEL)
	parent_message = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)

	def __str__(self):
		return '"' + (self.message_text if len(self.message_text) < 30 else self.message_text[:30] + '...') + '"'
