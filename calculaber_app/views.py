from django.shortcuts import render
from django.views.generic import ListView,UpdateView, DeleteView
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import models,forms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,F,Case,When,DecimalField
from django.core.serializers.json import DjangoJSONEncoder
import json

def index(request):
    if request.user.is_authenticated:
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
        return render(request,'calculaber_app/project_list.html',{'form':forms.CreateProjectForm,'projects':projects})
    else:
        return render(request,'calculaber_app/index.html')

@login_required
def account_info(request):
    return render(request,'calculaber_app/new_account_info.html')

class ProjectDetailView(LoginRequiredMixin,ListView):
    context_object_name = 'project_detail'
    template_name='calculaber_app/project_detail.html'
    model=models.Object

    def calculate_object_price(self,user_id,project_id,object_id=None):
        not_customized=Sum(F('materialobject__material__price')*F('materialobject__amount'))
        customized=Sum(F('materialobject__price')*F('materialobject__amount'))
        if object_id is None:
            selected_objects=models.Object.objects.filter(user=user_id,project=project_id).select_related()
        else:
            selected_objects=models.Object.objects.filter(user=user_id,project=project_id,id=object_id).select_related()
        complete_data=selected_objects.values('id','name','create_date')

        final_set = complete_data.annotate(object_price=Case(
            When(materialobject__customized=True,then=customized),
            When(materialobject__customized=False,then=not_customized),
            default=0,
            output_field=DecimalField()
            )).order_by('name')
        return final_set

    def get_context_data(self, **kwargs):
        context = super (). get_context_data (** kwargs)
        context.update({
         'form':forms.CreateObjectForm,
         'project':models.Project.objects.filter(user=self.request.user,id=self.kwargs['pk']).values()[0],
         'form_update':forms.CreateProjectForm,
         'form_tag':forms.ObjectTagForm,
         'project_json':json.dumps(list(models.Project.objects.filter(user=self.request.user,id=self.kwargs['pk']).values()), cls=DjangoJSONEncoder),
         'extra_expense_json':json.dumps(list(models.ExtraExpense.objects.filter(user=self.request.user,project=self.kwargs['pk']).values()), cls=DjangoJSONEncoder),
         'tag_list':json.dumps(list(models.ObjectTag.objects.filter(user=self.request.user).values('object_id','tag')), cls=DjangoJSONEncoder),
         'all_objects':json.dumps(list(models.Object.objects.filter(user=self.request.user).select_related('project').values('id','name','project_id','project__name')), cls=DjangoJSONEncoder),
        })
        return context

    def get_queryset(self):
        final_set=self.calculate_object_price(self.request.user,self.kwargs['pk'])
        return json.dumps(list(final_set.values('id','name','create_date','object_price')), cls=DjangoJSONEncoder)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('type')=="new":
                instance = models.Object()
                instance.name=request.POST.get("name")
                instance.project_id=request.POST.get("project")
                instance.user=request.user
                instance.save()

                for tag in request.POST.getlist('tags[]'):
                    tag_instance = models.ObjectTag()
                    tag_instance.object=instance
                    tag_instance.user=self.request.user
                    tag_instance.tag=tag
                    tag_instance.save()

                return JsonResponse(data={
                                "id":instance.id,
                                'name':instance.name,
                                'create_date':instance.create_date,
                                'tag_list':json.dumps(list(models.ObjectTag.objects.filter(object_id=instance.id,user=self.request.user).values('object_id','tag')), cls=DjangoJSONEncoder),
                                },status=200)

            elif request.POST.get('type')=="duplicate":
                instance=models.Object.objects.get(id=request.POST.get("id"))
                instance.pk=None
                instance.project_id=request.POST.get("project")
                instance.save()

                for tag in list(models.ObjectTag.objects.filter(object_id=request.POST.get("id"),user=self.request.user).values('tag')):
                    tag_instance = models.ObjectTag()
                    tag_instance.object=instance
                    tag_instance.user=self.request.user
                    tag_instance.tag=tag['tag']
                    tag_instance.save()

                for item in models.MaterialObject.objects.filter(object_id=request.POST.get("id")):
                    new_item=models.MaterialObject()
                    new_item.material=item.material
                    new_item.object=instance
                    new_item.name=item.name
                    new_item.amount=item.amount
                    new_item.user=request.user
                    new_item.save()

                duplicated_object=self.calculate_object_price(self.request.user,request.POST.get("project"),instance.id)
                return JsonResponse(data={
                                "object":json.dumps(list(duplicated_object.values('id','name','create_date','object_price')), cls=DjangoJSONEncoder),
                                'tag_list':json.dumps(list(models.ObjectTag.objects.filter(object_id=instance.id,user=self.request.user).values('object_id','tag')), cls=DjangoJSONEncoder),
                                },status=200)

        else:
            if "update_project_sub" in request.POST:
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
        material=models.Material.objects.filter(user=self.request.user).values('id','name','margin','price','units')

        context.update({
         'form':forms.CreateMaterialForm,
         'form_update':forms.UpdateMaterialForm,
         'tag_form':forms.MaterialTagForm,
         'units_list':json.dumps([choice[1] for choice in models.Material._meta.get_field('units').choices], cls=DjangoJSONEncoder),
         'tag_list':json.dumps(list(models.MaterialTag.objects.filter(user=self.request.user).values('material_id','tag')), cls=DjangoJSONEncoder),
         'material_list':json.dumps(list(material), cls=DjangoJSONEncoder)
         })
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('type')=="delete":
                instance = models.Material.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.delete()
                return JsonResponse(data={"delete":request.POST['item_id']},status=200)

            elif request.POST.get('type')=="update":
                instance = models.Material.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.name=request.POST.get("name")
                instance.margin=request.POST.get("margin")
                instance.price=request.POST.get("price")
                instance.units=request.POST.get("units")
                instance.save()

                tags=list(models.MaterialTag.objects.filter(user=self.request.user,material_id=request.POST.get('item_id')).values('tag'))
                tags_lst=set([tag['tag'] for tag in tags])
                tags_lst_POST=set(request.POST.getlist('tags[]'))

                if tags_lst!=tags_lst_POST:
                    for tag_delete in (tags_lst-tags_lst_POST):
                        tag_instance = models.MaterialTag.objects.get(material_id=request.POST.get('item_id'),user=self.request.user,tag=tag_delete)
                        tag_instance.delete()

                    for tag in (tags_lst_POST-tags_lst):
                        tag_instance = models.MaterialTag()
                        tag_instance.material_id=request.POST.get('item_id')
                        tag_instance.user=self.request.user
                        tag_instance.tag=tag
                        tag_instance.save()

                return JsonResponse(data={
                                "id":instance.id,
                                'name':instance.name,
                                'price':instance.price,
                                'margin':instance.margin,
                                'units':instance.units,
                                'tag_list':json.dumps(list(models.MaterialTag.objects.filter(material_id=instance.id,user=self.request.user).values('material_id','tag')), cls=DjangoJSONEncoder),

                                },status=200)
            elif request.POST.get('type')=="new":
                instance = models.Material()
                instance.name=request.POST.get("name")
                instance.margin=request.POST.get("margin")
                instance.price=request.POST.get("price")
                instance.units=request.POST.get("units")
                instance.user=request.user
                instance.save()
                for tag in request.POST.getlist('tags[]'):
                    tag_instance = models.MaterialTag()
                    tag_instance.material_id=instance.id
                    tag_instance.user=self.request.user
                    tag_instance.tag=tag
                    tag_instance.save()
                return JsonResponse(data={
                                "id":instance.id,
                                'name':instance.name,
                                'price':instance.price,
                                'margin':instance.margin,
                                'units':instance.units,
                                'tag_list':json.dumps(list(models.MaterialTag.objects.filter(material_id=instance.id,user=self.request.user).values('material_id','tag')), cls=DjangoJSONEncoder),

                                },status=200)

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
            #'material_object': models.MaterialObject.objects.filter(object=self.kwargs['pk2']).select_related().order_by('name'),
            'object_info': models.Object.objects.filter(user=self.request.user,id=self.kwargs['pk2']).values('id','user_id','project_id','name','create_date','project__name')[0],
            'form':forms.CreateMaterialObjectForm(user=self.request.user.id),
            'tag_form':forms.ObjectTagForm,
            'update_object_form':forms.UpdateObjectForm,
            'update_form':forms.UpdateMaterialObjectForm(user=self.request.user.id),
            'material_object_json': json.dumps(list(models.MaterialObject.objects.filter(object=self.kwargs['pk2']).select_related().order_by('name').values('id','name','material_id','object_id','amount','price','margin','customized','material__name','material__price','material__margin','material__units')), cls=DjangoJSONEncoder),
            'material_tags_json': json.dumps(list(models.MaterialTag.objects.filter(user=self.request.user).values('material_id','tag')), cls=DjangoJSONEncoder),
            'object_tags_json': json.dumps(list(models.ObjectTag.objects.filter(user=self.request.user,object=self.kwargs['pk2']).values('object_id','tag')), cls=DjangoJSONEncoder),
            'material_json': json.dumps(list(models.Material.objects.filter(user=self.request.user).values('id','name','margin','price','units')), cls=DjangoJSONEncoder),
            'units_list':json.dumps([choice[1] for choice in models.Material._meta.get_field('units').choices], cls=DjangoJSONEncoder),
            'object_info_json': json.dumps(models.Object.objects.filter(user=self.request.user,id=self.kwargs['pk2']).values()[0], cls=DjangoJSONEncoder),
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('type')=="delete":
                instance = models.MaterialObject.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.delete()

                return JsonResponse(data={"delete":request.POST['item_id']},status=200)

            elif request.POST.get('type')=="new":
                instance = models.MaterialObject()
                instance.name=request.POST.get('name')
                instance.amount=request.POST.get('amount')
                instance.material_id=request.POST.get('material_id')
                instance.object_id=request.POST.get('object_id')
                instance.project_id=models.Object.objects.get(id=request.POST.get('object_id'),user=self.request.user).project_id
                instance.user=request.user
                instance.save()

                return JsonResponse(data={
                                        'amount':instance.amount,
                                        'customized':instance.customized,
                                        'id':instance.id,
                                        'margin':instance.margin,
                                        'material__margin':instance.material.margin,
                                        'material__name':instance.material.name,
                                        'material__price':instance.material.price,
                                        'material__units':instance.material.units,
                                        'material_id':instance.material_id,
                                        'name':instance.name,
                                        'object_id':instance.object_id,
                                        'price':instance.price,
                                        'total_price':float(instance.amount)*(float(instance.material.price)*((100+float(instance.material.margin))/100))},status=200)

            elif request.POST.get('type')=="update":
                instance = models.MaterialObject.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.name=request.POST.get('name')
                instance.amount=request.POST.get('amount')

                if request.POST.get('customized')=='true' and request.POST.get('price').isnumeric() and request.POST.get('margin').isnumeric():
                    instance.customized=True
                    instance.price=request.POST.get('price')
                    instance.margin=request.POST.get('margin')
                    _=float(instance.amount)*(float(instance.price)*((100+float(instance.margin))/100))
                else:
                    instance.customized=False
                    instance.price=None
                    instance.margin=None
                    _=float(instance.amount)*(float(instance.material.price)*((100+float(instance.material.margin))/100))
                instance.save()

                return JsonResponse(data={
                                        'amount':instance.amount,
                                        'customized':instance.customized,
                                        'id':instance.id,
                                        'margin':instance.margin,
                                        'material__margin':instance.material.margin,
                                        'material__name':instance.material.name,
                                        'material__price':instance.material.price,
                                        'material__units':instance.material.units,
                                        'material_id':instance.material_id,
                                        'name':instance.name,
                                        'object_id':instance.object_id,
                                        'price':instance.price,
                                        'total_price':_},status=200)

            elif request.POST.get('type')=='update_object':
                instance = models.Object.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.name=request.POST.get('name')
                instance.save()

                tags=list(models.ObjectTag.objects.filter(user=self.request.user,object_id=request.POST.get('item_id')).values('tag'))
                tags_lst=set([tag['tag'] for tag in tags])
                tags_lst_POST=set(request.POST.getlist('tags[]'))

                if tags_lst!=tags_lst_POST:
                    for tag_delete in (tags_lst-tags_lst_POST):
                        tag_instance = models.ObjectTag.objects.get(object_id=request.POST.get('item_id'),user=self.request.user,tag=tag_delete)
                        tag_instance.delete()

                    for tag in (tags_lst_POST-tags_lst):
                        tag_instance = models.ObjectTag()
                        tag_instance.object_id=request.POST.get('item_id')
                        tag_instance.user=self.request.user
                        tag_instance.tag=tag
                        tag_instance.save()

                return JsonResponse(data={
                                "id":instance.id,
                                'name':instance.name,
                                'tag_list':json.dumps(list(models.ObjectTag.objects.filter(object_id=instance.id,user=self.request.user).values('object_id','tag')), cls=DjangoJSONEncoder),
                                },status=200)

class ObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.Object

    def get_success_url(self,**kwargs):
        return reverse_lazy('project_detail',kwargs = {'pk': self.get_object().project.id})

class MaterialObjectDeleteView(LoginRequiredMixin,DeleteView):
    model=models.MaterialObject

    def get_success_url(self,**kwargs):
        pk1=models.Object.objects.filter(id=self.get_object().object.id).values()[0]['project_id']
        pk2=self.get_object().object.id
        return reverse_lazy('object_detail',kwargs = {'pk1': pk1, 'pk2': pk2})


class ExtraExpenseDetailView(LoginRequiredMixin,ListView):
    template_name = 'calculaber_app/extra_expense_detail.html'
    context_object_name = 'extra_expense_detail'
    model = models.ExtraExpense

    def get_context_data(self, **kwargs):
        context = super (). get_context_data (** kwargs)
        extra_expense=models.ExtraExpense.objects.filter(user=self.request.user,project=self.kwargs['pk']).order_by('name')
        extra_expense_total_price=extra_expense.aggregate(Sum('price'))['price__sum']
        print(models.Project.objects.get(user=self.request.user,id=self.kwargs['pk']))
        context.update({
            'project':models.Project.objects.get(user=self.request.user,id=self.kwargs['pk']),
            'create_form':forms.NewExtraExpenseForm(),
            'update_form':forms.UpdateExtraExpenseForm(),
            'total_price':extra_expense_total_price if not extra_expense_total_price is None else 0,
            'extra_expense_json':json.dumps(list(models.ExtraExpense.objects.filter(user=self.request.user,project=self.kwargs['pk']).values('id','name','description','price')), cls=DjangoJSONEncoder),
        })
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST.get('type')=="delete":
                instance = models.ExtraExpense.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.delete()

                return JsonResponse(data={"delete":request.POST['item_id']},status=200)

            elif request.POST.get('type')=="new":
                instance = models.ExtraExpense()
                instance.name=request.POST['name']
                instance.description=request.POST['description']
                instance.price=request.POST['price']
                instance.project_id=request.POST['project_id']
                instance.user=self.request.user
                instance.save()

                return JsonResponse(data={
                                "id":instance.id,
                                "name":instance.name,
                                "description":instance.description,
                                "price":instance.price
                                },status=200)

            elif request.POST.get('type')=="update":
                instance = models.ExtraExpense.objects.get(id=request.POST.get('item_id'),user=self.request.user)
                instance.name=request.POST['name']
                instance.description=request.POST['description']
                instance.price=request.POST['price']
                instance.save()
                return JsonResponse(data={
                                "id":instance.id,
                                "name":instance.name,
                                "description":instance.description,
                                "price":instance.price
                                },status=200)

class ExtraExpenseDeleteView(LoginRequiredMixin,DeleteView):
    model=models.ExtraExpense

    def get_success_url(self,**kwargs):
        return reverse_lazy('extra_expense_detail',kwargs = {'pk': self.get_object().project.id})
