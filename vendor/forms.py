from django import forms
from vendor.models import Vendor, OpeningHour
from accounts.validators import allow_only_images_validators

class vendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validators])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']

class openingHourForm(forms.ModelForm):

    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']