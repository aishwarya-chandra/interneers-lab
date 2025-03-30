"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .controllers.product_controller import ProductController  # Import from controller layer
from .controllers.product_category_controller import ProductCategoryController

urlpatterns = [
    path('products/', ProductController.as_view(), name='product_list'),                    
    path('products/<str:product_id>/', ProductController.as_view(), name='product_detail'),  # Use str for MongoDB ObjectId
    path('categories/', ProductCategoryController.as_view(), name='category_list'),  
    path('categories/<str:category_id>/', ProductCategoryController.as_view(), name='category_detail'),
]
