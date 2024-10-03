from .models import CompetitionJudges
from GenerationLists.serializers import *
import random
import json


def get_ans(data):
    json_end = dict()

    group_list, relatives_list, black_list, judge_counter_list = get_future_tables()
    comp_region_id = data['regionId']
    relatives_dict = relatives_list_change(relatives_list)

    # 1. сортировка входящего списка групп в зависимости от требуемой для судейства категории
    group_list = dict(sorted(group_list.items(), key=lambda item: item[1]['min_category'], reverse=True))

    # 2. запрашиваем и обрабатываем список судей
    ans = get_all_judges_yana(data['compId'])

    all_judges_list = {}  # преобразуем словарь для более удобной работы, создаем общий список доступных для выбора судей с параметрами

    for i in ans:
        i['SPORT_Category_decoded'] = decode_category(i['sport_category'])
        all_judges_list[i['id']] = i

    s = 0

    # 3. начинаем работать с каждой группой из переданного списка
    for i in group_list:

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
        min_category = group_list[i]['min_category']
        otd_num = group_list[i]['otd_num']
        n_judges = group_list[i]['n_judges']

        group_number = i
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
                    if try_judge_data['regionid'] in regions:
                        regions[try_judge_data['regionid']] += 1
                        if try_judge_data['regionid'] == comp_region_id and regions[try_judge_data[
                            'regionid']] == n_jud_comp_region:  # если судья из "домашнего" региона и при его добавлении лимит для региона исчерпан
                            # ФУНКЦИЯ удаляем всех судей с таким же регионом
                            group_all_judges_list = delete_region_from_judges(group_all_judges_list,
                                                                              try_judge_data['regionid'])
                        elif try_judge_data['regionid'] != comp_region_id and regions[
                            try_judge_data['regionid']] == n_jud_other_region:
                            # ФУНКЦИЯ удаляем всех судей с таким же регионом
                            group_all_judges_list = delete_region_from_judges(group_all_judges_list,
                                                                              try_judge_data['regionid'])
                    else:
                        regions[try_judge_data['regionid']] = 1

                    # удалили всех с таким же клубом
                    group_all_judges_list = delete_club_from_judges(group_all_judges_list, try_judge_data['club'])

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
            for i in group_finish_judges_list:
                json_end['judge_id'] = all_judges_list[i]['id']
            print('Распределение регионов', regions)
        else:
            sucess_result = 0
            json_end['group_number'] = group_number
            json_end['status'] = "fail"

    return json.loads(json.dumps(json_end))

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
    group_list = {
        21: {'name': 'Мужчины и женщины латиноамериканская программа', 'min_category': 8, 'otd_num': 11,
             'n_judges': 11},
        22: {'name': 'Мужчины и женщины европейская программа', 'min_category': 7, 'otd_num': 11, 'n_judges': 9},
        # 23: {'name': 'Мужчины и женщины двоеборье', 'min_category': 5, 'otd_num' : 11, 'n_judges': 9},
        # 24: {'name': 'Мужчины и женщины сальса', 'min_category': 7, 'otd_num' : 11, 'n_judges': 9}
    }

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
    return group_list, relatives_list, black_list, judge_counter_list

def get_all_judges_yana(compId):
    queryset = CompetitionJudges.objects.filter(compid=compId)
    serializer = JudgesSerializer(queryset, many=True)
    return serializer.data

#преобразование категории судьи
def decode_category(category_name):

    judge_category = {
        'Всероссийская' :8,
        'Первая' : 7,
        'Вторая' : 6,
        'Третья' : 5
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
    if i['club'] == club_name:
      dict_for_pop.pop(i['id'], None)
  return dict_for_pop


#функция удаляет всех судей с таким же регионом
def delete_region_from_judges(list_of_judges, region_id):

  dict_for_pop = list_of_judges.copy()
  for i in list(list_of_judges.values()):
    if i['regionid'] == region_id:
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