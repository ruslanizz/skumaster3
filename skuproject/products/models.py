from django.db import models
from django.conf import settings
from django.db.models import Sum

from products.godzilla import build_sizes_grid


class UploadedBaseInfo(models.Model):
    period=models.CharField(max_length=100, default='', blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def total_sellsumm_sold(self):
        summ = Size.objects.filter(user=self.user).aggregate(Sum('sellsumm_sold'))
        return round(summ['sellsumm_sold__sum'])

    @property
    def total_costsumm_sold(self):
        summ = Size.objects.filter(user=self.user).aggregate(Sum('costsumm_sold'))
        return round(summ['costsumm_sold__sum'])

    @property
    def total_income(self):
        summ = Size.objects.filter(user=self.user).aggregate(Sum('income'))
        return round(summ['income__sum'])

    @property
    def total_costsumm_instock(self):
        summ = Size.objects.filter(user=self.user).aggregate(Sum('costsumm_instock'))
        return round(summ['costsumm_instock__sum'])



class Season(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    season_firstletters = models.CharField(max_length=7, default='', blank=False)
    id = models.CharField(max_length=100, default='', primary_key=True, editable=True)
    img = models.ImageField(upload_to="", default="default.png", )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.season_firstletters} - {self.name}'

    @property
    def capsules_quantity(self):
        return Capsule.objects.filter(user=self.user, season=self.id).count()

    @property
    def capsules_sellsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku__capsule__season=self.id).aggregate(Sum('sellsumm_sold'))
        return round(summ['sellsumm_sold__sum'])

    @property
    def capsules_costsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku__capsule__season=self.id).aggregate(Sum('costsumm_sold'))
        return round(summ['costsumm_sold__sum'])

    @property
    def capsules_income(self):
        summ = Size.objects.filter(user=self.user, sku__capsule__season=self.id).aggregate(Sum('income'))
        return round(summ['income__sum'])

    @property
    def capsules_costsumm_instock(self):
        summ = Size.objects.filter(user=self.user, sku__capsule__season=self.id).aggregate(Sum('costsumm_instock'))
        return round(summ['costsumm_instock__sum'])

    @property
    def capsules_margin_percent(self):
        if (self.capsules_sellsumm_sold - self.capsules_income) == 0:
            return 0
        return round(((self.capsules_sellsumm_sold / (self.capsules_sellsumm_sold - self.capsules_income)) * 100) - 100)


class Capsule(models.Model):
    capsule_firstletters = models.CharField(max_length=30, default='', blank=False)
    name = models.CharField(max_length=50, default='', blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сезон')
    img = models.ImageField(upload_to="", default="default.png", )
    id = models.CharField(max_length=100, default='', primary_key=True, editable=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.capsule_firstletters} - {self.name}'

    @property
    def sku_quantity(self):
        return SKU.objects.filter(user=self.user, capsule=self.id).count()

    @property
    def sku_sellsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku__capsule=self.id).aggregate(Sum('sellsumm_sold'))
        return round(summ['sellsumm_sold__sum'])

    @property
    def sku_costsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku__capsule=self.id).aggregate(Sum('costsumm_sold'))
        return round(summ['costsumm_sold__sum'])

    @property
    def sku_costsumm_instock(self):
        summ = Size.objects.filter(user=self.user, sku__capsule=self.id).aggregate(Sum('costsumm_instock'))
        return round(summ['costsumm_instock__sum'])

    @property
    def sku_income(self):
        summ = Size.objects.filter(user=self.user, sku__capsule=self.id).aggregate(Sum('income'))
        return round(summ['income__sum'])

    @property
    def sku_margin_percent(self):
        if (self.sku_sellsumm_sold-self.sku_income) == 0 :
            return 0
        return round(((self.sku_sellsumm_sold/(self.sku_sellsumm_sold-self.sku_income))*100)-100)

    @property
    def get_season_name(self):
        queryset=Season.objects.filter(user=self.user, id=self.season.id).first()
        return queryset.name

    @property
    def sold_sizes_forchart(self):  # For Chart.js
        allowed_sizes=['74','80','86','92','98','104','110','116','122','128','134','140','146','152','158','164','170']
        # Чтобы не было разнобоя в графиках, некрасиво когда разные размеры - и шапки и носки в одном графике
        sizesdict = {}
        sizeslist = []
        quantitylist = []
        sorted_dict={}
        queryset = list(Size.objects.filter(user=self.user, sku__capsule=self.id, quantity_sold__gt=0))
        for i in queryset:
            if i.size_short in allowed_sizes:
                if i.size_short not in sizesdict.keys():
                    sizesdict[i.size_short] = i.quantity_sold
                else:
                    sizesdict[i.size_short] += i.quantity_sold

        sorted_dict={x:sizesdict[x] for x in sorted(sizesdict, key=int)}

        for key, value in sorted_dict.items(): # Кажется есть риск что будет не по порядку!
            sizeslist.append(key)
            quantitylist.append(value)

        if len(sizeslist)<=1: return [[],[]]

        return [quantitylist, sizeslist]


class SKU(models.Model):
    name = models.CharField(max_length=100, default='', blank=True)
    sku_firstletters = models.CharField(max_length=15, default='', blank=False)
    capsule = models.ForeignKey(Capsule, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Капсула')
    id = models.CharField(max_length=100, default='', primary_key=True, editable=True)
    img = models.ImageField(upload_to="", default="default.png", )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sku_firstletters} - {self.name}'

    @property
    def sizes_quantity_sold(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('quantity_sold'))
        return round(summ['quantity_sold__sum'])

    @property
    def sizes_quantity_instock(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('quantity_instock'))
        return round(summ['quantity_instock__sum'])

    @property
    def sizes_sellsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('sellsumm_sold'))
        return round(summ['sellsumm_sold__sum'])

    @property
    def sizes_costsumm_sold(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('costsumm_sold'))
        return round(summ['costsumm_sold__sum'])

    @property
    def sizes_income(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('income'))
        return round(summ['income__sum'])

    @property
    def sizes_costsumm_instock(self):
        summ = Size.objects.filter(user=self.user, sku=self.id).aggregate(Sum('costsumm_instock'))
        return round(summ['costsumm_instock__sum'])

    @property
    def margin_percent(self):
        if self.sizes_costsumm_sold == 0:
            return 0
        return round((self.sizes_sellsumm_sold/self.sizes_costsumm_sold)*100-100)

    @property
    def sizes_grid(self):
        queryset=Size.objects.filter(user=self.user, sku=self.id)
        grid={}

        for i in queryset:
            # grid[i.size_short]=[i.quantity_instock, i.quantity_sold]
            grid[i.size_short]=[i.quantity_instock, i.quantity_sold, i.quantity_onway]

        result = build_sizes_grid(grid)

        return result

    @property
    def get_season_name(self):
        queryset=Season.objects.filter(user=self.user, capsule__id=self.capsule.id).first()
        return queryset.name

    @property
    def get_capsule_name(self):
        queryset=Capsule.objects.filter(user=self.user, id=self.capsule.id).first()
        return queryset.name


class Size(models.Model):
    size_short = models.CharField(max_length=20, default='', blank=True)
    size_long = models.CharField(max_length=50, default='', blank=True)
    quantity_sold = models.IntegerField(default=0)
    quantity_instock = models.IntegerField(default=0)
    sellsumm_sold = models.DecimalField(default=0, max_digits= 11,decimal_places=2, blank=True)
    costsumm_sold = models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True)
    income = models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True)
    costsumm_instock = models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True)
    sku_full = models.CharField(max_length=100, default='', blank=False)
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Артикул')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity_onway = models.IntegerField(default=0, blank=True)
    costsumm_onway = models.DecimalField(default=0, max_digits=11, decimal_places=2, blank=True)

    def __str__(self):
        return self.sku_full

# class Onway(models.Model):
