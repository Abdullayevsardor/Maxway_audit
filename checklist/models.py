from django.db import models
from django.contrib.auth.models import User
from django.db import models
import uuid
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile





def audit_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f"audit_images/{uuid.uuid4().hex}.{ext}"
 
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    text = models.CharField(max_length=500)

    def __str__(self):
        return self.text

from django.contrib.auth.hashers import make_password, check_password

class Branch(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    pin = models.CharField(max_length=128, null=True, blank=True)  # HASH saqlanadi
    is_active = models.BooleanField(default=True)

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def __str__(self):
        return self.name

   

class Score(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("branch", "item")

    def __str__(self):
        return f"{self.branch} - {self.item} = {self.score}"




    
class Audit(models.Model):
    """Asosiy Audit yozuvi (Filial va umumiy foiz)."""
   
    auditor = models.CharField(max_length=150, blank=True, null=True)

    filial_nomi = models.CharField(max_length=255, verbose_name="Filial Nomi")
    total_percentage = models.FloatField(null=True, blank=True, verbose_name="Umumiy Foiz")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan Vaqti")
    
    
    def __str__(self):
        return f"{self.filial_nomi} - {self.total_percentage}%"

    

class AuditDetail(models.Model):
    """Har bir band uchun ball va rasm ma'lumotlari."""
    
    audit = models.ForeignKey(Audit, on_delete=models.CASCADE, related_name='details', verbose_name="Audit")
    band_id = models.CharField(max_length=255, verbose_name="Band IDsi (Savol)") # Masalan: '01', '02', '03'
    score = models.IntegerField(verbose_name="Kiritilgan Ball (0-3)")
    image = models.ImageField(
            upload_to=audit_image_path,
            null=True,
            blank=True
        )  
    
    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            # RGB ga o‘tkazamiz (PNG/JPEG muammosiz bo‘lsin)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # MAX o‘lcham (masalan 1280x1280)
            img.thumbnail((1280, 1280))

            buffer = BytesIO()
            img.save(
                buffer,
                format="JPEG",
                quality=70,      # 👈 ASOSIY SIQISH
                optimize=True
            )

            self.image.save(
                self.image.name,
                ContentFile(buffer.getvalue()),
                save=False
            )

        super().save(*args, **kwargs)


    
    def __str__(self):
        return f"{self.audit.filial_nomi} - Band {self.band_id}: {self.score} ball"
    
    class Meta:
        verbose_name = "2. Audit Detali (Savollar)"
        verbose_name_plural = "2. Audit Detallari"
        unique_together = ('audit', 'band_id') # Bir auditda bir band bir marta bo'lishi kerak



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=(('worker', 'Worker'),),
        default='worker'
    )

    def __str__(self):
        return self.user.username
