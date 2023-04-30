from django import forms
from .models import CartItem

from django import forms
from .models import *

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['nom', 'email', 'address', 'city']
