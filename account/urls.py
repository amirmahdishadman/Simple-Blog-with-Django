from django.urls import path
from .views import home,ArticleList,ArticlCreate,ArticlUpdate,ArticleDelete,Profile

app_name="account"

urlpatterns = [
   path('',ArticleList.as_view(),name='home'),
   path('article/create',ArticlCreate.as_view(),name='article-create'),
   path('article/update/<int:pk>',ArticlUpdate.as_view(),name='article-update'),
   path('article/delete/<int:pk>',ArticleDelete.as_view(),name='article-delete'),
   path('profile/',Profile.as_view(),name='profile'),


]


   #  path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
   #  path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   #  path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   #  path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),