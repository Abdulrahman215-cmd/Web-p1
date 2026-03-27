from django import forms
from .models import All_Posts

class All_PostsForm(forms.ModelForm):
    class Meta:
        model = All_Posts
        fields = ['NewPost']
        labels = {
            'NewPost': ''
        }
        widgets = {
            'NewPost': forms.Textarea(attrs={'cols': 70, 'rows': 3,
                                                'style': 'font-size: 18px;'}),
        }