from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import BookViewSet, AuthorListCreateAPIView, AuthorDetailAPIView

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors/', AuthorListCreateAPIView.as_view(), name='author-list-create'),
    path('api/authors/<int:pk>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('api/', include(router.urls)),
]
