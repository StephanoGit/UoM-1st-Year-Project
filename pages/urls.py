from django.urls import path, include
from . import views
from django_email_verification import urls as mail_urls

urlpatterns = [
  path('home', views.home_view, name="homePage"),
  # path('', views.home_view, name="homePage"),
  path('accommodation/<str:pk>', views.accommodation, name="accommodation"),
  path('search/', views.search, name="search"),
  path('logout/', views.logout_view, name="logoutPage"),
  path('login/', views.login_view, name="loginPage"),
  path('register/', views.register_view, name="registerPage"),
  path('comment/', views.comment, name="commentPage"),
  path('question/', views.question, name="questionPage"),
  #path('question/', views.answer, name="answerPage"),
  path('answer/', views.answer, name="answerbutton"),
  path('', views.loading_view, name="loadingPage"),
  # path('loading/', views.loading_view, name="loadingPage"),

  path('send_email', views.sendEmail),
  path('email/', include(mail_urls)),

  path('about/' , views.about , name = "about"),
  path('terms_and_conditions/' , views.terms_and_conditions , name = "terms_and_conditions"),
  path('ranking/' , views.ranking_view , name = "ranking")
]