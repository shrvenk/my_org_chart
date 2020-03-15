from django import forms
from django.contrib.auth.models import User
from .models import detail


class addemployee(forms.ModelForm):
    
    class Meta:
        model = detail
        fields = ['emp_id','manager_id','status','last_name','preferred_name','work_phone','personal_email','location','department',]
        widgets = {
            'emp_id': forms.NumberInput(attrs={'class':'form-control'}),
            'status': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'preferred_name': forms.TextInput(attrs={'class':'form-control'}),
            'work_phone': forms.TextInput(attrs={'class':'form-control'}),
            'personal_email': forms.EmailInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'}),
            'department': forms.TextInput(attrs={'class':'form-control'}),
            'manager_id' : forms.NumberInput(attrs={'class':'form-control'}),
        }


