from django import forms


class AddProd(forms.Form):
    title = forms.CharField(max_length=50)
    cost = forms.IntegerField(max_length=50)


class PurchaseForm(forms.Form):
    count = forms.IntegerField()
