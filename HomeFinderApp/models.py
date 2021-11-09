from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=225, null=True)
    phone = models.CharField(max_length=10, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=150, null=True)
    verify = models.BooleanField(default=False)

    def _str_(self):
        return self.username

    class Meta:
        db_table = "Account"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    property_id = models.CharField(max_length=15, null=True)
    location = models.CharField(max_length=100, null=True)
    add1 = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=100, null=True)
    property_type = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    area = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    beds = models.CharField(max_length=100, null=True)
    parking = models.CharField(max_length=100, null=True)
    property_des = models.CharField(max_length=255, null=True)
    imagefile = models.FileField(upload_to="Images", null=True, blank=True)
    videofile = models.FileField(upload_to="Videos", null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    mobile_no = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=100, null=True)
    owner_des = models.CharField(max_length=255, null=True)
    owner_imagefile = models.FileField(upload_to="ProfileImages", null=True, blank=True)
    balcony = models.CharField(max_length=5, null=True, blank=True)
    security = models.CharField(max_length=5, null=True, blank=True)
    tv = models.CharField(max_length=5, null=True, blank=True)
    refrigerator = models.CharField(max_length=5, null=True, blank=True)
    modular_kitchen = models.CharField(max_length=5, null=True, blank=True)
    parking_area = models.CharField(max_length=5, null=True, blank=True)
    power_backup = models.CharField(max_length=5, null=True, blank=True)
    ac = models.CharField(max_length=5, null=True, blank=True)
    fit = models.CharField(max_length=5, null=True, blank=True)
    kids_area = models.CharField(max_length=5, null=True, blank=True)
    water = models.CharField(max_length=5, null=True, blank=True)
    bike = models.CharField(max_length=5, null=True, blank=True)


    class Meta:
        db_table = "Post"

class PostImages(models.Model):
    imagefile = models.FileField(upload_to="Images", null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "PostImages"
