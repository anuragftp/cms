from django.urls import path
from django.contrib.auth.decorators import login_required
from core.views import (
      Home,
      UploadPaper,
      UpdateReview,
      ViewAll,
      ReReview,
      NotReview,
   )
urlpatterns=[
   # path('home/',home,name='home'),
   path('feed/',login_required(Home.as_view()),name='home_view'),
   path('feed/author/upload_paper/',login_required(UploadPaper.as_view()),name='upload_paper_view'),
   path('feed/reviewer/update_review/<int:id>',login_required(UpdateReview.as_view()),name='review_view'),
   path('feed/reviewer/view_all/',login_required(ViewAll.as_view()),name='view_all_view'),
   path('feed/reviewer/re-review/',login_required(ReReview.as_view()),name='re_view'),
   path('feed/reviewer/not_review/',login_required(NotReview.as_view()),name='NotReview_view'),


]