from django import forms
from django.forms import ModelForm

from shop.models import ProductSizes


class SizeForm(ModelForm):
    class Meta:
        model = ProductSizes
        fields = ['sizes']

    def __init__(self, *args, **kwargs):
        super(SizeForm, self).__init__(*args, **kwargs)
        product = self.initial['product']
        size_set = product.sizes
        # [7,8,9,10,11,12]

        self.fields['sizes'] = forms.ModelChoiceField(
            queryset=size_set,
            widget=forms.RadioSelect(
                attrs={
                    'class': 'btn-check',
                    'autocomplete': 'off',
                    'disabled': False,
                }
            ),
            label="Size",
        )

