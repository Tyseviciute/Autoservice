from django import forms

from .models import OrderReview


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('content', 'order', 'reviewer')
        widgets = {'order': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


