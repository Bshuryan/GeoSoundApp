from django import forms


class ReturningUserForm(forms.Form):
    email = forms.CharField(label='exampleInputEmail1')
    password = forms.CharField(label='exampleInputPassword1')
