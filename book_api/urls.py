from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import BookViewSet, AuthorViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
