from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^messages/(?P<msg_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^messages/(?P<msg_id>[0-9]+)/reply/$', views.reply, name='reply'),
	url(r'^messages/(?P<msg_id>[0-9]+)/select/$', views.select, name='select'),
	url(r'^selected/clear/$', views.clearselected, name='clearselected'),
	url(r'^selected/reply/$', views.replyselected, name='replyselected'),
	url(r'^replies/$', views.replies, name='replies'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
]
