from django.urls import path
from . import views

app_name = 'article_keyword_check'
urlpatterns = [
    path('', views.keyword_home_view, name='home'),
    path('article/', views.key_word_search, name='article_kw'),
    path('about/', views.forms_python, name='about'),
    path('findemail/', views.email_extractor_view, name='email_extractor'),
]