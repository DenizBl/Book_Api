from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author
from .serializers import BookSerializer, AuthorNestedSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

class AuthorListCreateAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class AuthorDetailAPIView(APIView):

    def get(self, request, pk):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk):
        author = Author.objects.filter(pk=pk).first()
        serializer = AuthorSerializer(author, data=request.data)
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

    @action(detail=False)
    def random(self, request):
        kitap = Book.objects.order_by('?').first()
        serializer = self.get_serializer(kitap)
        return Response(serializer.data)
