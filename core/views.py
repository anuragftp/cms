from django.shortcuts import render, redirect , get_object_or_404
from django.views.generic import View
from core.forms import PaperForm,FormStatus,ReviewUpload,ReviewUpdate,ContactForm
from core.models import Paper,PaperAssign,Reviewer,Contact
from django.contrib import messages
from django.db.models import Sum,Count
from django.contrib.auth import get_user_model
from django.db.models import F,Q
from datetime import datetime
import os
from django.conf import settings
from django.http import HttpResponse


from django.http import FileResponse
from django.views.generic.detail import BaseDetailView
# from wagtail.documents.views import serve

User = get_user_model()
# Create your views here.


class Home(View):
	template_name='core/home/homepage.html'

	def get(self,request):
		return render(request,self.template_name)

class Publish(View):
	template_name='core/home/publish.html'

	def get(self,request):
		obj=Paper.objects.filter(status="Approved")
		if obj.exists():
			delta=[]
			for i in obj:
				delta.append((datetime.now().date()-i.review_date.date()).days)
			context={'mylist': zip(obj, delta)}
			# breakpoint()
			return render(request,self.template_name,context)
		messages.error(request,"No Paper Yet !",extra_tags="error")
		# breakpoint()
		return render(request,self.template_name)

class Userhomepage(View):
	template_name='core/feed.html'
	template_name1='core/reviewer.html'


	def get(self,request):
		if Reviewer.objects.filter(user=request.user).exists():  
			obj=PaperAssign.objects.filter(review=request.user.reviewer.id)
			pp=obj.exists()
			if pp:
				# obj=request.user.reviewer.assigned_paper.select_related('assign_paper').annotate(paper=F('assign_paper')).values('paper')
				obj=PaperAssign.objects.filter(review=request.user.reviewer.id)
				result=PaperAssign.objects.filter(Q(review=request.user.reviewer.id) & Q(is_review=False)).values_list('is_review',flat=True).aggregate(total=Count('is_review'))
				obj1=request.user.reviewer.assigned_paper.select_related('assign_paper').annotate(paper=F('assign_paper')).values_list('paper',flat=True)
				# obj=Paper.objects.filter(id=request.user.reviewer.assigned_paper.select_related('assign_paper').annotate(paper=F('assign_paper')).values_list('assign_paper')).all()
				context={'mylist': zip(obj, obj1),'result':result}

				# context={'obj':obj,'objj':obj1}
				# context{'mylist'}
				# breakpoint()
				return render(request,self.template_name1,context)
			messages.error(request,"No Any Paper Assigned !",extra_tags="error")
			return render(request,self.template_name1)

		else:
			p=Paper.objects.filter(user=request.user).exists()
			if p:
				obj=Paper.objects.filter(user=request.user).all()
				obj1=Paper.objects.filter(user=request.user).aggregate(total_paper=Count('user'))
				context={'obj':obj,'obj1':obj1}			
				return render(request,self.template_name,context)
			messages.error(request,"No Any Document Uploaded !",extra_tags="error")
			return render(request,self.template_name)




class UploadPaper(View):
	template_name='core/uploadpaper.html'
	form_class = PaperForm

	def get(self,request):
		form=self.form_class()
		context={'form':form}
		return render(request,self.template_name,context)

	def post(self,request):
		form=self.form_class(request.POST,request.FILES)
		
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user=request.user
			# breakpoint()
			instance.save()
			return redirect('home_view')
		# breakpoint()
		context={'form':form}

		return render(request,self.template_name,context)

class DeletePaper(View):
	template_name="core/feed.html"
	def get(self,request,*args,**kwargs):
		paper_key=self.kwargs.get('id',None)
		result=Paper.objects.filter(id=paper_key).filter(status="Submitted")
		# breakpoint()
		if result.exists():
			result.delete()
		return redirect('home_view')

# def validate_file_extension(value):
#     if not value.name.endswith('.pdf'):
#         raise ValidationError(u'Error message')



# class DisplayPdfView(BaseDetailView):
# 	template_name='core/home/openpdf.html'
# 	def get(self,request,*args,**kwargs):
# 		objkey = self.kwargs.get('id', None)
# 		pdf = get_object_or_404(Paper, pk=objkey)
# 		# breakpoint()
# 		fname = pdf.filename()
# 		path = os.path.join(settings.MEDIA_ROOT, "author_files", fname)
# 		response = FileResponse(open(path, 'rb'), content_type="pdf")

# 		return response
	        

class UpdateReview(View):
	template_name='core/updatereview.html'
	form_class = FormStatus
	def get(self,request,*args,**kwargs):
		detail_id = kwargs.get('id')
		# detail_info=Paper.objects.filter(pk=detail_id).values_list('title','description','status','file')
		detail_info=Paper.objects.filter(pk=detail_id).all()
		context={'detail_info':detail_info,}
		# breakpoint()
		return render(request,self.template_name,context)

	def post(self,request,*args,**kwargs):
		detail_id = kwargs.get('id')
		obj=Paper.objects.get(pk=detail_id)
		obj1=PaperAssign.objects.get(assign_paper=detail_id)

		form=self.form_class(request.POST)
		# breakpoint()
		if form.is_valid():
			obj.status=form.cleaned_data.get('status')
			if obj.status=="Review":
				obj.is_review_submit=False
			obj.remarks=form.cleaned_data.get('remarks')
			obj.rating=form.cleaned_data.get('rating')
			obj.review_by=request.user.id
			obj.review_date=datetime.now()
			obj1.is_review=True
			obj.save()
			obj1.save()
		# obj1=Paper.objects.filter(pk=detail_id).values_list('updated_on')
		# context={'obj1':obj1}
		# breakpoint()
		return redirect('home_view')


	
class ViewAll(View):
	template_name = 'core/viewallreview.html'

	def get(self,request):
		obj=PaperAssign.objects.filter(review=request.user.reviewer.id)
		pp=obj.exists()
		if pp:
			obj1=request.user.reviewer.assigned_paper.select_related('assign_paper').annotate(paper=F('assign_paper')).values_list('paper',flat=True)
			context={'mylist': zip(obj, obj1)}
			return render(request,self.template_name,context)
		messages.error(request,"No Any Paper Assigned !",extra_tags="error")
		return render(request,self.template_name)

class NotReview(View):
	template_name = 'core/viewallreview.html'

	def get(self,request):
		obj=PaperAssign.objects.filter(review=request.user.reviewer.id).filter(is_review=False)
		pp=obj.exists()
		if pp:
			obj1=request.user.reviewer.assigned_paper.select_related('assign_paper').annotate(paper=F('assign_paper')).values_list('paper',flat=True)
			context={'mylist': zip(obj, obj1)}
			return render(request,self.template_name,context)
		messages.error(request,"No Any Paper !",extra_tags="error")
		return render(request,self.template_name)

class ReReview(View):
	template_name='core/reviewpaper.html'
	def get(self,request):
		pp=Paper.objects.filter(review_by=request.user.id).filter(status="Review").exists()
		if pp:
			obj=Paper.objects.filter(review_by=request.user.id).filter(status="Review").all()
			context={'obj':obj}
			# breakpoint()
			return render(request,self.template_name,context)
		messages.error(request,"No Any Review-Paper !",extra_tags="error")
		return render(request,self.template_name)

class ReReviewUpdate(View):
	template_name='core/reviewpaper.html'
	form_class = ReviewUpdate
	def post(self,request,*args,**kwargs):
		paper_id = kwargs.get('id')
		obj=Paper.objects.filter(review_by=request.user.id).get(pk=paper_id)
		form=self.form_class(request.POST)
		if form.is_valid():
			obj.status=form.cleaned_data.get('status')
			if obj.status=="Review":
				obj.is_review_submit=False
			obj.remarks = form.cleaned_data.get('remarks')
			obj.rating = form.cleaned_data.get('rating')
			obj.review_date=datetime.now()
			obj.save()
		# breakpoint()
		return redirect('home_view')


class Review(View):
	template_name='core/review.html'
	form_class = ReviewUpload

	def get(self,request):
		pp=Paper.objects.filter(user=request.user).filter(status="Review").filter(is_review_submit=False).exists()
		if pp:
			obj=Paper.objects.filter(user=request.user).filter(status="Review").all()
			context={'obj':obj}
			return render(request,self.template_name,context)
		messages.error(request,"No Any Review-Paper !",extra_tags="error")
		return render(request,self.template_name)

class ReviewUpload(View):
	template_name='core/review.html'
	form_class = ReviewUpload
	def post(self,request,*args,**kwargs):
		paper_id = kwargs.get('id')
		obj=Paper.objects.filter(user=request.user).get(pk=paper_id)
		form=self.form_class(request.POST,request.FILES)
		if form.is_valid():
			obj.is_review_submit=True
			obj.file=form.cleaned_data.get('file')
			obj.save()
		# breakpoint()
		return redirect('home_view')


class ContactView(View):
	template_name='core/contact.html'
	form_class=ContactForm
	

	def get(self,request):
		form=self.form_class()
		contact_list=Contact.objects.filter(email=request.user.email).all()[:3]
		context={'form':form,'contact_list':contact_list}
		return render(request,self.template_name,context)

	def post(self,request):
		form=self.form_class(request.POST)
		contact_list=Contact.objects.all()
		if form.is_valid():
			instance=form.save(commit=False)
			instance.user=request.user
			instance.save()
			return redirect('contact_view')
			
		context={'form':form,'contact_list':contact_list}
		return render(request,self.template_name,context)





