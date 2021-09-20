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
        if user:
            self.fields['material'].queryset = Material.objects.filter(user=user)
    def clean(self):
        all_clean_data= super().clean()
