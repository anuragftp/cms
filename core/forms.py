from django import forms
from core.models import Paper

class PaperForm(forms.ModelForm):
	class Meta:
		model=Paper
		fields=('title','description','status','file')
		# widgets={
		# 		'description':forms.Textarea(attrs={'rows':3,'cols':10,'class':'form-control mt-3 ','placeholder':'Description'}),
		# }