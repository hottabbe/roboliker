import requests
import sys,os
params = {'pass': input('Введите пароль доступа для загрузки : ')}
r = requests.post('https://hottabbe.000webhostapp.com/downloader.php',params).text
if r != 'НЕТ ДОСТУПА':
    name = input('Введите желаемое имя файла скрипта : ')
    file = open(name,'w+',encoding='utf-8')
    file.write(r)
    file.close()
    print('Скрипт накрутки загружен\nЗагрузка API....')
    api = open('stdex.py','w+',encoding = 'utf-8')
    api.write(requests.get('https://hottabbe.000webhostapp.com/stdex.py').text)
    api.close()
    input('API загружен\nНажмите Enter для запуска...')
    if sys.platform == 'win32':
        os.system('%s/%s' % (os.getcwd(), name))
    else:
        os.system('python3 %s/%s' % (os.getcwd(), name))
else:
    input('НЕВЕРНЫЙ ПАРОЛЬ\nENTER ДЛЯ ВЫХОДА')