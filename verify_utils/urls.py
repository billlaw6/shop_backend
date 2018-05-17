from django.conf.urls import url

from verify_utils import views

urlpatterns = [
    url(r'^get_captcha', views.get_captcha, name='get_captcha'),
]
