from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
import pandas as pd

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

contacts_lists = []
contacts_lists.append(contacts_list[0])
for i in contacts_list[1:]:
    fio = re.findall('\w+', str(i[:3]))
    lastname = fio[0]
    firstname = fio[1]
    if len(fio) > 2:
        surname = fio[2]
    else:
        surname = ''
    tel = re.sub('[^0-9]', '', i[5])
    tel = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})(\d{4})', r'+7(\2)\3-\4-\5 доб.\6', tel)
    tel = re.sub(r'(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})', r'+7(\2)\3-\4-\5', tel)
    new_line = []
    new_line.extend([lastname, firstname, surname, i[3], i[4], tel, i[6]])
    contacts_lists.append(new_line)
# pprint(contacts_lists)

# # TODO 2: сохраните получившиеся данные в другой файл

contacts_lists = pd.DataFrame(contacts_lists)
contacts_lists = contacts_lists.rename(columns=contacts_lists.loc[0])
contacts_lists = contacts_lists[1:]
contacts_lists = contacts_lists.groupby(['lastname', 'firstname']).agg({'surname':'max', 'organization':'max', 'position':'max', 'phone':'max', 'email':'max'}).reset_index()
contacts_lists.to_csv('phonebook.csv',index = False)