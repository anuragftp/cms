from django.shortcuts import render, redirect
from django.views.generic import View
from core.forms import PaperForm
from core.models import Paper,PaperAssign,Reviewer
from django.contrib import messages
from django.db.models import Sum,Count
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()
# Create your views here.


class Home(View):
	template_name='core/feed.html'
	template_name1='core/reviewer.html'


	def get(self,request):
		if Reviewer.objects.filter(user=request.user).exists():
			pp=PaperAssign.objects.filter(review=request.user.reviewer.id).exists()
			if pp:
				obj=request.user.reviewer.assigned_paper.select_related('assign_paper')
				context={'obj':obj}
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
