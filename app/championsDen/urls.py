from django.urls import path,include
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.contrib.auth import views as auth_views
from rest_framework import routers




urlpatterns = [
    path('', views.landingpage, name='homepage'),
    path('unathorized', views.unathorized, name='unathorized'),
    path('summoner', views.getSummoner),
    path('video', views.video_player, name='video_player'),
    path('tutor', views.tutor, name='tutor'),
    path('register', views.register_page, name='register'),
    path('login',views.user_login, name='login_link'),
    path('logout', views.user_logout, name='logout'),
    path('dashboard', views.summoner_dashboard, name='dashboard'),
    path('courses', views.courses, name='courses'),
    path('courses/<pk>', views.course, name='course'),
    path('index', views.index, name='index'),
    path('course-creator', views.course_creator, name='course_creator'),
    path('course-creator/<pk>', views.section_creator, name='section_creator'),
    path('<instruction>/<pk>', views.course_subscription, name='change-course'),
    path('course_detail', views.course_detail, name="course_detail"),


    #! Password Reset paths !#
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password" ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done" ),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),


    #! REST ENDPOINTS !#
    path('check', views.check, name="check")



]
