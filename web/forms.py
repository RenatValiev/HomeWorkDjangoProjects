from django import forms

from web.models import Advert, Car


class ModelFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class AdvertForm(ModelFormMixin, forms.ModelForm):
    car_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))

    def save(self, *args, **kwargs):
        self.instance.user = self.initial['user']
        self.instance.car = self.initial['car']
        return super(AdvertForm, self).save(*args, **kwargs)

    class Meta:
        model = Advert
        fields = ('car_name', 'price', 'description', 'image', 'color', 'mileage', 'generation', 'equipment')


class AuthForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


class UserForm(AuthForm):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))


class EditUserForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={
            'class': 'form-control'
        }
    ))
    password = forms.CharField(required=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control'
        }
    ))


# class CarForm(forms.ModelForm):
#     name = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     brand = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     engine = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     power = forms.IntegerField(widget=forms.NumberInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     transmission = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     drive = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     body_type = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))
#     wheel_type = forms.CharField(widget=forms.TextInput(
#         attrs={
#             'class': 'form-control'
#         }
#     ))

class CarForm(ModelFormMixin, forms.ModelForm):

    class Meta:
        model = Car
        fields = ('name', 'brand', 'engine', 'power', 'transmission', 'drive', 'body_type', 'wheel_type')
