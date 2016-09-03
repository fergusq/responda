from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^messages/(?P<msg_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^messages/(?P<msg_id>[0-9]+)/reply/$', views.reply, name='reply'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
]
