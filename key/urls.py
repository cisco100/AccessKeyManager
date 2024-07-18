from django.urls import path
from key import views

urlpatterns = [ 
    path('',views.home,name="home"), 
    path('dashboard/',views.dashboard,name="dashboard"),
    path('keys/generate/', views.request_new_key, name='new_key'),
    path('keys/<uuid:key_id>/revoke/', views.revoke_key, name='revoke_key'),
    path('verify-key/', views.verify_key, name='verify_key'),

    ]