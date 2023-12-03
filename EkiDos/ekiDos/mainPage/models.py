from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

# категория с едой
class FoodCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Категория ФастФуда:')
    anchor = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='Якорь')

    def save(self, *args, **kwargs):
        if not self.anchor:
            # Используем slugify для создания якоря на основе имени
            self.anchor = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория ФастФуда"
        verbose_name_plural = 'Категории ФастФуда'


# а вот это для директорий в папках
def upload_to(instance, filename):
    now = datetime.now()
    return f'img/{now.year}/{now.month}/{now.day}/{filename}'

# сама еда
class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название Еды:")
    price = models.IntegerField(verbose_name="Цена Еды:")
    image = models.ImageField(upload_to=upload_to, null=True, verbose_name="Картинка Еды:")
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ФастФуд"
        verbose_name_plural = 'ФастФуда'


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def like_comment(self, request):
        if request.user.is_authenticated:
            self.likes += 1
            self.save()
        else:
            return HttpResponseRedirect(reverse('loginPage:loginView'))
        
    def get_absolute_url(self):
        return reverse('mainPage:chat', args=[str(self.id)])

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'
    
    class Meta:
        verbose_name = "Коменты"
        verbose_name_plural = 'Коменты'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)

    def dishes_total_price(self):
        return sum(dish.price for dish in self.dishes.all())

    def __str__(self):
        return f"Cart for {self.user.username}"

class AddProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    img = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return self.user.username

