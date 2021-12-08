from django import forms
from calculaber_app.models import Project,Object,Material,MaterialObject,ExtraExpense, MaterialTag, ObjectTag

class LocalizedModelForm(forms.ModelForm): #test
    def __new__(cls, *args, **kwargs):
        new_class = super(LocalizedModelForm, cls).__new__(cls, *args, **kwargs)
        for field in new_class.base_fields.values():
            if isinstance(field, forms.DecimalField):
                field.localize = True
                field.widget.is_localized = True
        return new_class

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

class MaterialTagForm(forms.ModelForm):
    class Meta:
        model = MaterialTag
        fields = ('tag',)

    def __init__(self, *args, **kwargs):
        super(MaterialTagForm, self).__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs={
                'class':"form-control",
                'name':'tag',
                'placeholder': 'zadej tag'}
    def clean(self):
        all_clean_data= super().clean()

class ObjectTagForm(forms.ModelForm):
    class Meta:
        model = ObjectTag
        fields = ('tag',)

    def __init__(self, *args, **kwargs):
        super(ObjectTagForm, self).__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs={
                'class':"form-control",
                'name':'tag',
                'placeholder': 'zadej tag'}
    def clean(self):
        all_clean_data= super().clean()

class CreateMaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateMaterialForm, self).__init__(*args, **kwargs)
#        self.fields['margin'].localize = True
#        self.fields['margin'].widget.is_localized = True

#        self.fields['price'].localize = True
#        self.fields['price'].widget.is_localized = True

        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'new_material_name',
                'placeholder': 'Zadejte jméno materiálu',}
        self.fields['margin'].widget.attrs={
                'class':"form-control",
                'id':'new_material_margin',
                'placeholder': 'Zadejte margin',
#                'localization': True,
                'step':'any',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'id':'new_material_price',
                'placeholder': 'Zadejte cenu',
#                'localization': True,
                'step':'any',}
        self.fields['units'].widget.attrs={
                'class':"custom-select",
                'id':'new_material_units',}

    class Meta:
        model = Material
        fields = ('name','margin','price','units',)
        #localized_fields = '__all__'

class UpdateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('name','margin','price','units',)
        #localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateMaterialForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'update_material_name',
                'placeholder': 'Zadejte jméno materiálu',}
        self.fields['margin'].widget.attrs={
                'class':"form-control",
                'id':'update_material_margin',
                'placeholder': 'Zadejte margin',
                'step':'any',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'id':'update_material_price',
                'placeholder': 'Zadejte cenu',
                'step':'any',}
        self.fields['units'].widget.attrs={
                'class':"custom-select",
                'id':'update_material_units',}

class CreateMaterialObjectForm(forms.ModelForm):
    class Meta:
        model = MaterialObject
        fields = ('name','material','amount')

    def __init__(self, user,*args, **kwargs):
        super(CreateMaterialObjectForm, self).__init__(*args, **kwargs)
        self.fields['amount'].localize = True
        self.fields['amount'].widget.is_localized = True

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
                'placeholder': 'Množství',
                'step':'any',}
        self.fields['customized'].widget.attrs={
                'id':"id_customized_update",
                'class':"form-check-input",
                'name':'customized',
                }
        self.fields['price'].widget.attrs={
                'id':"id_price_update",
                'class':"form-control",
                'name':'price',
                'placeholder': 'Cena',
                'step':'any',}
        self.fields['margin'].widget.attrs={
                'id':"id_margin_update",
                'class':"form-control",
                'name':'margin',
                'placeholder': 'Margin',
                'step':'any',}

    def clean(self):
        all_clean_data= super().clean()

class NewExtraExpenseForm(forms.ModelForm):
    class Meta:
        model = ExtraExpense
        fields = ('name','description','price')
        #localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewExtraExpenseForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'new_expense_name',
                'placeholder': 'Zadejte jméno materiálu',}
        self.fields['description'].widget.attrs={
                'class':"form-control",
                'id':'new_expense_description',
                'placeholder': 'Zadejte popis výdaje',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'id':'new_expense_price',
                'placeholder': 'Zadejte cenu',
                'step':'any',}
    def clean(self):
        all_clean_data= super().clean()

class UpdateExtraExpenseForm(forms.ModelForm):
    class Meta:
        model = ExtraExpense
        fields = ('name','description','price')
        #localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateExtraExpenseForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'update_expense_name',
                'placeholder': 'Zadejte jméno materiálu',}
        self.fields['description'].widget.attrs={
                'class':"form-control",
                'id':'update_expense_description',
                'placeholder': 'Zadejte popis výdaje',}
        self.fields['price'].widget.attrs={
                'class':"form-control",
                'id':'update_expense_price',
                'placeholder': 'Zadejte cenu',
                'step':'any',}
    def clean(self):
        all_clean_data= super().clean()

class CreateMaterialTagForm(forms.ModelForm):
    class Meta:
        model = MaterialTag
        fields = ('material','tag')

    def __init__(self, user,*args, **kwargs):
        super(CreateMaterialTagForm, self).__init__(*args, **kwargs)
        self.fields['material'].widget.attrs={
                'class':"form-control",
                'name':'material',}
        self.fields['tag'].widget.attrs={
                'class':"form-control",
                'name':'tag',
                'placeholder': 'Tag'}

        if user:
            self.fields['material'].queryset = Material.objects.filter(user=user)

    def clean(self):
        all_clean_data= super().clean()

class UpdateObjectForm(forms.ModelForm):
    class Meta:
        model = Object
        fields = ('name',)
        #localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateObjectForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs={
                'class':"form-control",
                'id':'update_object_name',
                'placeholder': 'Zadejte jméno objektu',}

class CreateObjectTagForm(forms.ModelForm):
    class Meta:
        model = ObjectTag
        fields = ('object','tag')

    def __init__(self, user,*args, **kwargs):
        super(CreateObjectTagForm, self).__init__(*args, **kwargs)
        self.fields['object'].widget.attrs={
                'class':"form-control",
                'name':'material',}
        self.fields['tag'].widget.attrs={
                'class':"form-control",
                'name':'tag',
                'placeholder': 'Tag'}

        if user:
            self.fields['object'].queryset = Object.objects.filter(user=user)

    def clean(self):
        all_clean_data= super().clean()
