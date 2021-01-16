from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from products.models import UploadedBaseInfo, Season, Capsule, SKU
from rest_framework.viewsets import ModelViewSet

from products.serializers import UploadedBaseInfoSerializer, SeasonSerializer, CapsuleSerializer, SkuSerializer
from products.services import handle_uploaded_file


class UploadedBaseInfoView(ModelViewSet):
    queryset = UploadedBaseInfo.objects.all()
    serializer_class = UploadedBaseInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


class SeasonsView(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(user=self.request.user)
        return query_set


@login_required
def index_page(request):
    print('USER:',request.user)
    print('USER ID:',request.user.id)

    return render(request,'index.html')


def upload_file(request):
    successfully_loaded = False
    if request.method == 'POST' and request.FILES.get('xlsx_file'):

        uploaded_xlsx_file = request.FILES['xlsx_file']
        print('Эксель файл загружен:')
        print('Файл:', uploaded_xlsx_file.name)
        print('Размер файла:', uploaded_xlsx_file.size)
        print('--------------------------')
        successfully_loaded, error_message = handle_uploaded_file(uploaded_xlsx_file, request.user)
        if successfully_loaded:
            return HttpResponseRedirect('/')
        else:
            return render(request, 'open.html', {'message': error_message})

    return render(request,'open.html')


def capsules_page(request):
    return render(request, 'capsules.html')


def sku_page(request):
    return render(request, 'sku.html')

class SkuView(ModelViewSet):

    queryset = SKU.objects.all()
    serializer_class = SkuSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Переопределяем метод чтобы получать фильтрованный queryset
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
        Переопределяем метод чтобы получать фильтрованный queryset
        """
        query_set = self.queryset
        param = self.request.query_params.get('season', None)
        if param is not None:
            query_set = query_set.filter(season=param, user=self.request.user)
        return query_set