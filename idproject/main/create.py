import requests
from bs4 import BeautifulSoup

#Саня не лезь сюда, убьёт, комменатрии напишу позже

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://studydep.miigaik.ru',
    'Referer': 'http://studydep.miigaik.ru/semestr/index.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36',
}


list_schedule = open('list by faculties, courses and groups.txt', 'r', encoding='utf-8')
number_of_lines = len(list_schedule.readlines())
list_schedule.seek(0)

urls_update = open('urls.py', 'w', encoding='utf-8')
string = "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.index, name='home'),\n    path('about', views.about, name='about'),\n    path('admin', views.admin, name='admin'),\n    path('writetous', views.writetous, name='writetous'), \n"
urls_update.write(string)

views_update = open('views.py', 'w', encoding='utf-8')
string = "from django.shortcuts import render\ndef index(request):\n    return render(request, 'main/index.html')\ndef about(request):\n    return render(request, 'main/about.html')\ndef writetous(request):\n    return render(request, 'main/writetous.html')\ndef admin(request):\n    return render(request, '127.0.0.1:8000/admin')\n"
views_update.write(string)

number_of_group = 0

for string in range(number_of_lines):
    schedule = list_schedule.readline().rstrip()
    if schedule.strip(): # проверка на пустую строку
        schedule = tuple(schedule.split(',')) # конвертация строки в кортеж из трех элементов
        data = { # создание словаря из картежа(для запроса)
            'fak': schedule[0].rstrip().lstrip(),
            'kurs': schedule[1].rstrip().lstrip(),
            'grup': schedule[2].rstrip().lstrip(),
        }

        response = requests.post('http://studydep.miigaik.ru/semestr/index.php', headers=headers, data=data,
                                 verify=False)

        soup = BeautifulSoup(response.text, "html.parser")
        page = soup.findAll('table', class_='t')
        file_name = str(schedule[2].rstrip().lstrip())
        need = str(page[0])
        need = need.replace('<th>прим.</th>', '<th>комментарий</th>')
        need = need.replace(' bgcolor="#EAEDEE"', '')
        need = need.replace('<th>П-г</th>', '<th>Подгруппы</th>')
        need = need.replace('bgcolor="#ffffaa"', '')
        file_path = 'templates/main/Расписание/' + file_name + '.html'
        string = 'gr' + str(number_of_group)
        number_of_group += 1
        urls_update.write("    path('" + string + "', views." + string + ", name='" + string + "'),\n")
        views_update.write("def " + string + "(request):\n")
        views_update.write("    return render(request,'" + file_path[10:] + "')\n")

        f = open(file_path, 'w', encoding='utf-8')
        f.write("{% extends 'main/layout.html' %}\n{% block title %}Расписание{% endblock %}\n{% block content %}\n")
        f.write(need)
        f.write("\n{% endblock %}")
        f.close()
urls_update.write(']')
urls_update.close()
views_update.close()
list_schedule.close()