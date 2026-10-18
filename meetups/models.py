from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    address = models.CharField(max_length=300, verbose_name="Адрес")

    def __str__(self):
        return f"{self.name} ({self.address})"

class Participant(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь")

    class Meta:
        verbose_name = "Участники"
        verbose_name_plural = "Участники"

    def __str__(self):
        return self.email
    
class Meetup(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True, db_index=True, verbose_name="slug")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="image", null=True, blank=True, verbose_name="Изображение")
    date = models.DateField(null=True, blank=True, verbose_name="Дата митапа")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Место")
    participants = models.ManyToManyField(Participant, blank=True, verbose_name="Участники")
    organizer_email = models.EmailField(null=True, blank=True, verbose_name="Email организатора")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Создатель")

    class Meta:
        verbose_name = "Митап"
        verbose_name_plural = "Митапы"

    def __str__(self):
        return f"{self.title} ({self.slug})"
    
