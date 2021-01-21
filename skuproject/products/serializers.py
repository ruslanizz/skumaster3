
from rest_framework.serializers import ModelSerializer
from products.models import Season, UploadedBaseInfo, Capsule, SKU


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = ['name',
                  'id',
                  'img',
                  'season_firstletters',
                  'user',
                  'capsules_quantity',
                  'capsules_sellsumm_sold',
                  'capsules_income'
                  ]


class CapsuleSerializer(ModelSerializer):
    class Meta:
        model = Capsule
        fields = ['name',
                  'id',
                  'season',
                  'img',
                  'capsule_firstletters',
                  'user',
                  'sku_quantity',
                  'sku_sellsumm_sold',
                  'sku_costsumm_instock',
                  'sku_income',
                  'sku_margin_percent',
                  'get_season_name',
                  'sold_sizes_forchart'
                          ]


class UploadedBaseInfoSerializer(ModelSerializer):
    class Meta:
        model = UploadedBaseInfo
        fields = ['period',
                  'upload_date',
                  'user']


class SkuSerializer(ModelSerializer):

    class Meta:
        model = SKU
        fields = ['name',
                  'sku_firstletters',
                  'capsule',
                  'img',
                  'user',
                  'sizes_quantity_sold',
                  'sizes_sellsumm_sold',
                  'sizes_costsumm_sold',
                  'sizes_income',
                  'sizes_quantity_instock',
                  'sizes_costsumm_instock',
                  'margin_percent',
                  'sizes_grid',
                  'get_season_name',
                  'get_capsule_name'
                  ]

