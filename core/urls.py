from django.urls import path
from django.contrib.auth.decorators import login_required
from core.views import (
      Home,
      Userhomepage,
      UploadPaper,
      UpdateReview,
      ContactView,
      ViewAll,
      ReReview,
      NotReview,
      Review,
      ReviewUpload,
      ReReviewUpdate,
      Publish,
   )
urlpatterns=[
   path('',Home.as_view(),name='home'),
   path('view-publish/',Publish.as_view(),name='publish_view'),
   path('feed/dashboard',login_required(Userhomepage.as_view()),name='home_view'),
   path('feed/author/upload_paper/',login_required(UploadPaper.as_view()),name='upload_paper_view'),
   path('feed/reviewer/update_review/<int:id>',login_required(UpdateReview.as_view()),name='update_review_view'),
   path('feed/dashboard/contact/',login_required(ContactView.as_view()),name='contact_view'),
   path('feed/author/review',login_required(Review.as_view()),name='paper_review_view'),
   path('feed/author/review/<int:id>',login_required(ReviewUpload.as_view()),name='ReUpload_view'),
   path('feed/reviewer/view_all/',login_required(ViewAll.as_view()),name='view_all_view'),
   path('feed/reviewer/re-review/',login_required(ReReview.as_view()),name='re_view'),
   path('feed/reviewer/re-review/<int:id>',login_required(ReReviewUpdate.as_view()),name='ReReviewUpdate_view'),
   
   path('feed/reviewer/not_review/',login_required(NotReview.as_view()),name='NotReview_view'),


]