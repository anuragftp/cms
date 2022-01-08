from django.shortcuts import render, redirect
from django.views.generic import View
from core.forms import PaperForm,FormStatus,ReviewUpload,ReviewUpdate,ContactForm
from core.models import Paper,PaperAssign,Reviewer,Contact
from django.contrib import messages
from django.db.models import Sum,Count
from django.contrib.auth import get_user_model
from django.db.models import F,Q
from datetime import datetime

User = get_user_model()
# Create your views here.


class Home(View):
	template_name='core/home/homepage1.html'

	def get(self,request):
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


# class Home(View):
# 	template_name="core/reviewer.html"

# 	def get(self,request):
# 		obj=request.user.reviewer.assigned_paper.select_related('assigned_paper__assign_paper').annotate(paper=F('assign_paper')).values('paper')
# 		# obj=request.user.reviewer.assigned_paper.select_related('assign_paper')
# 		context={'obj':obj}
# 		breakpoint()
# 		return render(request,self.template_name,context)

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





