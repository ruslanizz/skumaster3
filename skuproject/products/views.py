from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.models import UploadedBaseInfo, Season, Capsule, SKU
from products.serializers import UploadedBaseInfoSerializer, SeasonSerializer, CapsuleSerializer, SkuSerializer, \
    AnalyticsCapsuleSerializer, AnalyticsSeasonSerializer
from products.services import handle_uploaded_file, upload_onway_bill, set_sku_ratings, set_capsule_ratings, \
    set_total_rating


class UploadedBaseInfoView(ModelViewSet):
    queryset = UploadedBaseInfo.objects.all()
    serializer_class = UploadedBaseInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


# class SeasonsView(ModelViewSet):
#     queryset = Season.objects.all()
#     serializer_class = SeasonSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         queryset = self.queryset
#         query_set = queryset.filter(user=self.request.user)
#         return query_set


class SeasonsView(ModelViewSet):
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Season.objects.filter(user=self.request.user)


def demo_index_page(request):
    demo_user = authenticate(username='test@test.com', password='Sosiska25')
    login(request, demo_user)
    return render(request,'index.html')


@login_required
def index_page(request):
    return render(request,'index.html')


def upload_file(request):
    successfully_loaded = False
    if request.method == 'POST' and request.FILES.get('xlsx_file'):
        uploaded_xlsx_file = request.FILES['xlsx_file']
        successfully_loaded, error_message = handle_uploaded_file(uploaded_xlsx_file, request.user)

        if successfully_loaded:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'open.html', {'message': error_message})

    return render(request,'open.html')


def capsules_page(request):
    current_season = request.GET.get('season', None)
    if current_season is not None:
        oneentry = Season.objects.get(id=current_season, user=request.user)
        if not oneentry.capsule_ratings_were_set:
            set_capsule_ratings(current_season, request.user)
            oneentry.capsule_ratings_were_set = True
            oneentry.save()
            set_total_rating(current_season, request.user)

    return render(request, 'capsules.html')


def sku_page(request):
    current_capsule = request.GET.get('capsule', None)
    if current_capsule is not None:
        oneentry = Capsule.objects.get(id=current_capsule, user=request.user)
        if not oneentry.sku_ratings_were_set:
            set_sku_ratings(current_capsule, request.user)
            oneentry.sku_ratings_were_set = True
            oneentry.save()
    return render(request, 'sku.html')


class SkuView(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SkuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override method to get filtered queryset
        """
        query_set = self.queryset
        param = self.request.query_params.get('capsule', None)
        if param is not None:
            query_set = query_set.filter(capsule=param, user=self.request.user)
        return query_set


class CapsulesView(ModelViewSet):
    queryset = Capsule.objects.all()
    serializer_class = CapsuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override method to get filtered queryset
        """
        query_set = self.queryset
        param = self.request.query_params.get('season', None)
        if param is not None:
            query_set = query_set.filter(season=param, user=self.request.user)
        return query_set


def onway_page(request):
    successfully_loaded = False
    if request.method == 'POST' and request.FILES.get('xlsx_file'):
        uploaded_xlsx_file = request.FILES['xlsx_file']
        successfully_loaded, error_message = upload_onway_bill(uploaded_xlsx_file, request.user)

        if successfully_loaded:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'onway.html', {'message': error_message})

    return render(request, 'onway.html')


def analytics_page(request):
    return render(request, 'analytics.html')


class AnalyticsCapsuleView(ModelViewSet):
    queryset = Capsule.objects.all()
    serializer_class = AnalyticsCapsuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override method to get filtered queryset
        """
        query_set = self.queryset
        param = self.request.query_params.get('season', None)
        print('===========', param)
        if param is not None:
            query_set = query_set.filter(season=param, user=self.request.user)
        return query_set


class AnalyticsSeasonView(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = AnalyticsSeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override method to get filtered queryset
        """
        query_set = self.queryset
        param = self.request.query_params.get('id', None)
        print('###########', param)
        if param is not None:
            query_set = query_set.filter(id=param, user=self.request.user)
        return query_set