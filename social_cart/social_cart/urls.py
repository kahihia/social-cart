"""social_cart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from social_cart import views

admin.autodiscover()
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^home/$', views.HomeView.as_view()),
    url(r'^login/$', views.LoginView.as_view(), name='social_login'),
    url(r'^search/', views.UserSearchView.as_view()),
    url(r'^friends/(?P<shopper_id>\w+)/$', views.FriendsView.as_view()),
    url(r'^friends/$', views.FriendsView.as_view()),
    url(r'^products/$', views.ProductsView.as_view()),
    url(r'^shop/$', views.GoShopView.as_view()),
    url(r'^social-cart/$', views.SocialCartTemplateView.as_view()),
    url(r'^social-cart/update/$', views.SocialCartShopperView.as_view()),
    url(r'^social-cart/finalize/$', views.SocialCartShopperView.as_view()),
    url(r'^social-cart-add/$', views.SocialCartInviteeView.as_view()),
    url(r'^go-social/$', views.SocialCartInviteeView.as_view()),
    url(r'^gcm_key/$', views.gcm_key_view),
    url(r'^$', views.login_redirect_view),
    url(r'^invitees/$', views.CartInviteTemplateView.as_view()),
]

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'^groups', views.GroupViewSet, base_name='Groups')
urlpatterns += router.urls
