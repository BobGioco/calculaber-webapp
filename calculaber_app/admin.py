from django.contrib import admin
from calculaber_app.models import Project,Material,Object,MaterialObject,ExtraExpense,MaterialTag

admin.site.register(Project)
admin.site.register(Material)
admin.site.register(Object)
admin.site.register(MaterialObject)
admin.site.register(ExtraExpense)
admin.site.register(MaterialTag)
