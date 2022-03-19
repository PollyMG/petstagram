from datetime import date

from django import forms

from petstagram.common.helpers import BootstrapFormMixin, DisabledFieldsFormMixin
from petstagram.main.models import Pet
from petstagram.common.validators import MaxDateValidator


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        # commit False does not persist to datebase
        # just returns the object to be created
        pet = super().save(commit=False)

        pet.user = self.user
        if commit:
            pet.save()
        return pet

    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth')
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter pet name',
                }
            ),
        }


class EditPetForm(BootstrapFormMixin, forms.ModelForm):
    MIN_DATE_OF_BIRTH = date(1920, 1, 1)
    MAX_DATE_OF_BIRTH = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean_date_of_birth(self):
        MaxDateValidator(date.today())(self.cleaned_data['date_of_birth'])
        return self.cleaned_data['date_of_birth']

    # def clean_date_of_birth(self):
    #     date_of_birth = self.cleaned_data['date_of_birth']
    #     if date_of_birth < self.MIN_DATE_OF_BIRTH or \
    #             self.MAX_DATE_OF_BIRTH < date_of_birth:
    #         raise ValidationError(f'Date of birth must be between {self.MIN_DATE_OF_BIRTH} and {self.MAX_DATE_OF_BIRTH}')
    #     return date_of_birth

    class Meta:
        model = Pet
        exclude = ('user_profile', )


class DeletePetForm(BootstrapFormMixin, DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Pet
        exclude = ('user_profile', )
