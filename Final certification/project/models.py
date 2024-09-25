from django.db import models

class MyUser(models.Model):
    email = models.EmailField(max_length=100)
    fam = models.CharField(max_length=50, verbose_name='Фамилия')
    name = models.CharField(max_length=50, verbose_name='Имя')
    otc = models.CharField(max_length=50, verbose_name='Отчество')
    phone = models.CharField(max_length=15, verbose_name='Телефон')

class Coords(models.Model):
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    height = models.IntegerField(null=True)

class Level(models.Model):

    level_1 = '1А'
    level_2 = '1Б'
    level_3 = '2А'
    level_4 = '2Б'
    level_5 = '3А'
    level_6 = '3Б'

    LEVEL_CHOICES = {
        (level_1, '1А'),
        (level_2, '1Б'),
        (level_3, '2А'),
        (level_4, '2Б'),
        (level_5, '3А'),
        (level_6, '3Б'),
    }

    winter = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=level_1, verbose_name='Зима')
    summer = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=level_1, verbose_name='Лето')
    autumn = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=level_1, verbose_name='Осень')
    spring = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=level_1, verbose_name='Весна')

class Pereval(models.Model):

    STATUSES = [
        ('new', 'Новое'),
        ('pen', 'На рассмотрении'),
        ('acp', 'Принято'),
        ('rej', 'Отклонено'),
    ]

    beauty_title = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=50, blank=True)
    other_titles = models.CharField(max_length=128, blank=True)
    connect = models.CharField(max_length=128, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUSES, default='new')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

class Images(models.Model):
    data = models.CharField(max_length=2000, verbose_name='Cсылка на изображение')
    title = models.TextField(verbose_name='Описание изображения')
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, verbose_name='Изображения', related_name='images')

    def __str__(self):
        return self.data, self.title