def build_sizes_grid(newsizes):

    def sorting_double_sizes(inputstr):
        # Эта функция нужна изза случаев с двойными размерами типа 122*128
        # в этом случае функция sort(key=int) не работает, к сожалению
        # if inputstr=='No size':
        #     return 0   # Если нет размера
        postn = inputstr.find('*')
        if postn == -1:    # Звездочки нет
            if inputstr.isdigit():
                return int(inputstr)
            else:   # Если нет размера или там "OTHER"
                return 0
        else:
            return int(inputstr[:postn])

    # определим Максимальное количество строк в нашей grid size
    summ = 0
    max_rows = 0
    for key, value in newsizes.items():
        summ = value[0] + value[1]
        if max_rows < summ: max_rows = summ
    # print('max rows', max_rows)

    # определим Максимальное количество колонок
    max_cols=len(newsizes)
    # print('max cols',max_cols)

    # keys_list=newsizes.keys()

    # Создадим список ключей (размеров):
    keys_list = [i for i in newsizes]   # да, такая вот слегка сложноватая запись
    # print(keys_list)
    keys_list.sort(key=sorting_double_sizes)


    # print('newsizes',newsizes)

    # print('SORTED', keys_list)
    # Где то здесь надо будет сделать сортировку по размерам! Предусмотреть что размер может быть не int, а string
    final_list=[]

    newsizes_copy = newsizes

    for r in range(0,max_rows):
        myrow = []

        for key in keys_list:
            x=newsizes_copy[key]    # это список типа [5,2]

            if x[0]>0:
                myrow.append([key,'INSTOCK'])
                newsizes_copy[key]=[x[0]-1,x[1]]
            elif x[1]>0:
                myrow.append([key,'SOLD'])
                newsizes_copy[key]=[x[0],x[1]-1]
            elif x[0]==0 and x[1]==0:
                myrow.append(['-', 'EMPTY'])

        # print('myrow', myrow)
        final_list.append(myrow)

    # print('final', final_list)
    # print('-----------------')

    return final_list