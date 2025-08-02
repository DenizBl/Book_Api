from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_tur(self, value):
        valid_choices = [choice[0] for choice in Book.TUR_CHOICES]
        if value not in valid_choices:
            raise serializers.ValidationError(f"Geçersiz tür. Geçerli türler: {valid_choices}")
        return value

    def validate(self, data):
        yayinevi = data.get('yayinevi')
        if self.instance:
            # Güncelleme işlemi için
            count = Book.objects.filter(yayinevi=yayinevi).exclude(id=self.instance.id).count()
        else:
            # Yeni kayıt için
            count = Book.objects.filter(yayinevi=yayinevi).count()

        if count >= 5:
            raise serializers.ValidationError(f"{yayinevi} yayınevinden en fazla 5 kitap olabilir.")
        return data
