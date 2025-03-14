import random
import json
from . import config
import pymysql

def get_ans(data):
    json_end = dict()
    json_export = dict()
    group_list = []

    group_list_raw = data['groupList']
    for group_id_inp in group_list_raw:
        r = get_group_params(data['compId'], group_id_inp)
        #Не нашли группу
        if r == "undefinedGroup":
            json_end['group_number'] =  group_id_inp
            json_end['status'] = "fail"
            json_end['judge_id'] = []
            json_export[group_id_inp] = json_end
        else:
            group_list.append(r)

        #Все группы не пробились
    if group_list == []:
        return json.loads(json.dumps(json_export))

    relatives_list, black_list, judge_counter_list = get_future_tables()
    comp_region_id = data['regionId']
    relatives_dict = relatives_list_change(relatives_list)

    # 1. сортировка входящего списка групп в зависимости от требуемой для судейства категории
    group_list.sort(key=lambda x: x[2] * -1)

    # 2. запрашиваем и обрабатываем список судей
    ans = get_all_judges_yana(data['compId'])

    all_judges_list = {}  # преобразуем словарь для более удобной работы, создаем общий список доступных для выбора судей с параметрами

    for i in ans:
        i['SPORT_Category_decoded'] = decode_category(i['SPORT_Category'])
        all_judges_list[i['id']] = i

    s = 0

    # 3. начинаем работать с каждой группой из переданного списка
    for i in group_list:
        json_end = dict()

        s += 1
        if s == 0: sucess_result = 0

        if s > 1 and sucess_result == 1:  # если нам передали несколько групп, то есть мы должны генерить в параллель и если это уже не первая группа и предыдущая была сгенерена успешно
            # тогда из общего списка судей выкидываем всех кого нагенерили в панельки ранее
            group_all_judges_list = all_judges_list.copy()
            for j in group_finish_judges_list:
                group_all_judges_list.pop(j, None)
            group_finish_judges_list = []
            regions = {}
            sucess_result = 0
        else:
            group_all_judges_list = all_judges_list.copy()  # общий список судей из которого будем случайно выбирать
            group_finish_judges_list = []  # список, в котором финально будем передавать судей, оценивающих категорию
            regions = {}  # счетчик судейств по регионам

        # определяем параметры группы
        n_judges, min_category = i[1], i[2]
        #otd_num = group_list[i]['otd_num']

        group_number = i[0]
        n_judges_category = 0

        # определяем условия на регионы судей
        n_jud_comp_region, n_jud_other_region = rc_a_region_rules(comp_region_id, n_judges)

        group_all_judges_list = judges_category_filter(group_all_judges_list,
                                                       min_category)  # 4. удаляем судей с неподходящей категорией

        black_list_cat = black_list_convert(group_number,
                                            black_list)  # 5. определяем судей с запретом на судейство в конкретной категории
        group_all_judges_list = judges_black_list_filter(group_all_judges_list,
                                                         black_list_cat)  # 6. удаляем таких судей из категории

        if len(group_all_judges_list) > n_judges:
            while n_judges_category < n_judges:
                if len(group_all_judges_list) > 0:
                    # после чисток выбираем рандомного судью из списка
                    try_judge_data = get_random_judge(group_all_judges_list)

                    # обновляем данные о судейском составе текущей группы
                    group_finish_judges_list.append(try_judge_data['id'])  # добавили судью в список выбранных
                    n_judges_category += 1  # количество набранных судей в категорию увеличилось на 1

                    # добавили информацию о регионе судьи в словарь по регионам
                    if try_judge_data['RegionId'] in regions:
                        regions[try_judge_data['RegionId']] += 1
                        if try_judge_data['RegionId'] == comp_region_id and regions[try_judge_data[
                            'RegionId']] == n_jud_comp_region:  # если судья из "домашнего" региона и при его добавлении лимит для региона исчерпан
                            # ФУНКЦИЯ удаляем всех судей с таким же регионом
                            group_all_judges_list = delete_region_from_judges(group_all_judges_list,
                                                                              try_judge_data['RegionId'])
                        elif try_judge_data['RegionId'] != comp_region_id and regions[
                            try_judge_data['RegionId']] == n_jud_other_region:
                            # ФУНКЦИЯ удаляем всех судей с таким же регионом
                            group_all_judges_list = delete_region_from_judges(group_all_judges_list,
                                                                              try_judge_data['RegionId'])
                    else:
                        regions[try_judge_data['RegionId']] = 1

                    # удалили всех с таким же клубом
                    group_all_judges_list = delete_club_from_judges(group_all_judges_list, try_judge_data['Club'])

                    # обновляем данные о судях, доступных для выбора
                    group_all_judges_list.pop(try_judge_data['id'],
                                              None)  # судью которого мы выбрали второй раз выбрать нельзя
                    # если у судьи есть родственники, то применяем функцию для удаления родственников
                    if try_judge_data['id'] in relatives_dict:
                        for i in relatives_dict[try_judge_data['id']]:
                            group_all_judges_list.pop(i, None)

                    if n_judges_category == n_judges:  # если набрали необходимое количество судей, то успех
                        sucess_result = 1
                else:
                    print('Не удалось набрать необходимое количество судей по заданным ограничениям')
                    print(group_finish_judges_list)
                    break

            json_end['group_number'] = group_number
            json_end['status'] = "success"
            json_end['judge_id'] = list()
            for i in group_finish_judges_list:
                json_end['judge_id'].append(all_judges_list[i]['id'])
            print('Распределение регионов', regions)
        else:
            sucess_result = 0
            json_end['group_number'] = group_number
            json_end['status'] = "fail"

        json_export[group_number] = json_end

    return json.loads(json.dumps(json_export))

#получить параметр групп по турниру и номеру
def get_group_params(comp_id, group_id):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            cur.execute(
                f'''SELECT groupId, groupNumber,judges, minCategoryId
                 from competition_group
                 WHERE compId = {comp_id} and groupId = {group_id}
                                        ''')
            data = cur.fetchone()
            if data is None:
                return "undefinedGroup"
            else:
                return data['groupId'], data['judges'], data['minCategoryId']
    except:
        return 0

#функция для ограничения на регионы
def rc_a_region_rules(comp_region_id, n_judges):
  if n_judges == 7:
    return(3, 2)
  elif n_judges == 9:
    return(4, 2)
  elif n_judges == 11:
    return(5, 3)
  elif n_judges == 13:
    return(6, 3)


#костыль пока не таблиц в БД
def get_future_tables():
    #group_list = {
        #21: {'name': 'Мужчины и женщины латиноамериканская программа', 'min_category': 8, 'otd_num': 11,
    #     'n_judges': 11},
        #22: {'name': 'Мужчины и женщины европейская программа', 'min_category': 7, 'otd_num': 11, 'n_judges': 9},
        # 23: {'name': 'Мужчины и женщины двоеборье', 'min_category': 5, 'otd_num' : 11, 'n_judges': 9},
        # 24: {'name': 'Мужчины и женщины сальса', 'min_category': 7, 'otd_num' : 11, 'n_judges': 9}
    #}

    relatives_list = [
        {'id': 1,
         'relative_id': 3},
        {'id': 3,
         'relative_id': 1}
    ]

    black_list = [
        {'group_number': 21,
         'id': 1},
        {'group_number': 21,
         'id': 5},
        {'group_number': 21,
         'id': 67}
    ]

    judge_counter_list = [{'otd_num': 11, 'id': i, 'jud_entries': 0} for i in range(1, 101)]
    return relatives_list, black_list, judge_counter_list

def get_all_judges_yana(compId):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            cur.execute(
               f"SELECT id, lastName, firstName, SPORT_Category, RegionId, Club, bookNumber FROM competition_judges WHERE compId = {compId}")  # выбираем только активных на данный момент судей
            data = cur.fetchall()
            return data

    except Exception as e:
        print(e)
        return 0

#преобразование категории судьи
def decode_category(category_name):

    judge_category = {
        'Всероссийская' :6,
        'Первая' : 5,
        'Вторая' : 4,
        'Третья' : 3,
        'Четвертая': 2
    }

    try:
        category_num = judge_category[category_name]
    except KeyError:
        return 10
    return category_num

#функция удаляет судей с категорией ниже минимальной для группы
def judges_category_filter(all_judges_list, min_category):
  all_judges_list_1 = all_judges_list.copy()
  for i in all_judges_list:
    if all_judges_list_1[i]['SPORT_Category_decoded'] < min_category:
      all_judges_list_1.pop(i, None)
  return all_judges_list_1

#функция предварительной обработки блэклиста - по номеру категории определяем судей с запретом, на выход - айдишники судей
def black_list_convert(category_number, black_list):
  category_black_list = []
  for i in black_list:
    if i['group_number'] == category_number:
      category_black_list.append(i['id'])
  return category_black_list

#функция удаляет судей с запретом на судейство в категории
def judges_black_list_filter(all_judges_list, category_black_list):
  all_judges_list_1 = all_judges_list.copy()
  for i in all_judges_list:
    if i in category_black_list:
      all_judges_list_1.pop(i, None)
  return all_judges_list_1

#функция генерирует случайного судью
def get_random_judge(group_all_judges_list):
  random_number = random.randint(0, len(group_all_judges_list.keys()) - 1) #генерация случайного индекса
  return group_all_judges_list[list(group_all_judges_list.keys())[random_number]] #достаем из общего списка судей параметры по судье исходя из случайного индекса

#функция удаляет всех судей с таким же клубом
def delete_club_from_judges(list_of_judges, club_name):
  dict_for_pop = list_of_judges.copy()
  for i in list(list_of_judges.values()):
    if i['Club'] == club_name:
      dict_for_pop.pop(i['id'], None)
  return dict_for_pop


#функция удаляет всех судей с таким же регионом
def delete_region_from_judges(list_of_judges, region_id):

  dict_for_pop = list_of_judges.copy()
  for i in list(list_of_judges.values()):
    if i['RegionId'] == region_id:
      dict_for_pop.pop(i['id'], None)
  return dict_for_pop


# преобразование списка родственников после загрузки
def relatives_list_change(relatives_list):

    relatives_dict = {}
    for i in relatives_list:
        if i['id'] in relatives_dict:
            relatives_dict[i['id']].append(i['relative_id'])
        else:
            relatives_dict[i['id']] = list()
            relatives_dict[i['id']].append(i['relative_id'])

    return relatives_dict