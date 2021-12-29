from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout,get_user_model
from accounts.forms import UserEditForm,UserForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (
	PasswordResetView,
	PasswordResetConfirmView,
	PasswordResetDoneView,
	PasswordResetCompleteView,
	PasswordChangeView,
	PasswordChangeDoneView,

	)

# Create your views here.

User=get_user_model()


# def home(request):
# 	return HttpResponse("Welcome to this world")


class SignInView(View):
	template_name='accounts/signin1.html'

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			return redirect('home_view')
		return render(request,self.template_name)
		
	
	def post(self,request,*args,**kwargs):
		email=request.POST.get('email')
		password=request.POST.get('password')

		try:
			user_obj=User.objects.get(username=email)
			email=user_obj.email

		except Exception as e:
			email=email
		
		user=authenticate(request,email=email,password=password)
		# breakpoint()
		if user is None:
			messages.error(request,"Invalid Login ",extra_tags="error")
			return render(request,self.template_name)


		login(request,user)
		# messages.success(request,"Thanks for Login, Welcome to Blood Donation System")
		
		return redirect('home_view')



class SignUpView(View):
	template_name='accounts/signup1.html'

	form_class=UserForm
	# form_class1=DetailsForm

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			return redirect('home_view')
		return render(request,self.template_name)

	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST)
		if form.is_valid():
			form.save()
			return redirect('signin_view')

		context={'form':form}

		return render(request,self.template_name,context)


class SignOutView(View):
	def post(self,request,*args,**kwargs):
		logout(request)
		return redirect('signin_view')

class PRView(PasswordResetView):
	template_name='accounts/password_reset.html'
	email_template_name='accounts/password_reset_email.html'


class PRConfirm(PasswordResetConfirmView):
    template_name='accounts/password_reset_confirm.html'

class PRDone(PasswordResetDoneView):
	template_name='accounts/password_reset_done.html'

class PRComplete(PasswordResetCompleteView):
	template_name='accounts/password_reset_complete.html'

class PWDChangeView(PasswordChangeView):
	template_name='accounts/password_change.html'
	success_url=reverse_lazy('password_change_done_view')

class PWDChangeDoneView(PasswordChangeDoneView):
	template_name='accounts/password_change_done.html'

class ProfileView(View):
	template_name='accounts/profile.html'
	def get(self,request,*args,**kwargs):
		username=kwargs.get('username')
		try:
			user=User.objects.get(full_name=username)
		except Exception as e:
			return HttpResponse('<h1>This page is not exist </h1>')

		if username == request.user.full_name:
			context={'user':user}
			return render(request,self.template_name,context)
		
		else:
			return HttpResponse('<h1>This page is not exist </h1>')




class ProfileEditView(View):
	template_name='accounts/profile_edit.html'
	form_class=UserEditForm
	def get(self,request,*args,**kwargs):
		username=kwargs.get('username')
		if username != request.user.full_name:
			return HttpResponse('<h1>This page is not exist </h1>')
		form=self.form_class(instance=request.user)
		context={'form':form}
		# breakpoint()
		return render(request,self.template_name,context)


	def post(self,request,*args,**kwargs):
		form=self.form_class(request.POST,request.FILES,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'Saved !')
			return redirect('profile_view',request.user.full_name)

		else:
			for field in form.errors:
				form[field].field.widget.attrs['class'] += ' is-invalid'
			context={'form':form}
			return render(request,self.template_name,context)


