from django import forms


class UpdateForm(forms.Form):
    """Dummy form for updates."""
    status = forms.HiddenInput()
