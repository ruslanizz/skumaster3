from django.contrib import admin
from .models import UploadedBaseInfo, Season, Capsule, SKU, Size


class UploadedBaseInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'period', 'upload_date']
    search_fields = ['user']

class SeasonAdmin(admin.ModelAdmin):
    list_display = ['season_firstletters', 'name', 'user']
    search_fields = ['season_firstletters']

class CapsuleAdmin(admin.ModelAdmin):
    list_display = ['capsule_firstletters', 'name', 'user']
    search_fields = ['capsule_firstletters']

class SKUAdmin(admin.ModelAdmin):
    list_display = ['sku_firstletters', 'name', 'user']
    search_fields = ['sku_firstletters']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['sku_full', 'quantity_sold','quantity_instock','quantity_onway', 'user']
    search_fields = ['sku_full']


admin.site.register(UploadedBaseInfo, UploadedBaseInfoAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Capsule, CapsuleAdmin)
admin.site.register(SKU, SKUAdmin)
admin.site.register(Size, SizeAdmin)

