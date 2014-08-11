from rango.models import Page, Category, UserProfile
from django import forms
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=120,help_text='Please enter category name')
    views = forms.IntegerField(widget = forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget = forms.HiddenInput(),initial=0)
    
    class Meta:
        model = Category
        
        
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=120,help_text='Please enter title for Page')
    url= forms.URLField(max_length=200,help_text='Please enter url for Page')
    views = forms.IntegerField(widget = forms.HiddenInput(),initial=0)
    
    class Meta:
        model = Page
        
        fields = ('title', 'url', 'views')
        

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username' , 'password' , 'email')
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture', 'website')