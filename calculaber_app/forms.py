from django import forms
from calculaber_app.models import Project,Object,Material,MaterialObject

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','project_pic')
    def __init__(self, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'class':"form-control",
                'placeholder': 'Zadejte jméno projektu',}
        self.fields['project_pic'].widget.attrs={
                'class':"custom-file-input",
                }

class CreateObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(CreateObjectForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'class':"form-control",
                'name':'name',
                'placeholder': 'Název'}

class CreateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name','margin','price','units',)

    def __init__(self, *args, **kwargs):
        super(CreateMaterialForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'class':"form-control",
                'placeholder': 'Zadejte jméno matiálu',}
        self.fields['margin'].widget.attrs={
                'class':"form-control",
                'placeholder': 'Zadejte margin',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'placeholder': 'Zadejte cenu',}
        self.fields['units'].widget.attrs={
                'class':"custom-select",}

class UpdateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name','margin','price','units',)

    def __init__(self, *args, **kwargs):
        super(UpdateMaterialForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'update_material_name',
                'placeholder': 'Zadejte jméno matiálu',}
        self.fields['margin'].widget.attrs={
                'class':"form-control",
                'id':'update_material_margin',
                'placeholder': 'Zadejte margin',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'id':'update_material_price',
                'placeholder': 'Zadejte cenu',}
        self.fields['units'].widget.attrs={
                'class':"custom-select",
                'id':'update_material_units',}

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
