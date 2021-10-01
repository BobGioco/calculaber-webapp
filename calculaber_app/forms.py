from django import forms
from calculaber_app.models import Project,Object,Material,MaterialObject

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','project_pic')

class CreateObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name',)

class CreateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name','margin','price','units',)

class CreateMaterialObjectForm(forms.ModelForm):
    class Meta:
        model = MaterialObject
        fields = ('name','material','amount')

    def __init__(self, user,*args, **kwargs):
        super(CreateMaterialObjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'class':"form-control",
                'name':'name',
                'placeholder': 'Název'}
        self.fields['material'].widget.attrs={
                'class':"form-control",
                'name':'material',}
        self.fields['amount'].widget.attrs={
                'class':"form-control",
                'name':'amount',
                'placeholder': 'Množství'}

        if user:
            self.fields['material'].queryset = Material.objects.filter(user=user)


    def clean(self):
        all_clean_data= super().clean()

class UpdateMaterialObjectForm(forms.ModelForm):
    class Meta:
        model = MaterialObject
        fields = ('name','amount','customized','price','margin')

    def __init__(self, user,*args, **kwargs):
        super(UpdateMaterialObjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'id':"id_name_update",
                'class':"form-control",
                'name':'name',
                'placeholder': 'Název'}
        self.fields['amount'].widget.attrs={
                'id':"id_amount_update",
                'class':"form-control",
                'name':'amount',
                'placeholder': 'Množství'}
        self.fields['customized'].widget.attrs={
                'id':"id_customized_update",
                'class':"form-check-input",
                'name':'customized',
                }
        self.fields['price'].widget.attrs={
                'id':"id_price_update",
                'class':"form-control",
                'name':'price',
                'placeholder': 'Cena'}
        self.fields['margin'].widget.attrs={
                'id':"id_margin_update",
                'class':"form-control",
                'name':'margin',
                'placeholder': 'Margin'}

    def clean(self):
        all_clean_data= super().clean()
