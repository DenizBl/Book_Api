from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorNestedSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
from django.core.cache import cache


logger=logging.getLogger(__name__)        #hoca düzelttirdi bunu dikkat et 86. satırdaki logging.info-->logger.info çevrildi düzgünce import etmiştin zatten


class AuthorListCreateAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorNestedSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorNestedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class AuthorDetailAPIView(APIView):

    def get(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorNestedSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = Author.objects.filter(pk=pk).first()
        serializer = AuthorNestedSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        author = Author.objects.get(pk=pk)
        author.delete()
        return Response({})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['ad', 'yazar__ad']

    def create(self, request, *args, **kwargs):
        yayinevi = request.data.get("yayinevi")
        if not yayinevi:
            return Response({"error": "Yayınevi zorunludur"})

        cache_key = f"yayinevi_{yayinevi}_count"
        yayinevi_sayisi = cache.get(cache_key)

        if yayinevi_sayisi is None:
            # Cache’de yoksa DB’den sayıyoruzz
            yayinevi_sayisi = Book.objects.filter(yayinevi=yayinevi).count()
            cache.set(cache_key, yayinevi_sayisi, timeout=300)

        if yayinevi_sayisi >= 5:
            return Response({"error": "Bu yayınevine ait en fazla 5 kitap eklenebilir."})

        response = super().create(request, *args, **kwargs)

        cache.set(cache_key, yayinevi_sayisi + 1, timeout=300)
        return response


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        cache_key = f"book_{instance.id}_views"
        views = cache.get(cache_key, 0) + 1
        cache.set(cache_key, views, timeout=300)

        logger.info(f"{instance.ad} kitabı {views} kere görüntülendi")

        return Response({
            **serializer.data,
            "goruntulenme_sayisi": views
        })



    @action(detail=False)
    def random(self, request):
        kitap = Book.objects.order_by('?').first()
        serializer = self.get_serializer(kitap)
        return Response(serializer.data)

