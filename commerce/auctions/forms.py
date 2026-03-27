from django import forms
from .models import auction_listing, Bid, Comment

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = auction_listing
        fields = ['title', 'image_url', 'description', 'starting_bid', 'category']
        labels = {
            'image_url': '',
            'description': '',
            'title': '',
            'starting_bid': '',
        }
        widgets = {
            'image_url': forms.URLInput(attrs={'placeholder': 'Enter Image URL Here (Optional)',
                                               'style': 'width: 529px; font-size: 22px;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description Here',
                                                 'cols': 47, 'rows': 8,
                                                 'style': 'font-size: 22px;'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title Here',
                                               'style': 'width: 529px; font-size: 22px;'}),
            'starting_bid': forms.NumberInput(attrs={'placeholder': 'Enter Your Starting Price Here',
                                                'style': 'width: 529px; font-size: 20px;'}),
            'category': forms.Select(attrs={'style': 'width: 457px; font-size: 22px;'})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': ''
            }
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Place Amount Here',
                                               'style': 'width: 520px; position: relative; left: 10px; font-size: 22px'
                                               }),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']
        labels = {
            'comments': ''
            }
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Add Comment Here',
                                                 'cols': 90, 'rows': 3,
                                                 'style':'font-size: 22px; position: relative; left: 10px;' 
                                                 }),
        }