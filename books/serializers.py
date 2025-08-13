from rest_framework import serializers
from .models import Book, Author


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
        kitaplar = Book.objects.filter(yayinevi=yayinevi)

        if self.instance:
            kitaplar = kitaplar.exclude(id=self.instance.id)

        if kitaplar.count() >= 5:
            raise serializers.ValidationError(f"{yayinevi} yayınevinden en fazla 5 kitap olabilir.")
        return data


def to_representation(self, instance):
    return {
        'id': instance.id,
        'yayinevi': instance.yayinevi.title(),
        'tur': instance.tur.title(),
        'sayfa_sayisi': instance.sayfa_sayisi,
        'yayin_yili': instance.yayin_yili,
        'yazar': {
            'ad': instance.yazar.ad,
            'soyad': instance.yazar.soyad,
        } if instance.yazar else None
    }

#class BookSerializer(serializers.ModelSerializer):
    #yazar = AuthorSerializer(read_only=True)  #   def to_representation yerine Nested serializer daha pratik

class AuthorSerializer(serializers.ModelSerializer):
    kitap_sayisi = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'ad', 'soyad', 'yas', 'kitap_sayisi']

    def get_kitap_sayisi(self, obj):
        return obj.book_set.count()

