"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^login/', views.login, name='login'),
    url('^loginForm/', views.loginForm, name='loginForm'),
    url('^recover/', views.recover, name='recover'),
    url('^recoverForm/', views.recoverForm, name='recoverForm'),
    #url('^arecover/', views.arecover, name='arecover'),
    url('^registerationForm/', views.registrationForm, name='registrationForm'),
    url('^product/', views.product, name='product'),
    url('^add/', views.add, name='add'),
    url('^admin/', views.admin, name='admin'),
    url('^remove/', views.remove, name='remove'),
    url('^removeItem/', views.removeItem, name='removeItem'),
    url('^removeFromCart/', views.removeFromCart, name='removeFromCart'),
    url('^displayCategory/', views.displayCategory, name='displayCategory'),
    url('^productDescription/', views.productDescription, name='productDescription'),
    url('^addToCart/', views.addToCart, name='addToCart'),
    url('^cart/', views.cart, name='cart'),
    url('^address/', views.bill, name='address'),
    url('^bill/', views.address, name='bill'),
    url('^register/', views.register, name='register'),
    url('^logout/', views.logout, name='logout'),
    url('^logout1/', views.logout1, name='logout1'),
    url('^end/', views.end, name='end'),
    url('^end2/', views.end2, name='end2'),
    url('^alogin/', views.alogin, name='alogin'),
    url('^aloginForm/', views.aloginForm, name='aloginForm'),
    url('^aregister/', views.aregister, name='aregister'),
    url('^aregisterationForm/', views.aregistrationForm, name='aregistrationForm'),
    url('^edit/', views.edit, name='edit'),
    url('^catadd/', views.catadd, name='catadd'),
    url('^catadmin/', views.catadmin, name='catadmin'),
    url(r'^update/(?P<productId>\d+)/$', views.update, name='update'),
    url(r'^order/', views.order, name='order'),
]