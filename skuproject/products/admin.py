from django.contrib import admin
from .models import UploadedBaseInfo, Season, Capsule, SKU, Size

class SKUAdmin(admin.ModelAdmin):
    search_fields = ['sku_firstletters']


admin.site.register(UploadedBaseInfo)
admin.site.register(Season)
admin.site.register(Capsule)
admin.site.register(SKU, SKUAdmin)
admin.site.register(Size)

