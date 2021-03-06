from django import forms
from django.contrib.auth.models import User
from .models import List,Card


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ("username", "last_name", "first_name", "email",)



class ListForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = List
        fields = ("title",)



class CardForm(forms.ModelForm):
    class Meta:
        model=Card
        fields=("title","description","list")

    # def __init__(self, *args, **kwargs):
    #     super(CardForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(CardForm, self).__init__(*args, **kwargs)
        self.fields['list'].queryset = List.objects.filter(user=user)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

