from django import forms
from .models import Ad, ExchangeProposal
from .models import Profile

class AdForm(forms.ModelForm):
    # URLField без схемы → автоматически добавляем https
    image_url = forms.URLField(required=False, assume_scheme="https")

    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']

class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio"]
