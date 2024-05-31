from django.urls import path
from . import views 


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('',views.home,name="home"),
    path('room/<str:pk>',views.room,name="room"),

    path('calculate-CF/',views.calculateCF,name="calculate-CF"),
    path('leaderboard/',views.leaderboard,name='leaderboard'),
    path('challenges/',views.challenges,name='challenges'),
    path('log-action/<int:challenge_id>/',views.log_action,name='log_action'),
    path('join-challenge/<int:challenge_id>/', views.join_challenge, name='join_challenge'),
]