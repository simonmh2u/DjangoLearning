from rango.models import Page, Category
from django import forms

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
        
