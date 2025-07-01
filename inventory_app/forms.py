from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Supplier, RawMaterial, Product, StockEntry, SpoilageAssessment
from .models import RawMaterial

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'reliability_score']

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = '__all__'  # Adjust fields as needed (e.g., ['name', 'expiry', ...])
        widgets = {
            'expiry': forms.DateInput(attrs={'type': 'text', 'class': 'datepicker'}),  # Use text type for Flatpickr
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'raw_materials', 'production_date']

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = ['product', 'quantity']

class SpoilageAssessmentForm(forms.ModelForm):
    class Meta:
        model = SpoilageAssessment
        fields = ['raw_material', 'avg_temp', 'days_stored']