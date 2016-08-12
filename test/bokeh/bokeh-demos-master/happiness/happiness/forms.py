from django import forms

from .models import Happiness


class HappinessForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HappinessForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            # Add bootstrap class
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['happiness'].widget.attrs['min'] = 0
        self.fields['happiness'].widget.attrs['max'] = 9
        self.fields['happiness'].widget.attrs['style'] = 'width: 60px;'
        self.fields['date'].widget.attrs['style'] = 'width: 100px;'

    class Meta:
        model = Happiness
        exclude = ('employee',)
