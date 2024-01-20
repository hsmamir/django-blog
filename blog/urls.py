from django.urls import path
from .views import BlogListAPIView, BlogDetailAPIView

urlpatterns = [
    path('blog/', BlogListAPIView.as_view()),
    path('blog/<int:pk>/', BlogDetailAPIView.as_view()),
]
