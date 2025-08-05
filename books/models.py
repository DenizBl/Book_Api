from django.db import models

class Book(models.Model):
    TUR_CHOICES = [
        ('roman', 'Roman'),
        ('hikaye', 'Hikaye'),
        ('siir', 'Şiir'),
        ('biyografi', 'Biyografi'),
        ('felsefe', 'Felsefe'),
    ]

    ad = models.CharField(max_length=255, unique=True)
    tur = models.CharField(max_length=20)
    sayfa_sayisi = models.PositiveIntegerField()
    yayinevi = models.CharField(max_length=255)

    def __str__(self):
        return self.ad
