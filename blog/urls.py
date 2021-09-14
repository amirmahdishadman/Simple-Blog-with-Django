from django.urls import path
from .views import Articlelist,ArticleDetail,Categorylist,Authorlist,ArticlePreview,Searchlist

app_name='blog'
urlpatterns = [
    path('',Articlelist.as_view() , name='home'),
    path('page/<int:page>',Articlelist.as_view() , name='home'),
    path('article/<slug:slug>',ArticleDetail.as_view(),name='detail'),
    path('preview/<int:pk>',ArticlePreview.as_view(),name='preview'),
    path('category/<slug:slug>/page/<int:page>',Categorylist.as_view(),name='category'),
    path('category/<slug:slug>',Categorylist.as_view(),name='category'),
    path('author/<slug:username>/page/<int:page>',Authorlist.as_view(),name='author'),
    path('author/<slug:username>',Authorlist.as_view(),name='author'),
    path('search/page/<int:page>',Searchlist.as_view(),name='search'),
    path('search/',Searchlist.as_view(),name='search'),

]



