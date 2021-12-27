from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'full_name',
            'picture',
            'email',
            'bio',
            'mobile',
            'address',
            'city',
            'gender',
            'is_private_account',
            )
        labels = {
            'is_private_account': 'Do you want to make your account private ?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == 'picture':
                self.fields[field].widget.attrs.update({'class': 'form-control-file'})
            elif field == 'is_private_account':
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control form-control-sm'})



class UserForm(UserCreationForm):
    class Meta:
        # model=User
        model=get_user_model()
        fields=('full_name','email','password1','password2')

        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model=get_user_model()
        fields=('full_name','email')