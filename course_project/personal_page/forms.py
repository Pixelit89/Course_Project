from django import forms
from .models import Account


class PostForm(forms.Form):
    post_name = forms.CharField(
        max_length=512,
        widget=forms.TextInput
    )
    post_text = forms.CharField(
        widget=forms.Textarea
    )

    def clean(self):
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'avatar']
