from django.urls import path
from resources import views

urlpatterns = [
    path('',views.index_page),
    path('files' ,views.upload_resource),
    path("all_files" , views.Files),
    path("update/<str:fileid>/<str:DecriptionToken>" , views.FileUpdate),
    path("details/<str:fileid>" , views.FileDetails),


]