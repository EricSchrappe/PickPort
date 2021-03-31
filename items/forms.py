from django import forms
from items.models import Items


class ItemForm(forms.ModelForm):

	class Meta():
		fields = ('name',)
		model = Items

