from django.core.exceptions import ValidationError
from django import forms
from contact.models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
            }
        )
    )

    

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture')

    def clean(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) > 20:
            self.add_error('phone', ValidationError('Numero de telefone invalido', code='invalid'))

        return super().clean()
    
    