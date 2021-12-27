from django.urls import path
from django.contrib.auth.decorators import login_required
from core.views import (
      Home,
      UploadPaper,
   )
urlpatterns=[
   # path('home/',home,name='home'),
   path('home/',login_required(Home.as_view()),name='home_view'),
   path('author/upload_paper/',login_required(UploadPaper.as_view()),name='upload_paper_view'),


]