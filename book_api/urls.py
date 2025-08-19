from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import BookViewSet, AuthorListCreateAPIView, AuthorDetailAPIView
from django.http import JsonResponse

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

def home(request):
    return JsonResponse({"message": "📚 Book API'ye hoş geldiniz!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('api/authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    path('', home),
]

