dict_ = [{'name': 'david', 'prenom': 'jean'}, {'name': 50, 'prenom': 'coco'},{'name': 20, 'prenom': 'doudou'},{'name': 'hilaire', 'prenom': 'sousou'},{'name': 'goura', 'prenom': 'toutou'}]
dict_second = {'name': 'ema', 'prenom': 'jean'}
empty_ = {}
list_second = ['name', 'prenom']

#-----------------------------------------------------------------
init_data_dic = {val: [] for val in list_second}

for item in dict_:
    for key, value in item.items():
        init_data_dic[key] += [value]

#-------------------------------------------------------------
empty_list = []
for dict_val in init_data_dic.values():
    empty_list.append(dict_val[1])
print(init_data_dic)
print(empty_list)



"""with open("bank.csv", 'r') as f_csv:
    read_csv_file = csv.DictReader(f_csv)
    #list_for_column = []
    for data in read_csv_file:
        list_for_column = list(data.keys())
        break

    size_of_row = len(list(read_csv_file))
    print(list_for_column)
    print(size_of_row, len(list_for_column), sep='\t')"""



"""with open("bank.csv", "r") as f_csv:
    spliting_ = []
    for word in f_csv:
        empty_list = []
        for value in word.split(','):
            try:
                numeric_value = int(value)
            except Exception:
                empty_list.append(value)
            else:
                empty_list.append(numeric_value)

        spliting_.append(empty_list)
        print(spliting_)
    print(len(spliting_))
    print(len(spliting_) - 1)"""