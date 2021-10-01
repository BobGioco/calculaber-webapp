from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#import uuid

class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    create_date=models.DateTimeField(default=timezone.now)
    project_pic=models.ImageField(upload_to='project_pics',blank=True)
    def __str__(self):
        return f"{self.name}"

class Material(models.Model):
    class UnitsChoice(models.TextChoices):
        setup_0 = '0', "m2"
        setup_1 = '1', "kus"
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    margin=models.DecimalField(default=0,blank=False, max_digits=3, decimal_places=2)
    price=models.DecimalField(default=0,blank=False, decimal_places=2,max_digits=65)
    create_date=models.DateTimeField(default=timezone.now)
    units = models.CharField(
        max_length=2,
        choices=UnitsChoice.choices,
        default=UnitsChoice.setup_0)

    def __str__(self):
        return f"{self.name} - {self.price} czk ({self.get_units_display()})"

class Object(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    create_date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.project.name}"

class MaterialObject(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    object=models.ForeignKey(Object,on_delete=models.CASCADE)
    material=models.ForeignKey(Material,on_delete=models.CASCADE)
    name=models.CharField(max_length=128)
    amount=models.DecimalField(default=0,blank=False, decimal_places=2,max_digits=65)
    create_date=models.DateTimeField(default=timezone.now,blank=True)

    customized=models.BooleanField(default=False)
    margin=models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=2)
    price=models.DecimalField(blank=True, null=True, decimal_places=2,max_digits=65)

    def __str__(self):
        return f"{self.name} - {self.amount} {self.material.get_units_display()}"
