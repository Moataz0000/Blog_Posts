from django import forms 
from .models import Comment





class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={"class":'form-control', 'placeholder':'Enter Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Your Email'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter E-mail'}))
    comments = forms.CharField(required=False , widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter Your Notes!'}))




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }



class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mr-sm-2", 'placeholder': 'Search'}))
