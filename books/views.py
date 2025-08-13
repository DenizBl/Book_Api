from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['ad', 'yazar__ad']  # Kitap ve yazar isimlerine göre arama yapmayı sağlayan filter

    @action(detail=False)
    def random(self, request):
        kitap = Book.objects.order_by('?').first()
        serializer = self.get_serializer(kitap)
        return Response(serializer.data)
