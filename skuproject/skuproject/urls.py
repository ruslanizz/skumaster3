"""skuproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from products.views import *

router = SimpleRouter()
router.register('api/seasons', SeasonsView, basename='seasons')
router.register('api/baseinfo', UploadedBaseInfoView)
router.register('api/capsules', CapsulesView, basename='capsules')
router.register('api/sku', SkuView, basename='sku')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('demo/', demo_index_page),
    path('open/', upload_file),
    path('onway/', onway_page),
    path('sku/', sku_page),
    path('capsules/', capsules_page),
    path('accounts/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls'))

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+= router.urls
