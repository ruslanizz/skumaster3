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
                  # 'capsules_quantity',
                  'capsules_sellsumm_sold',
                  'capsules_costsumm_sold',
                  'capsules_income',
                  'capsules_costsumm_instock',
                  'capsules_margin_percent',
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
                  # 'sku_quantity',
                  'sku_sellsumm_sold',
                  'sku_costsumm_sold',
                  'sku_costsumm_instock',
                  'sku_income',
                  'sku_margin_percent',
                  'get_season_name',
                  'sold_sizes_forchart',
                  'sizes_sold_quantity',
                  'sizes_instock_quantity',
                  'rentability',
                  'rating_rentability',
                  'rating_income',
                  'rating_rel_leftovers',
                  'relative_leftovers',
                  'rating_total',
                  'gender',
                  'age'
                          ]


class UploadedBaseInfoSerializer(ModelSerializer):
    class Meta:
        model = UploadedBaseInfo
        fields = ['period',
                  'upload_date',
                  'user',
                  'total_sellsumm_sold',
                  'total_costsumm_sold',
                  'total_income',
                  'total_costsumm_instock']


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
                  'get_capsule_name',
                  'rating_income',
                  'rating_sellsumm_sold',
                  'rating_quantity',
                  # 'clothes_type',
                  'get_clothes_type_display'
                  ]


class AnalyticsCapsuleSerializer(ModelSerializer):
    class Meta:
        model = Capsule
        fields = ['name',
                  'id',
                  'season',
                  # 'img',
                  'capsule_firstletters',
                  'user',
                  # 'sku_quantity',
                  # 'sku_sellsumm_sold',
                  # 'sku_costsumm_sold',
                  # 'sku_costsumm_instock',
                  # 'sku_income',
                  # 'sku_margin_percent',
                  'get_season_name',
                  # 'sizes_sold_quantity',
                  # 'sizes_instock_quantity',
                  'type_of_clothes', # переименовать, это количество футболок и т п
                  'gender',
                  'age'
                          ]


class AnalyticsSeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = ['name',
                  'id',
                  'img',
                  'season_firstletters',
                  'user',
                  # 'capsules_quantity',
                  # 'capsules_sellsumm_sold',
                  # 'capsules_costsumm_sold',
                  # 'capsules_income',
                  # 'capsules_costsumm_instock',
                  # 'capsules_margin_percent',
                  'analytics_gender_age',
                  ]
