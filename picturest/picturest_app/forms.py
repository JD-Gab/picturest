from django import forms
from .models import userPictures

class userPicturesForm(forms.ModelForm):

    title  = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter title...', 'id': 'titleInput'}), label="Title")
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control mb-3', 'placeholder': 'formFile', 'id':'formFile'}), label="Upload Image"
        )
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter description...', 'id': 'descriptionInput', 'rows': 3, 'maxlength': '900'}), label="Description", required=False)

    
    class Meta:
        model = userPictures
        fields = ['title', 'image', 'description']