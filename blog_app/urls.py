"""
URL configuration for BLOG project.

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
from django.contrib import admin
from django.urls import path
from blog_app import views
from .views import DraftListView

urlpatterns = [
   
    path("",views.PostListView.as_view(),name="post-list"),
    path("post-detail/<int:pk>/",views.PostDetailView.as_view(),name="post-detail"),
    path("draft-list/",views.DraftListView.as_view(),name="draft-list"),
    path("draft-detail/<int:pk>/",views.DraftDetailView.as_view(),name="draft-detail"),
    path("draft-publish/<int:pk>/",views.DraftPublishView.as_view(),name="draft-publish"),
    path("post-create/",views.PostCreateView.as_view(),name="post-create"),
    path("post-update/<int:pk>/",views.PostCreateView.as_view(),name="post-update"),
    path("post-delete/<int:pk>/",views.PostDeleteView.as_view(),name="post-delete")
   
]
