import hashlib
import random
import time

import vk

from stdex import *

global zakazy
global q
api = vk.API(
    vk.AuthSession(app_id='4580399', user_login='hottabbe@gmail.com', user_password='Hottab1234!'),
    lang='ru', v='5.62', scope='messages')

if hot_api() < 1.53:
    print('ВЕРСИЯ API УСТАРЕЛА,ЭТО МОЖЕТ ВЫЗВАТЬ БАГИ В РАБОТЕ СКРИПТА!!!!!\a', True, 0, True)
    if int(input('1. Выйти из скрипта\n2. Продолжить работу\n--> ', '12')) == 1:
        sys.exit()


def formatter(values, length, delim):
    for i in range(len(values)):
        values[i] = str(values[i])
        if len(values[i]) < length[i]:
            values[i] = values[i] + ' ' * (length[i] - len(values[i]) - 1) + delim
        else:
            values[i] = values[i][0:length[i] - 1] + delim
    return values


class orders:
    @staticmethod
    def get():
        zakazy = readcfg('orders.hs')
        q = {}
        for every in zakazy:
            qw = requests.get(
                'http://roboliker.ru/api/get_order/%s/3858f62230ac3c915f300c664312c63f.json' % every).json()
            try:
                q[every] = [qw['url'], zakazy[every].split(';')[1], '%s/%s' % (qw['like_ready'], qw['like_count']),
                            zakazy[every].split(';')[0]]
            except:
                pass
        return q

    def add(order, tip, target):
        zakazy = readcfg('orders.hs')
        zakazy[order.json()['id']] = '%s;%s' % (tip, target)
        writecfg('orders.hs', zakazy)
        return True

    @staticmethod
    def suc_del():
        zak = {}
        q = orders.get()
        for every in q:
            if q[every][1].split('/')[0] != q[every][1].split('/')[1]:
                zak[every] = '%s;%s' % (q[every][0],q[every][1])
        writecfg('orders.hs',zak,False)
        return orders.get()


hash_access = '3858f62230ac3c915f300c664312c63f'  # 'foobar'
global dev_id
global sex
global key_
global country
dev_id = ''  # id устройства
types = ['like_photo', 'fun', 'group', 'like_post', 'like_comment']
sex = ['', 'girl', 'boy', '']
country = ['', 'All', 'Ukraine', 'Russia', 'BY', 'Москва']


def reg_user(vk_id_rand):  # Регистрация пользователя
    global key_
    global dev_id
    for i in range(32):
        dev_id += random.choice(string.ascii_lowercase + string.digits)
    md5_key = md5hash('liker' + dev_id + 'android_' + key_ + vk_id_rand + '0')
    md5_version = md5hash('version2' + 'android_' + key_ + vk_id_rand)
    args = {
        "i_user": {
            "balans": 0,
            "vk_id": 'android_' + key_ + vk_id_rand,
            "device_id": dev_id
        },
        "hesh_access": hash_access,
        "type": "free",
        "male": "girl",
        "version": md5_version,
        "key": md5_key
    }
    r = requests.post('http://api.roboliker.ru/ios_api/i_users_new.json', json=args)
    return r.json()


def auth_user(vk_id):  # Авторизация пользователя.
    global key_
    md5_key = md5hash('version2' + 'android_' + key_ + vk_id)
    r = requests.get(
        'http://api.roboliker.ru/ios_api/i_users/android_' + key_ + vk_id + '/' + md5_key + '/' + hash_access + '.json')
    resp = r.json()
    try:
        return resp['balans'], resp['promocod'], resp['promo_coins_count']
    except TypeError:
        return 0, input('Не удалось получить пользователя\nВведите промо-код : ', '1234567890', 0), 30


def get_promo(vk_id_rand, code):  # Активация промокода.
    global key_
    md5_key = md5hash('liker' + 'android_' + key_ + vk_id_rand + code)
    args = {
        "hesh_access": hash_access,
        "code": code,
        "vk_id": 'android_' + key_ + vk_id_rand,
        "key": md5_key
    }
    r = requests.post('http://api.roboliker.ru/ios_api/i_users/send_promocode.json', json=args)
    if r.text == '{"status":true}':
        return True


def add_task(vk_id, target_id, count, type, arg='', sex='', country='', age = ''):  # Добавление задания
    global key_
    url = ['https://vk.com/id%s?z=photo%s_%s' % (target_id, target_id, arg),
           'https://vk.com/id%s' % target_id,
           'https://vk.com/public%s' % arg,
           'https://vk.com/wall%s_%s' % (target_id, arg),
           'https://vk.com/wall%s_%s' % (target_id, arg)]
    messages = {
        'like_photo': 'Задание на %s лайков на эту фотографию активировано! Спасибо за использование . За информацией '
                      'напишите ему : vk.com/hottabbe' % count,
        'like_post': 'Задание на %s лайков на этот пост активировано! Спасибо за использование . За информацией '
                     'напишите ему : vk.com/hottabbe' % count,
        'like_comment': 'Задание на %s лайков на комментарий vk.com/wall%s_%s активировано! Спасибо за использование . За информацией '
                        'напишите ему : vk.com/hottabbe' % (count, target_id, arg),
        'fun': 'Задание на %s подписчиков активировано! Спасибо за использование. За информацией напишите ему : '
               'vk.com/hottabbe' % count,
        'group': 'Задание на %s подписчиков в группу vk.com/public%s активировано! Спасибо за использование. За '
                 'информацией напишите ему : vk.com/hottabbe' % (count, arg)}
    url = url[type]
    type = types[type]
    args = {
        "hesh_access": hash_access,
        "social": "vk",
        "type": type.split('_')[0],
        "url": url,
        "order_rate": "4",
        "country_name": country,
        "like_count": count,
        "male": sex,
        "description": "vkandroidfree",
        "external_user_id": vk_id,
        "age": age
    }
    r = requests.post('http://api.roboliker.ru/api/create_order', json=args)
    if 'id' in r.json():
        order_id = r.json()['id']

        def activate_order(vk_id, order_id):  # Проверка добавления задания
            args = {
                "hesh_access": hash_access,
                "order_id": order_id,
                "vk_id": 'android_' + key_ + vk_id,
                "version": md5hash('version2' + str(order_id)),
                "key": md5hash('liker' + str(order_id) + 'android_' + key_ + str(vk_id))
            }
            t = requests.post('http://api.roboliker.ru/ios_api/i_users/activate_order.json', json=args)
            if t.json()['status'] is True:
                return True
            else:
                return False

        if activate_order(vk_id, order_id) is True:
            try:
                try:
                    if type.split('_')[1] == 'photo':
                        api.messages.send(user_id=target_id, message=messages[type],
                                          attachment='photo%s_%s' % (target_id, arg))
                    elif type.split('_')[1] == 'post':
                        api.messages.send(user_id=target_id, message=messages[type],
                                          attachment='post%s_%s' % (target_id, arg))
                    elif type.split('_')[1] == 'comment':
                        api.messages.send(user_id=target_id, message=messages[type])
                except IndexError:
                    api.messages.send(user_id=target_id, message=messages[type])
            except:
                pass
            orders.add(order=r, tip=type, target='vk.com/id%s' % target_id)
            return True


def md5hash(key):  # Генерация md5 хэша.
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    return m.hexdigest()


def stream(code):
    vk_id_rand = str(random.randint(1, 999999999))
    reg_user(vk_id_rand)
    if get_promo(vk_id_rand, code) is True:
        return True


def enter():
    global key_
    key = int(input('\n\n1 - Вконтакте\n2 - Instagram\n--> ', '12', 1))
    if key == 1:
        key_ = 'vk'
        main_vk()
    else:
        key_ = 'ig'
        main_ig()
    return key_


def force_add(count, target_id, type, arg, sex, country,age):
    global dev_id
    while True:
        vk_id = str(random.randint(1, 999999999))
        print('1. Попытка регистрации пользователя с ID %s' % vk_id, False, 1)
        if reg_user(vk_id)['device_id'] == dev_id:
            break
    print('2. Получаю промо-код для пользователя ID %s' % vk_id, True, 1)
    vars_ = list(auth_user(vk_id))
    factor = 8
    if sex != '':
        factor += 1
    if country != 'All':
        factor += 1
    if age != 0:
        factor += 1
    cycles = int(count) * factor
    print('3. Накручиваю баланс для добавления задания (Необходимо %s коинов)\n' % cycles, True, 1)
    vars_[0] = int(vars_[0])
    vars_[2] = int(vars_[2])
    while vars_[0] < cycles:
        time_ = time.time()
        if stream(vars_[1]):
            vars_[0] += vars_[2]
            s = (time.time() - time_) * ((cycles - vars_[0]) / 30)
            h = s // 3600
            s %= 3600
            m = s // 60
            s %= 60
            print('Накручено %s из %s. Осталось примерно %s:%s:%s' % (vars_[0], cycles, int(h), int(m), int(s)), False,
                  4)
    print('4. Добавляю задание....', False, 1)
    if add_task(vk_id, target_id, count, type, arg,sex,country,age):
        print('УСПЕШНО!\a', True, 1)
        return True
    else:
        print('Неудача,попробуйте изменить параметры задания.....', True, clr=True, color=0)
        enter()


def get_orders():
    print('ПОДОЖДИТЕ,ИДЕТ ГЕНЕРАЦИЯ СПИСКА ЗАКАЗОВ...............', frame=True, color=4, clr=True)
    zakaz = orders.get()
    for every in zakaz:
        zakaz[every] = formatter(zakaz[every], [45, 45, 15, 15], '┃')
    head = formatter(['ID заказа', 'Ссылка на заказ', 'Заказчик', 'Выполнено', 'Тип заказа'], [15, 45, 45, 15, 15], '┃')
    string = ''
    for every in head:
        string += every
    print(string, False, 5, True)
    print('━' * 14 + '╋' + '━' * 44 + '╋' + '━' * 44 + '╋' + '━' * 14 + '╋' + '━' * 14 + '┫')
    for every in zakaz:
        if zakaz[every][2].split('/')[1].split(' ')[0] == zakaz[every][2].split('/')[0]:
            col = '\x1b[42m'
        elif zakaz[every][2].split('/')[1] != zakaz[every][2].split('/')[0]:
            col = '\x1b[41m'
        string = formatter([every], [15], '┃')[0]
        for ever in zakaz[every]:
            string += ever
        print(col + string + '\x1b[0m', True, 2)
        print('━' * 14 + '╋' + '━' * 44 + '╋' + '━' * 44 + '╋' + '━' * 14 + '╋' + '━' * 14 + '┫\x1b[0m')
    print('━' * 14 + '┻' + '━' * 44 + '┻' + '━' * 44 + '┻' + '━' * 14 + '┻' + '━' * 14 + '┛')
    print('\n\n\n\n\n\nНАЖМИТЕ TAB ДЛЯ ОБНОВЛЕНИЯ\nНАЖМИТЕ ENTER ДЛЯ ВЫХОДА', color=2)
    we = inputos()
    if we == chr(9):
        orders.suc_del()
        get_orders()
    elif we == chr(10):
        print('', clr=True)
        main_vk()


def main_vk():  # Основная функция.
    global sex, country
    print('Меню:\n1. Накрутка баланса\n2. Добавить задание\n3. Информация о пользователе\n4. Список заказов\n5. Проверить обновления', False,
          4, True, frame=True)
    opt = int(input('--> ', '12345'))
    if opt == 1:
        vk_id = input('\nВведите ваш ID ВК: ', '1234567890')
        balance, code, promo_count = auth_user(vk_id)
        print('\nНа вашем балансе %s баллов.\nПромокод: %s\nБаллов за одного друга: %s\n\n' % (
            balance, code, promo_count))
        cycles = int((int(input('До какого баланса докрутить? \n --> ', '1234567890')) - int(balance)) / promo_count)
        for i in range(cycles + 1):
            time_ = time.time()
            if stream(code) is True:
                balance += promo_count
                s = (time.time() - time_) * (cycles - i)
                h = s // 3600
                s = s % 3600
                m = s // 60
                s = s % 60
                print('%s +%s монет. Текущий баланс %s монет. Осталось примерно %s:%s:%s    ' % (
                    time.strftime('[%H:%M:%S]'), promo_count, balance, int(h), int(m), int(s)),
                      False, 1, False, True)
    elif opt == 2:
        print(
            '1. Накрутка лайков\n2. Накрутка подписчиков\n3. Накрутка подписчиков в группу\n4. Накрутка лайков на '
            'запись\n5. Накрутка лайков на комментарии (тест)',
            color=4, frame=True)
        type = int(input('--> ', '12345'))
        if type in {1, 4, 5}:
            count = input('Сколько лайков накрутить: ', '1234567890')
            target_id = input('ID человека/группы: ', '1234567890-')
            if type == 5:
                arg = '%s?reply=%s' % (input('ID записи: ', '1234567890'), input('ID комментария: ', '1234567890'))
            else:
                arg = input('ID записи/фото/комментария: ', '1234567890')
        elif type in {2, 3}:
            count = input('Сколько человек накрутить: ', '1234567890')
            target_id = input('ID человека (При накрутке в группу ID заказчика) : ', '1234567890')
            arg = ''
            if type == 3:
                arg = input('ID группы (без минуса) : ', '1234567890')
        print('Выберите пол потенциальных исполнителей\n1. Женский\n2. Мужской\n3. Любой', color=4, frame=True)
        sex_ = sex[int(input('--> ', '123'))]
        print('Выберите страну потенциальных исполнителей\n1. Любая\n2. Украина\n3. Россия\n4. Белоруссия', color=4, frame=True)
        country_ = country[int(input('--> ', '1234'))]
        print('Выберите возраст потенциальных исполнителей\n1. Не имеет значения\n2. До 18 лет\n3. Старше 18 лет', color=4, frame=True)
        age = int(input('--> ','123')) - 1
        if force_add(count, target_id, type - 1, arg, sex_, country_,age) is True:
            print('Задание успешно добавлено!', False, 1)
        else:
            print('При добавлении задания произошла ошибка!', False, 0)
            main_vk()
    elif opt == 3:
        vk_id = input('ID пользователя: ', '1234567890')
        info = auth_user(vk_id)
        print('Баланс: %s\nПромокод: %s' % (info[0], info[1]), False, 4)
    elif opt == 4:
        get_orders()
    elif opt == 5:
        print('Проверка обновлений......')
        updater('123.py', 'https://raw.githubusercontent.com/hottabbe/roboliker/master')
        print('Проверка обновлений API...')
        updater('stdex.py', 'https://raw.githubusercontent.com/hottabbe/stdex/master')


def main_ig():  # Основная функция.
    while True:
        print('\n\nМеню:\n1. Накрутка баланса', False, 4)
        opt = int(input('--> '), '1')
        if opt == 1:
            break
        else:
            continue
    if opt == 1:
        code = input('\nВведите ваш промо-код: ', '1234567890')
        balance = 0
        while True:
            if stream(code) is True:
                balance += 30
                print('Добавлено на баланс %s монет' % balance, False, 1)


if __name__ == '__main__':
    print('Проверка обновлений......')
    updater('123.py', 'https://raw.githubusercontent.com/hottabbe/roboliker/master')
    print('Проверка обновлений API...')
    updater('stdex.py', 'https://raw.githubusercontent.com/hottabbe/stdex/master')
    try:
        print('Приложение для накрутки баланса в приложении Мой Рейтинг в ВК\n'
              'https://play.google.com/store/apps/details?id=ru.like.vs', True, random.randint(0, 9), frame=True)
        while True:
            enter()
    except KeyboardInterrupt:
        print('\n\nВыходим...', True, random.randint(0, 9))
