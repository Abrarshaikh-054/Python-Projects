"""
URL configuration for Furni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('cpass/',views.cpass,name='cpass'),
    path('uprofile/',views.uprofile,name='uprofile'),
    path('upicture/',views.upicture,name='upicture'),
    path('fpass/',views.fpass,name='fpass'),
    path('newpass/',views.newpass,name='newpass'),
    path('otp/',views.otp,name='otp'),
    path('shop/',views.shop,name='shop'),
    path('mdetails/<int:pk>',views.mdetails,name="mdetails"),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('addwish/<int:pk>',views.addwish,name='addwish'),
    path('removewish/<int:pk>',views.removewish,name='removewish'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('blog/',views.blog,name='blog'),
    path('contact/',views.contact,name='contact'),
    path('cart/',views.cart,name='cart'),
    path('addcart/<int:pk>',views.addcart,name='addcart'),
    path('deletecart/<int:pk>',views.deletecart,name='deletecart'),
    path('updateqty/<int:pk>',views.updateqty,name='updateqty'),
    path('checkout/',views.checkout,name='checkout'),
    path('myorders/',views.myorders,name='myorders'),
    path('thankyou/',views.thankyou,name='thankyou'),

    #-------------------seller side----------------------#

    path('sindex/',views.sindex,name="sindex"),
    path('padd/',views.padd,name="padd"),
    path('pview/',views.pview,name="pview"),
    path('sprofile/',views.sprofile,name="sprofile"),
    path('plist/',views.plist,name="plist"),
    path('pdetails/',views.pdetails,name="pdetails"),
    path('pupdate/<int:pk>',views.pupdate,name="pupdate"),
    path('pdelete/<int:pk>',views.pdelete,name="pdelete"),
    
]
