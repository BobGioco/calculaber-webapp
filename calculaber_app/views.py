from django.shortcuts import render
from django.views.generic import ListView,UpdateView, DeleteView #,FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models,forms
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method=="POST":
        project_form=forms.CreateProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            obj = models.Project()
            obj.name=project_form.cleaned_data.get("name")
            obj.project_pic=project_form.cleaned_data.get("project_pic")
            obj.user_id=request.user.id
            obj.save()

            return HttpResponseRedirect(request.path_info)

    projects=models.Project.objects.filter(user=request.user.id)
    return render(request,'calculaber_app/index.html',{'form':forms.CreateProjectForm,'projects':projects})

@login_required
def account_info(request):
    return render(request,'calculaber_app/new_account_info.html')

class ProjectDetailView(LoginRequiredMixin,ListView):
    context_object_name = 'project_detail'
    template_name='calculaber_app/project_detail.html'
    model=models.Object

    def get_context_data(self, **kwargs):
        context = super (). get_context_data (** kwargs)
        context.update({
         'form':forms.CreateObjectForm,
         'project':models.Project.objects.filter(user=self.request.user,id=self.kwargs['pk']).values()[0],
         'list_all': models.Object.objects.filter(user=self.request.user).select_related('project'),
         'form_update':forms.CreateProjectForm,
        })
        return context

    def get_queryset(self):
        return models.Object.objects.filter(user=self.request.user,project=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        if "new_object_sub" in request.POST:
            object_form=forms.CreateObjectForm(request.POST)
            if object_form.is_valid():
                obj = models.Object()
                obj.name=object_form.cleaned_data.get("name")
                obj.project_id=kwargs['pk']
                obj.user=request.user
                obj.save()
        elif "duplicate_sub" in request.POST:
            print(request.POST)
            obj = models.Object()
            obj.name=models.Object.objects.get(id=request.POST.get('select_object')).name
            obj.project_id=kwargs['pk']
            obj.user=request.user
            obj.save()

            material_object_lst=models.MaterialObject.objects.filter(object=request.POST.get('select_object'))
            for item in material_object_lst:
                new_item=models.MaterialObject()
                new_item.material=item.material
                new_item.object=obj
                new_item.name=item.name
                new_item.amount=item.amount
                new_item.user=request.user
                new_item.save()
        elif "update_project_sub" in request.POST:
            print(request.POST)
            print(request.FILES)
            object_form=forms.CreateProjectForm(request.POST, request.FILES)
            if object_form.is_valid():
                obj=models.Project.objects.get(id=self.kwargs['pk'])
                obj.name=object_form.cleaned_data.get("name")
                if not object_form.cleaned_data.get("project_pic") is None:
                    obj.project_pic=object_form.cleaned_data.get("project_pic")
                obj.save()

        return HttpResponseRedirect(request.path_info)

class ProjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Project
    success_url=reverse_lazy('calculaber_app:index')

class MaterialListView(LoginRequiredMixin,ListView):
    context_object_name = 'material_list'
    template_name='calculaber_app/material_list.html'
    model=models.Material

    def get_context_data(self, **kwargs):
        context = super (). get_context_data (** kwargs)
        context.update({
         'form':forms.CreateMaterialForm,
         'form_update':forms.UpdateMaterialForm,
        })
        return context

    def get_queryset(self):
        return models.Material.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        #print(request.path_info)
        #print(request)
        if "new_material_sub" in request.POST:
            material_form=forms.CreateMaterialForm(request.POST)
            if material_form.is_valid():
                obj = models.Material()
                obj.name=material_form.cleaned_data.get("name")
                obj.margin=material_form.cleaned_data.get("margin")
                obj.price=material_form.cleaned_data.get("price")
                obj.units=material_form.cleaned_data.get("units")
                obj.project=material_form.cleaned_data.get("project")
                obj.user=request.user
                obj.save()
        elif "update_material_sub" in request.POST:
            material_form=forms.UpdateMaterialForm(request.POST)
            if material_form.is_valid():
                print(material_form)
                obj = models.Material.objects.get(id=request.POST.get('id'),user=self.request.user)
                obj.name=material_form.cleaned_data.get("name")
                obj.margin=material_form.cleaned_data.get("margin")
                obj.price=material_form.cleaned_data.get("price")
                obj.units=material_form.cleaned_data.get("units")
                obj.project=material_form.cleaned_data.get("project")
                obj.user=request.user
                obj.save()

        return HttpResponseRedirect(request.path_info)

class MaterialDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Material
    success_url= reverse_lazy('calculaber_app:material_list')

class ObjectDetailView(LoginRequiredMixin,ListView):
    template_name = 'calculaber_app/object_detail.html'
    context_object_name = 'object_detail'
    model = models.MaterialObject

    def get_context_data(self, **kwargs):
        context = super (). get_context_data (** kwargs)
        context.update({
            'material_object': models.MaterialObject.objects.filter(object=self.kwargs['pk2']).select_related().order_by('name'),
            'object_info': models.Object.objects.filter(user=self.request.user,id=self.kwargs['pk2']).values()[0],
            'form':forms.CreateMaterialObjectForm(user=self.request.user.id),
            'update_form':forms.UpdateMaterialObjectForm(user=self.request.user.id),
            'total_price':self.calculate_total(models.MaterialObject.objects.filter(object=self.kwargs['pk2']).select_related().order_by('name')),
        })
        #print(context)
        return context
    def calculate_total(self,model):
        total=0
        for item in model:
            if item.customized==True:
                temp=item.amount*(item.price*(item.margin/100))
            else:
                temp=item.amount*(item.material.price*(item.material.margin/100))
            total=total+temp
        return str(round(total,2))


    def post(self, request, *args, **kwargs):
        #print(request.path_info)
        #print(request)
        if "new_material_object_sub" in request.POST:
            materialobject_form=forms.CreateMaterialObjectForm(data=request.POST,user=request.user.id)
            print(materialobject_form)
            if materialobject_form.is_valid():
                #print(object_form)
                obj = models.MaterialObject()
                obj.name=materialobject_form.cleaned_data.get("name")
                obj.amount=materialobject_form.cleaned_data.get("amount")
                obj.material=materialobject_form.cleaned_data.get("material")
                obj.object_id=self.kwargs['pk2']
                obj.project_id=self.kwargs['pk1']
                obj.user=request.user
                obj.save()
        elif "update_material_object_sub" in request.POST:
            print(request.POST)
            obj = models.MaterialObject.objects.get(id=request.POST.get('id'),user=self.request.user)
            obj.name=request.POST.get('name')
            obj.amount=request.POST.get('amount')
            if request.POST.get('customized', False):
                obj.customized=True
                obj.price=request.POST.get('price')
                obj.margin=request.POST.get('margin')
            else:
                obj.customized=False
                obj.price=None
                obj.margin=None
            obj.save()
        elif "update_object_sub" in request.POST:
            obj = models.Object.objects.get(id=request.POST.get('object_id'),user=self.request.user)
            obj.name=request.POST.get('object_name')
            obj.save()
            #print(request.POST)

        return HttpResponseRedirect(request.path_info)

class ObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Object

    def get_success_url(self,**kwargs):
        return reverse_lazy('project_detail',kwargs = {'pk': self.get_object().project.id})

class MaterialObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.MaterialObject
    #success_url= reverse_lazy('calculaber_app:index')

    def get_success_url(self,**kwargs):
        pk1=models.Object.objects.filter(id=self.get_object().object.id).values()[0]['project_id']
        pk2=self.get_object().object.id
        return reverse_lazy('object_detail',kwargs = {'pk1': pk1, 'pk2': pk2})
