import os

import xlrd
import openpyxl as op
from decimal import *

from skuproject.settings import STATIC_ROOT, STATIC_URL

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

        try:
            left_part_of_size = int(temp_size_divided[0])
            right_part_of_size = int(temp_size_divided[1])

            if left_part_of_size > right_part_of_size:
                sizeshort = sizelong[0:t]  # считаем так: если размер типа 92*52 то оставим только 92
                case = 'TODDLER SIZE'
            else:
                sizeshort = sizelong    # а если 14*16 то оставляем без изменений
                case = 'DOUBLE SIZE'
        except:
            case = "OTHER"  # Какойнить странный вариант типа 6*6S и т.д.
            sizeshort = sizelong

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
    try:
        # if isinstance(string, str): # нужно для того, чтобы
        string = string.replace(' ','')
        return Decimal(string)
    except:
        return 0

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
    error_message=''
    seasonname_from_config=''
    capsulename_from_config=''
    try:
        config = configparser.ConfigParser()
        config.read('sku_config.ini')
        seasons_configlist = config['Seasons']
        capsules_configlist = config['Capsules']
    except:
        print("Файл конфигурации 'sku_config.ini' не обнаружен. Названия коллекций могут не подгружаться.")
        return False, "Файл конфигурации 'sku_config.ini' не обнаружен."

    # -------- Читаем Эксель файл
    rb = xlrd.open_workbook(file_contents=xlsx_file.read())
    sheet = rb.sheet_by_index(0)

    # -------- Парсим заголовок
    row_header=-1
    period_from_xls=''
    col_sku=col_name=col_quantity_sold=col_sellsumm_sold=col_sellprice_sold=col_costsumm_sold=col_costprice_sold = -1
    col_income=col_quantity_instock=col_costsumm_instock=-1

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

            # if sheet.cell_value(rownum, colnum) == 'Цена розничная, руб. (продажи)':
            #     col_sellprice_sold=colnum


            if sheet.cell_value(rownum, colnum) == 'Сумма себестоимость, руб. (продажи)':
                col_costsumm_sold = colnum


            # if sheet.cell_value(rownum, colnum) == 'Цена себестоимость, руб. (продажи)':
            #     col_costprice_sold=colnum


            if sheet.cell_value(rownum, colnum) == 'Доход, руб.':
                col_income=colnum

            if sheet.cell_value(rownum, colnum)=='Кол-во (остатки)':
                col_quantity_instock=colnum

            if sheet.cell_value(rownum, colnum) == 'Сумма себестоимость, руб. (остатки)':
                col_costsumm_instock = colnum


        if row_header != -1 and rownum>row_header:
            break   # чтобы не пробегать весь файл до конца. Все что надо мы уже выяснили.

    if col_sku == -1:
        return False, "Нет столбца 'Номенклатура.Код'"
    if col_name == -1:
        return False, "Нет столбца 'Номенклатура'"
    if col_quantity_sold == -1:
        return False, "Нет столбца 'Кол-во (продажи)'"
    if col_sellsumm_sold == -1:
        return False, "Нет столбца 'Сумма, руб. (продажи)'"
    # if col_sellprice_sold == -1:
    #     return False, "Нет столбца 'Цена розничная, руб. (продажи)'"
    if col_costsumm_sold == -1:
        return False, "Нет столбца 'Сумма себестоимость, руб. (продажи)'"
    # if col_costprice_sold == -1:
    #     return False, "Нет столбца 'Цена себестоимость, руб. (продажи)'"
    if col_income == -1:
        return False, "Нет столбца 'Доход, руб.'"
    if col_quantity_instock == -1:
        return False, "Нет столбца 'Кол-во (остатки)'"
    if col_costsumm_instock == -1:
        return False, "Нет столбца 'Сумма себестоимость, руб. (остатки)'"


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


        # Проверим все ли в порядке с цифрами и подготовим их для записи в Size ниже

        cell = sheet.cell_value(row,col_quantity_sold)  # Количество (продажи)
        if cell:
            cell=str(cell)
            q_s=string_to_integer(cell)
        else:
            q_s=0

        cell = sheet.cell_value(row, col_sellsumm_sold) # Сумма (продажи)
        if cell:
            cell=str(cell)
            ss_s=string_to_decimal(cell)
        else:
            ss_s=0

        cell = sheet.cell_value(row, col_costsumm_sold)  # Сумма себестоимость (продажи)
        if cell:
            cell=str(cell)
            cs_s = string_to_decimal(cell)
        else:
            cs_s = 0

        cell = sheet.cell_value(row, col_income)  # Доход
        if cell:
            cell=str(cell)
            incm = string_to_decimal(cell)
        else:
            incm = 0

        cell = sheet.cell_value(row, col_quantity_instock)  # Количество (остатки)
        if cell:
            cell=str(cell)
            q_i = string_to_integer(cell)
        else:
            q_i = 0

        cell = sheet.cell_value(row, col_costsumm_instock)  # Сумма себестоимость (остатки)
        if cell:
            cell=str(cell)
            cs_i = string_to_decimal(cell)
        else:
            cs_i = 0

        # Теперь сама проверка: --------------------
        if q_s <= 0 or ss_s <=0 or cs_s <=0 : # Если кол-во проданного, сумма и себестоимость <=0,
            q_s = 0                           # то остальное не имеет смысла. А Доход может быть <=0.
            ss_s = 0
            cs_s = 0
            incm = 0

            if q_i <= 0 or cs_i <=0:    # Если при этом еще и в Instock тоже <=0, то все, пропускаем строку
                row += 1
                continue

        if q_i <= 0 or cs_i <=0:
            q_i = cs_i = 0
        # Конец проверки ------------------------------

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

        
        # Добавим Season
        if season not in seasons_checklist:
            seasons_checklist.append(season)
            try:
                seasonname_from_config=seasons_configlist[season]
            except:
                seasonname_from_config = '----'
                # print('Не нашелся в конфиге сезон')

            filename = 'images/'+ season+'/'+season + '.jpg'
            image_season = STATIC_URL + filename

            if not os.path.isfile(STATIC_ROOT+'/'+filename):
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

            filename = 'images/' + season + '/' + capsule + '.jpg'
            image_capsule = STATIC_URL + filename

            if not os.path.isfile(STATIC_ROOT+'/' + filename):
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

            filename = 'images/' + season+'/'+capsule+'/'+sku_nosize + '.jpg'
            image_sku = STATIC_URL + filename

            if not os.path.isfile(STATIC_ROOT+'/'+filename):
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

    # print('SEASON!!!!!', Season.objects.all())
    return True, error_message



def upload_onway_bill(xlsx_file, user_id):

    # -------- Читаем config файл
    seasons_configlist = []
    capsules_configlist = []
    error_message=''
    seasonname_from_config=''
    capsulename_from_config=''
    try:
        config = configparser.ConfigParser()
        config.read('sku_config.ini')
        seasons_configlist = config['Seasons']
        capsules_configlist = config['Capsules']
    except:
        print("Файл конфигурации 'sku_config.ini' не обнаружен. Названия коллекций могут не подгружаться.")
        return False, "Файл конфигурации 'sku_config.ini' не обнаружен."

    # -------- Читаем Эксель файл

    wb = op.load_workbook(xlsx_file, data_only=True)
    sheet = wb.active

    # -------- Парсим заголовок
    row_header = -1

    col_sku = col_name = col_quantity = col_summ = -1
    name=''

    for rownum in range(1,sheet.max_row+1):
        for colnum in range(sheet.max_column+1):

            if str(sheet.cell(row=rownum, column=colnum).value) == 'Артикул':
                col_sku=colnum
                row_header = rownum

            if str(sheet.cell(row=rownum, column=colnum).value) == 'Товары (работы, услуги)':
                col_name = colnum

            if str(sheet.cell(row=rownum, column=colnum).value) == 'Кол-во':
                col_quantity = colnum


            if str(sheet.cell(row=rownum, column=colnum).value) == 'Сумма':
                col_summ = colnum


        if row_header != -1 and rownum > row_header:
            break  # чтобы не пробегать весь файл до конца. Все что надо мы уже выяснили.

    if col_sku == -1:
        return False, "Нет столбца 'Артикул'"
    if col_name == -1:
        return False, "Нет столбца 'Товары (работы, услуги)'"
    if col_quantity == -1:
        return False, "Нет столбца 'Кол-во'"
    if col_summ == -1:
        return False, "Нет столбца 'Сумма'"

    # -------- Читаем из файла строки и формируем списки, затем позже сделаем bulk_create
    season_list = []  # Список моделей , который мы потом запишем
    capsule_list = []
    sku_list = []
    size_list = []

    seasons_checklist = []  # Список по которому мы будем проверять, создана ли уже такая модель
    capsules_checklist = []
    skus_checklist = []

    row = row_header + 1  # Начнем со строки заголовка+1, выше нет смысла начинать

    while row < sheet.max_row: # Проверить, не надо ли +1

        work_cell = sheet.cell(row=row, column=col_sku).value   # Артикул
        work_cell=work_cell.strip()

        # Нехитрым способом проверим что первые три символа - это цифры и значит это артикул
        if not str(work_cell)[:3].isdigit():
            row += 1
            continue

        # Проверим все ли в порядке с цифрами и подготовим их для записи в Size ниже

        cell = sheet.cell(row=row, column=col_name).value  # Наименование
        if cell:
            name=cell

        cell = sheet.cell(row=row, column=col_quantity).value  # Количество
        if cell:
            cell = str(cell)
            q_onway = string_to_integer(cell)
        else:
            q_onway = 0

        cell = sheet.cell(row=row, column=col_summ).value  # Сумма
        if cell:
            cell = str(cell)
            summ_onway = string_to_decimal(cell)
        else:
            summ_onway = 0


        # Теперь сама проверка: --------------------
        if q_onway <= 0 or summ_onway <= 0 :  # Если кол-во , сумма  <=0,
            row += 1
            continue

        # Конец проверки ------------------------------

        # Разберем прочитанный sku на части
        t = work_cell.find('-')
        if t != -1:
            sku_nosize = work_cell[:t]  # Артикул без размера
            sizelong = work_cell[t + 1:]
        else:
            sku_nosize = work_cell
            sizelong = 'No size'

        season = work_cell[:5]  # Первые цифры сезона
        if season[3:5] == 'GS' or season[3:5] == 'gs':
            pass  # Значит Школа, берем первые 5 символов
        else:
            season = season[0:3]  # Не школа, берем 3 символа

        capsule = sku_nosize[:6]  # Капсула - первые 6 символов артикула

        string_id_season = ''

        # Добавим Season
        # Но сначала проверим, нет ли его уже в Базе Данных:
        if Season.objects.filter(season_firstletters=season, user=user_id).exists():
            one_entry = Season.objects.get(season_firstletters=season, user=user_id)
            string_id_season = one_entry.id
        else:

            if season not in seasons_checklist:
                seasons_checklist.append(season)
                try:
                    seasonname_from_config=seasons_configlist[season]
                except:
                    seasonname_from_config = '----'
                    # print('Не нашелся в конфиге сезон')

                filename = 'images/'+ season+'/'+season + '.jpg'
                image_season = STATIC_URL + filename

                if not os.path.isfile(STATIC_ROOT+'/'+filename):
                    image_season = ''

                # id назначаю сам, потому что сначала вся база создается в памяти, и только в конце будет bulk_create
                # А так как мне надо установить уже все связи ForeignKey, мне уже нужно знать id
                # поэтому сделал id типа CharField и вида 'onway-номер строки-user id'
                # то есть что-то типа 'onway-211-18'. Это должно быть уникальным id
                # добавляю 'onway-' потому что строки могут совпасть с id уже существующими в базе

                string_id_season='onway-'+str(row)+'-'+str(user_id.id)
                print('string_id_season:',string_id_season)

                season_list.append(Season(season_firstletters=season,
                                          name = seasonname_from_config,
                                          img = image_season,
                                          user = user_id,
                                          id=string_id_season))  #id назначаю сам


        # Добавим Capsule
        # Но сначала проверим, нет ли его уже в Базе Данных:
        if Capsule.objects.filter(capsule_firstletters=capsule, user=user_id).exists():
            one_entry=Capsule.objects.get(capsule_firstletters=capsule, user=user_id)
            string_id_capsule=one_entry.id
        else:
            if capsule not in capsules_checklist:
                capsules_checklist.append(capsule)
                try:
                    capsulename_from_config=capsules_configlist[capsule]
                except:
                    capsulename_from_config='----'
                    # print('Не нашлась в конфиге капсула')

                filename = 'images/' + season + '/' + capsule + '.jpg'
                image_capsule = STATIC_URL + filename

                if not os.path.isfile(STATIC_ROOT+'/' + filename):
                    image_capsule = ''

                season_id=string_id_season
                # print('season_id', season_id)

                string_id_capsule='onway-'+str(row)+'-'+str(user_id.id)

                capsule_list.append(Capsule(capsule_firstletters=capsule,
                                            id=string_id_capsule,
                                            name=capsulename_from_config,
                                            img = image_capsule,
                                            user=user_id,
                                            season=Season(id=season_id)))   # корректно ли так писать? так то работает все

        # Добавим Sku
        # Но сначала проверим, нет ли его уже в Базе Данных:
        if SKU.objects.filter(sku_firstletters=sku_nosize, user=user_id).exists():
            one_entry=SKU.objects.get(sku_firstletters=sku_nosize, user=user_id)
            string_id_sku=one_entry.id
        else:
            if sku_nosize not in skus_checklist:
                skus_checklist.append(sku_nosize)

                filename = 'images/' + season+'/'+capsule+'/'+sku_nosize + '.jpg'
                image_sku = STATIC_URL + filename

                if not os.path.isfile(STATIC_ROOT+'/'+filename):
                    image_sku = ''

                capsule_id=string_id_capsule

                string_id_sku='onway-'+str(row)+'-'+str(user_id.id)

                sku_list.append(SKU(name=sheet.cell_value(row+1,col_name),
                                    sku_firstletters=sku_nosize,
                                    id=string_id_sku,
                                    capsule=Capsule(id=capsule_id),
                                    user=user_id,
                                    img = image_sku
                ))


        # Добавим Size
        sku_id = string_id_sku

        s_s = get_size_short(sizelong)

        size_list.append(Size(size_long=sizelong,
                              sku_full=work_cell,
                              sku=SKU(id=sku_id),
                              user=user_id,
                              quantity_sold=0,
                              sellsumm_sold=0,
                              costsumm_sold=0,
                              income=0,
                              quantity_instock=0,
                              costsumm_instock=0,
                              size_short=s_s,
                              # quantity_onway=q_onway,
                              # costsumm_onway=summ_onway

                              ))

        row+=1
        # if row>40: break    # Пока ограничимся 40 строками


    return True, error_message