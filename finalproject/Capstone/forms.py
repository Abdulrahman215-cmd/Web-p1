from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    REVIEW_CHOICES = [
        ('Good', 'Good'),
        ('Bad', 'Bad'),
    ]
    review_type = forms.ChoiceField(choices=REVIEW_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = Comment
        fields = ['comments']
        labels = {
            'comments': '',
            }
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Add Comment Here',
                                                 'cols': 60, 'rows': 3,
                                                 'style':'font-size: 22px; position: relative; left: 10px;' 
                                                 }),
        }