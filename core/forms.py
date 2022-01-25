from django import forms
from core.models import Paper,Contact

class PaperForm(forms.ModelForm):
	class Meta:
		model=Paper
		fields=('title','description','file')
		# widgets={
		# 		'description':forms.Textarea(attrs={'rows':3,'cols':10,'class':'form-control mt-3 ','placeholder':'Description'}),
		# }

class FormStatus(forms.ModelForm):
	class Meta:
		model=Paper
		fields=('title','description','status','remarks','rating')

class ReviewUpdate(forms.ModelForm):
	class Meta:
		model=Paper
		fields=('status','remarks','rating')

class ReviewUpload(forms.ModelForm):
	class Meta:
		model=Paper
		fields=('title','file')
class ContactForm(forms.ModelForm):
	class Meta:
		model=Contact
		fields=('email','description',)
		widgets={
				
				'description':forms.Textarea(attrs={'rows':10,'cols':10,'class':'form-control mt-3','placeholder':'Description'}),


		}