from django.contrib import admin
from .models import UploadedBaseInfo, Season, Capsule, SKU, Size

admin.site.register(UploadedBaseInfo)
admin.site.register(Season)
admin.site.register(Capsule)
admin.site.register(SKU)
admin.site.register(Size)