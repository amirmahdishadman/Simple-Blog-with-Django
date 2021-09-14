"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path,re_path
from account.views import Login,Signup,activate,active_later
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('signup/',Signup.as_view(),name="signup"),
    path('activate/<slug:uidb64>/<slug:token>',activate,name="activate"),
    path('activate_account/',active_later,name="activate_later"),
    # re_path(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('admin/', admin.site.urls),
    path('',include('blog.urls')),
    path('',include('django.contrib.auth.urls')),
    path('account/',include('account.urls')),
    path('comment/', include('comment.urls')),
]



from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
