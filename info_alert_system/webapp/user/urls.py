from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('signup/', views.signup, name = 'signup'),
	path('signin/', views.signin, name = 'signin'),
	path('signup_submit/', views.signup_submit, name = 'signup_submit'),
	path('signin_submit/', views.signin_submit, name = 'signup_submit'),
	path('OTPcheck/', views.otp_check, name = 'otp_check'),
	path('user/', views.user_serve, name = 'user'),
	path('user_delete/', views.user_delete, name = 'user_delete'),
	path('alert/', views.alert, name = 'alert'),
	path('alert_create/', views.alert_create, name = 'alert_create'),
	path('alert_delete/', views.alert_delete, name = 'alert_delete'),
	path('alert_get/<int:alert_id>/', views.alert_get, name = 'alert_get'),
]