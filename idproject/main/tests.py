import requests, urllib.request, json, re, html
from bs4 import BeautifulSoup
from datetime import date

with urllib.request.urlopen("https://study.miigaik.ru/api/v1/groups") as url:
    data = json.load(url)
    data2 = str(data)
    counter = data2.count('}')

year_today = str(date.today())[:4]
cici = 0
faculty_t=''
course_t=''
group_t=''
coper = 0
with open('list_by_faculties,_courses_and_groups.txt', 'w', encoding='utf-8') as f:
    with open('layout.html', 'w', encoding='utf-8') as new:
        new.write(f'{{% load static %}}\n<!doctype html>\n<html lang="ru">\n<head>    \n<meta charset="UTF-8">    \n<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">    \n<meta http-equiv="X-UA-Compatible" content="ie=edge">    \n<title>{{% block title %}}{{% endblock %}}</title>    \n<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">    \n<link rel="stylesheet" href="{{% static ''main/css/main.css'' %}}">    \n<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.2/css/all.css">    \n<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.1/css/fontawesome.min.css">    \n<meta http-equiv="X-UA-Compatible" content="IE=edge">    \n<meta name="viewport" content="width=device-width, initial-scale=1.0">    \n<link rel="stylesheet" href="style.css">\n<script type="text/javascript" src="https://ff.kis.v2.scr.kaspersky-labs.com/FD126C42-EBFA-4E12-B309-BB3FDD723AC1/main.js?attr=DGYy6kpCaK9lUmlBYpfwaFwkurK-02hbokS6esVpl05H9Bzwiz9fihPKbkAkVem039BXqApAtAWWnDN8mJ9F2obD8APw_og2uammpnVYSyE1JyhgOWeR7cSyJxrw5f7vijSRSbJ1zDV-1XswQtq85i08O7REH__4Ocmex91W-naZYZlGgyY489d2cCEwBxtAwVrOJX1frUfLaCaMZPMAIOH3vIMGRjyXyvILbm3ogRbRVdW1sYvbEBU8zRP-r6RxzM1yYVvEyL20wUv0t11L2g" charset="UTF-8"></script></head>\n<body>\n<nav>  \n<ul class="menu">    \n<li><a href="/" >Главная</a>    \n</li>      \n<li><a href="{% url ''admin'' %}">Авторизация</a></li>      \n<li><a href="">Расписание</a>\n<ul class="submenu">')
        for i in data:
            group = i.get("name")
            faculty = re.search("-(.+?)-", group)
            if faculty:
                faculty = faculty.group(1)
            course = int(year_today) - int(str(group)[:4])
            if course == 0:
                course = 1
            while coper == 0:
                if faculty_t == faculty:
                    new.write(f'<li><a href="">{faculty}</a><ul class="submenu">\n')
                if course_t == course:
                    new.write(f'<li><a href="">{course} курс</a><ul class="submenu">\n')
                coper = 1
            f.write(f"{faculty}, {course}, {group}\n")
            if faculty_t != faculty:
                new.write(f'</ul>\n</li>\n<li><a href="">{faculty}</a><ul class="submenu">\n')
            if course_t != course:
                new.write(f'</ul>\n</li>\n<li><a href="">{course} курс</a><ul class="submenu">\n')
            if group_t != group:
                new.write(f'<li><a href=gr{cici}>{group}</a></li>\n')
            else: break
            faculty_t = faculty
            course_t = course
            group_t = group
            cici += 1
        new.write(f'</ul>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><a href="{{% url ''about'' %}}">Разработчики</a></li>\n<li><a href="{% url ''writetous'' %}">Техподдержка</a></li>\n</ul>\n</nav>\n<main>\n{% block content %}\n{% endblock %}\n</main>\n</body>')
