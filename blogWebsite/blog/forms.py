from django import forms
from .models import Comment

class EmailForm(forms.Form):
	name=forms.CharField(max_length=25)
	email=forms.EmailField()
	to=forms.EmailField()
	message=forms.CharField(required=False,widget=forms.Textarea)


#Comment form from Comment model

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=('name','emailID','comment')
