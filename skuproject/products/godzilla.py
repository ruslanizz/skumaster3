def build_sizes_grid(newsizes):
    '''
    This function builds grid, convinient for frontend visualisation.
    From dictionary like this  {'122':[3,0,1], '128':[1,1,0], '134':[3,2,4]}

    :param newsizes: {size: [quantity_instock, quantity_sold, quantity_onway]}
    :return: [
                [ ['122','INSTOCK'], ['128','INSTOCK'], ['134','INSTOCK'] ],
                [ ['122','EMPTY'], ['128','SOLD'], ['134', 'ONWAY'] ]
              ]
    '''

    def sorting_double_sizes(inputstr):
        # If we have DOUBLE size like 122*128,
        # sort(key=int) doesn't work
        # So I've made this function.
        postn = inputstr.find('*')
        if postn == -1:    # No "*"
            if inputstr.isdigit():
                return int(inputstr)
            else:   # No size or "OTHER"
                return 0
        else:
            return int(inputstr[:postn])

    # find number of rows in our grid
    summ = 0
    max_rows = 0
    for key, value in newsizes.items():
        summ = value[0] + value[1] + value[2]

        if max_rows < summ:
            max_rows = summ

    keys_list = [i for i in newsizes]       # keys - sizes
    keys_list.sort(key=sorting_double_sizes)

    final_list=[]

    newsizes_copy = newsizes

    for r in range(0,max_rows):
        myrow = []

        for key in keys_list:
            x=newsizes_copy[key]    # list like [5,2,1] , where 5 - INSTOCK, 2 - ONWAY, 1 - SOLD

            if x[0] > 0:
                myrow.append([key, 'INSTOCK'])
                newsizes_copy[key] = [x[0] - 1, x[1], x[2]]

            elif x[2]>0:
                myrow.append([key, 'ONWAY'])
                newsizes_copy[key] = [x[0], x[1], x[2]-1]

            elif x[1] > 0:
                myrow.append([key, 'SOLD'])
                newsizes_copy[key] = [x[0], x[1] - 1, x[2]]

            elif x[0] == 0 and x[1] == 0 and x[2] == 0:
                myrow.append(['-', 'EMPTY'])

        final_list.append(myrow)

    return final_list