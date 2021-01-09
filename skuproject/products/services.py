import os

import xlrd
from decimal import *

from skuproject.settings import MEDIA_ROOT
from .models import UploadedBaseInfo, SKU, Capsule, Season, Size
import configparser


def get_size_short(sizelong):
    # Размер вида 140*72*63  разбирает и на выходе отдает короткую версию размера
    # причем определяет корректно - если спаренный размер то оставляет обе цифры

    if sizelong.count('*') == 2:  # если в размере две звездочки
        t = sizelong.find('*')  # находим номер символа первой звездочки
        sizeshort = sizelong[0:t]  # сокращаем размер - отбрасываем первую звездочку и все после нее
        case = 'NORMAL SIZE'

    elif sizelong.count('*') == 1:  # если одна звездочка в размере
        t = sizelong.find('*')  # то может быть два варианта - либо это тоддлеры, либо спаренные размеры

        temp_size_divided = sizelong.split('*')  # делим размер на две части , разделитель звездочка
        left_part_of_size = int(temp_size_divided[0])
        right_part_of_size = int(temp_size_divided[1])

        if left_part_of_size > right_part_of_size:
            sizeshort = sizelong[0:t]  # считаем так: если размер типа 92*52 то оставим только 92
            case = 'TODDLER SIZE'
        else:
            sizeshort = sizelong    # а если 14*16 то оставляем без изменений
            case = 'DOUBLE SIZE'

    elif sizelong == 'No size':
        sizeshort = 'No size'
        case = 'NO SIZE'

    elif sizelong.isdigit():
        case = 'ONE DIGIT SIZE'
        sizeshort=sizelong

    else:
        case = "OTHER"  # Все другие варианты типа 120/30 и т.д.
        sizeshort = sizelong

    return sizeshort


def string_to_decimal(string):
    string = string.replace(' ','')
    return Decimal(string)

def string_to_integer(string):
    try:
        string = string.replace(' ','')
        pos=string.find('.')
        if pos != -1:
            return int(string[:pos])
        return int(string)
    except:
        return 0

def handle_uploaded_file(xlsx_file, user_id):
    # -------- Читаем config файл
    seasons_configlist = []
    capsules_configlist = []
    seasonname_from_config=''
    capsulename_from_config=''
    try:
        config = configparser.ConfigParser()
        config.read('sku_config.ini')
        seasons_configlist = config['Seasons']
        capsules_configlist = config['Capsules']
    except:
        print("Файл конфигурации 'sku_config.ini' не обнаружен. Названия коллекций могут не подгружаться.")

    # -------- Читаем Эксель файл
    rb = xlrd.open_workbook(file_contents=xlsx_file.read())
    sheet = rb.sheet_by_index(0)

    # def Check if this table is ok
    #   return False

    # -------- Парсим заголовок
    row_header=-1

    for rownum in range(sheet.nrows):
        for colnum in range(sheet.ncols):

            if str(sheet.cell_value(rownum, colnum))[:7] == 'Период:':
                t1=sheet.cell_value(rownum, colnum).find('\n')  # находим место перевода строки
                period_from_xls=sheet.cell_value(rownum, colnum)[8:t1]

            if sheet.cell_value(rownum, colnum) == 'Номенклатура.Код':
                col_sku=colnum

            if sheet.cell_value(rownum, colnum) == 'Номенклатура':
                col_name=colnum

            if sheet.cell_value(rownum, colnum)=='Кол-во (продажи)':
                col_quantity_sold=colnum
                row_header = rownum

            if sheet.cell_value(rownum, colnum) == 'Сумма, руб. (продажи)':
                col_sellsumm_sold=colnum

            if sheet.cell_value(rownum, colnum) == 'Цена розничная, руб. (продажи)':
                col_sellprice_sold=colnum

            if sheet.cell_value(rownum, colnum) == 'Сумма себестоимость, руб. (продажи)':
                col_costsumm_sold = colnum

            if sheet.cell_value(rownum, colnum) == 'Цена себестоимость, руб. (продажи)':
                col_costprice_sold=colnum

            if sheet.cell_value(rownum, colnum) == 'Доход, руб.':
                col_income=colnum

            if sheet.cell_value(rownum, colnum)=='Кол-во (остатки)':
                col_quantity_instock=colnum

            if sheet.cell_value(rownum, colnum) == 'Сумма себестоимость, руб. (остатки)':
                col_costsumm_instock = colnum

        if row_header != -1 and rownum>row_header:
            break   # чтобы не пробегать весь файл до конца. Все что надо мы уже выяснили.

    # -------- Читаем из файла строки и формируем списки, затем позже сделаем bulk_create
    season_list=[]          # Список моделей , который мы потом запишем
    capsule_list=[]
    sku_list = []
    size_list=[]

    seasons_checklist=[]    # Список по которому мы будем проверять, создана ли уже такая модель
    capsules_checklist=[]
    skus_checklist=[]


    row = row_header + 1  # Начнем со строки заголовка+1, выше нет смысла начинать

    while row < sheet.nrows:
        work_cell=sheet.cell_value(row,col_sku).strip()

        # Нехитрым способом проверим что первые три символа - это цифры и значит это артикул
        if not str(work_cell)[:3].isdigit():
            row+=1
            continue

        # Разберем прочитанный sku на части
        t = work_cell.find('-')
        if t != -1:
            sku_nosize = work_cell[:t] # Артикул без размера
            sizelong = work_cell[t+1:]
        else:
            sku_nosize = work_cell
            sizelong = 'No size'

        season = work_cell[:5]  # Первые цифры сезона
        if season[3:5] == 'GS' or season[3:5] == 'gs':
            pass  # Значит Школа, берем первые 5 символов
        else:
            season = season[0:3]  # Не школа, берем 3 символа

        capsule = sku_nosize[:6]    # Капсула - первые 6 символов артикула

        # print('=========================')
        # print('work_cell=', work_cell)
        # print('sku_nosize',sku_nosize)
        # print('sizelong', sizelong)
        # print('season', season)
        # print('CAPSULE=', capsule)

        # Добавим Season
        if season not in seasons_checklist:
            seasons_checklist.append(season)
            try:
                seasonname_from_config=seasons_configlist[season]
            except:
                seasonname_from_config = '----'
                # print('Не нашелся в конфиге сезон')

            image_season = season+'/'+season + '.jpg'
            if not os.path.isfile(MEDIA_ROOT+'/'+image_season):
                image_season = ''

            # id назначаю сам, потому что сначала вся база создается в памяти, и только в конце будет bulk_create
            # А так как мне надо установить уже все связи ForeignKey, мне уже нужно знать id
            # поэтому сделал id типа CharField и вида 'номер строки-user id'
            # то есть что-то типа '211-18'. Это должно быть уникальным id

            string_id=str(row)+'-'+str(user_id.id)
            print('string_id:',string_id)

            season_list.append(Season(season_firstletters=season,
                                      name = seasonname_from_config,
                                      img = image_season,
                                      user = user_id,
                                      id=string_id))  #id назначаю сам

        # Добавим Capsule
        if capsule not in capsules_checklist:
            capsules_checklist.append(capsule)
            try:
                capsulename_from_config=capsules_configlist[capsule]
            except:
                capsulename_from_config='----'
                # print('Не нашлась в конфиге капсула')

            image_capsule = season + '/' + capsule + '.jpg'
            if not os.path.isfile(MEDIA_ROOT + '/' + image_capsule):
                image_capsule = ''

            season_id=[i.id for i in season_list if i.season_firstletters == season][0]
            # print('season_id', season_id)

            string_id=str(row)+'-'+str(user_id.id)

            capsule_list.append(Capsule(capsule_firstletters=capsule,
                                        id=string_id,
                                        name=capsulename_from_config,
                                        img = image_capsule,
                                        user=user_id,
                                        season=Season(id=season_id)))   # корректно ли так писать? так то работает все


        # Добавим Sku
        if sku_nosize not in skus_checklist:
            skus_checklist.append(sku_nosize)

            image_sku = season+'/'+capsule+'/'+sku_nosize + '.jpg'
            if not os.path.isfile(MEDIA_ROOT+'/'+image_sku):
                image_sku = ''

            capsule_id=[i.id for i in capsule_list if i.capsule_firstletters == capsule][0]

            string_id=str(row)+'-'+str(user_id.id)

            sku_list.append(SKU(name=sheet.cell_value(row+1,col_name),
                                sku_firstletters=sku_nosize,
                                id=string_id,
                                capsule=Capsule(id=capsule_id),
                                user=user_id,
                                img = image_sku
            ))

        # Добавим Size
        sku_id = [i.id for i in sku_list if i.sku_firstletters == sku_nosize][0]

        cell = sheet.cell_value(row,col_quantity_sold)  # Количество (продажи)
        if cell:
            q_s=string_to_integer(cell)
        else:
            q_s=0

        cell = sheet.cell_value(row, col_sellsumm_sold) # Сумма (продажи)
        if cell:
            ss_s=string_to_decimal(cell)
        else:
            ss_s=0

        cell = sheet.cell_value(row, col_costsumm_sold)  # Сумма себестоимость (продажи)
        if cell:
            cs_s = string_to_decimal(cell)
        else:
            cs_s = 0

        cell = sheet.cell_value(row, col_income)  # Доход
        if cell:
            incm = string_to_decimal(cell)
        else:
            incm = 0

        cell = sheet.cell_value(row, col_quantity_instock)  # Количество (остатки)
        if cell:
            q_i = string_to_integer(cell)
        else:
            q_i = 0

        cell = sheet.cell_value(row, col_costsumm_instock)  # Сумма себестоимость (остатки)
        if cell:
            cs_i = string_to_decimal(cell)
        else:
            cs_i = 0

        s_s = get_size_short(sizelong)

        size_list.append(Size(size_long=sizelong,
                              sku_full=work_cell,
                              sku=SKU(id=sku_id),
                              user=user_id,
                              quantity_sold=q_s,
                              sellsumm_sold=ss_s,
                              costsumm_sold=cs_s,
                              income=incm,
                              quantity_instock=q_i,
                              costsumm_instock=cs_i,
                              size_short=s_s

                              ))

        row+=1
        # if row>40: break    # Пока ограничимся 40 строками


    #   ------------------ Now lets write to database ----------------

    # -------- Удалим всю старую базу
    UploadedBaseInfo.objects.filter(user=user_id).delete()
    Season.objects.filter(user=user_id).delete()
    Capsule.objects.filter(user=user_id).delete()
    SKU.objects.filter(user=user_id).delete()
    Size.objects.filter(user=user_id).delete()


    UploadedBaseInfo.objects.create(user=user_id, period=period_from_xls)
    Season.objects.bulk_create(season_list)
    Capsule.objects.bulk_create(capsule_list)
    SKU.objects.bulk_create(sku_list)
    Size.objects.bulk_create(size_list)

    return True


