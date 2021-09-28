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
        })
        return context

    def get_queryset(self):
        return models.Material.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        #print(request.path_info)
        #print(request)
        material_form=forms.CreateMaterialForm(request.POST)
        if material_form.is_valid():
            #print(object_form)
            obj = models.Material()
            obj.name=material_form.cleaned_data.get("name")
            obj.margin=material_form.cleaned_data.get("margin")
            obj.price=material_form.cleaned_data.get("price")
            obj.units=material_form.cleaned_data.get("units")
            obj.project=material_form.cleaned_data.get("project")
            obj.user=request.user
            obj.save()

        return HttpResponseRedirect(request.path_info)

class MaterialUpdateView(LoginRequiredMixin,UpdateView):
    success_url= reverse_lazy('calculaber_app:material_list')
    model=models.Material
    fields = ['name','margin','price','units'] #['name','sensor_type','sensor_ID']
    template_name_suffix = '_update_form'

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

        })
        print(context)
        return context

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
            obj = models.MaterialObject.objects.get(id=request.POST.get('materialobject_pk'))
            obj.name=request.POST.get('materiaobject_name')
            obj.amount=request.POST.get('materiaobject_amount')
            obj.save()
            #print(request.POST)

        return HttpResponseRedirect(request.path_info)

class ObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Object

    def get_success_url(self,**kwargs):
        return reverse_lazy('project_detail',kwargs = {'pk': self.get_object().project.id})

class ObjectUpdateView(LoginRequiredMixin,UpdateView):
    #success_url= reverse_lazy('calculaber_app:material_list')
    model=models.Object
    fields = ['name','project',] #['name','sensor_type','sensor_ID']
    template_name_suffix = '_update_form'

    def get_success_url(self,**kwargs):
        pk2=self.get_object().id
        pk1=models.Object.objects.filter(id=pk2).values()[0]['project_id']
        return reverse_lazy('object_detail',kwargs = {'pk1': pk1, 'pk2': pk2})

class ProjectUpdateView(LoginRequiredMixin,UpdateView):
    model=models.Project
    fields = ['name','project_pic',] #['name','sensor_type','sensor_ID']
    template_name_suffix = '_update_form'

    def get_success_url(self,**kwargs):
        pk=self.get_object().id
        return reverse_lazy('project_detail',kwargs = {'pk': pk})

class MaterialObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.MaterialObject
    #success_url= reverse_lazy('calculaber_app:index')

    def get_success_url(self,**kwargs):
        pk1=models.Object.objects.filter(id=self.get_object().object.id).values()[0]['project_id']
        pk2=self.get_object().object.id
        return reverse_lazy('object_detail',kwargs = {'pk1': pk1, 'pk2': pk2})
