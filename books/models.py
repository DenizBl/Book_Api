from django.db import models

class Author(models.Model):
    ad = models.CharField(max_length=255)
    soyad = models.CharField(max_length=255)
    yas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ad} - {self.soyad}"

class Book(models.Model):
    TUR_CHOICES = [
        ('roman', 'Roman'),
        ('hikaye', 'Hikaye'),
        ('siir', 'Şiir'),
        ('biyografi', 'Biyografi'),
        ('felsefe', 'Felsefe'),
    ]

    ad = models.CharField(max_length=255, unique=True)
    tur = models.CharField(max_length=20, choices=TUR_CHOICES)
    sayfa_sayisi = models.PositiveIntegerField()
    yayinevi = models.CharField(max_length=255)
    yayin_yili = models.PositiveIntegerField(default=2025)
    yazar = models.ForeignKey(Author, on_delete=models.CASCADE,null=True, blank=True)
    #makemigrations hatası aldım, null=True blank=True, db oluştuktan sonra null=False yapp

    def __str__(self):
        return f"{self.ad} - {self.tur} - {self.sayfa_sayisi} - {self.yayinevi} - {self.yayin_yili}"
