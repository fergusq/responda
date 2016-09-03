from django import forms

from .models import Message
from django.contrib.auth.models import User

class ReplyForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['message_text']
		labels = { 'message_text': '' }
