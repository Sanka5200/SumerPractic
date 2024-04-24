import urllib.request,  re, sqlite3, json, requests # Импорты библиотек

from urllib.parse import quote, urlsplit, urlunsplit
from bs4 import BeautifulSoup
from datetime import date
from django.shortcuts import render

connection = sqlite3.connect('my_database.db') # Создание и манипуляции с базой данных
cursor = connection.cursor()
cursor.execute('''DROP TABLE IF EXISTS layout''') # Удаляем БД при повторном запуске, если она есть. Если нет - не удаляем. Процедура аналогична обновлению БД
cursor.execute('''
CREATE TABLE IF NOT EXISTS layout( 
facility VARCHAR (60) NOT NULL,
gruppa VARCHAR (60) NOT NULL,
course VARCHAR (60) NOT NULL,
day VARCHAR (60) NOT NULL,
lesson VARCHAR (60) NOT NULL,
week_type VARCHAR (60) NOT NULL,
subgroup VARCHAR (60) NOT NULL,
subject VARCHAR (60) NOT NULL,
teacher VARCHAR (60) NOT NULL,
classroom VARCHAR (60) NOT NULL,
lesson_type VARCHAR (60) NOT NULL,
additional_info VARCHAR (60) NOT NULL
)
''') # Создаем БД, если она еще не создана. Я использовал VARCHAR (60), так как строки врядли будут длиннее, а использование TEXT - нецелесообразно
cursor.execute('CREATE INDEX IF NOT EXISTS idx_facility ON layout (facility)') # Создаем индексы для каждого атрибута
cursor.execute('CREATE INDEX IF NOT EXISTS idx_gruppa ON layout (gruppa)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_course ON layout (course)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_day ON layout (day)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_lesson ON layout (lesson)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_week_type ON layout (week_type)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_subgroup ON layout (subgroup)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_subject ON layout (subject)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_teacher ON layout (teacher)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_classroom ON layout (classroom)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_lesson_type ON layout (lesson_type)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_additional_info ON layout (additional_info)')

def iri_to_uri(iri): # Вспомогательная функция для адекватного пользования ссылками, ибо русские буквы помещать в ссылки напрямую - отказывается
    parts = urlsplit(iri)
    uri = urlunsplit((
        parts.scheme,
        parts.netloc.encode('idna').decode('ascii'),
        quote(parts.path),
        quote(parts.query, '='),
        quote(parts.fragment),
    ))
    return uri
with urllib.request.urlopen("https://study.miigaik.ru/api/v1/groups") as url:
    data = json.load(url)
for i in data:
    schedule_link = i.get("schedule-link")
    adress = 'https://study.miigaik.ru/api/v1/' + str(schedule_link)
    adress = iri_to_uri(adress)
    adress = adress.replace('%26','&')
    with urllib.request.urlopen(adress) as url1:
        rasp = json.load(url1)
        fac_cour = re.search(r"faculty=(\w+)&course=(\w+)&", schedule_link)
        faculty = fac_cour[1]
        course = fac_cour[2]
        gruppa = i.get("name")
        for week in rasp:
            week_type = week
            for day in rasp[week]:
                for subs in rasp[week][day]: # Заполняем БД
                    day = subs.get("day")
                    lesson = subs.get("lesson")
                    week_type = subs.get("week-type")
                    subgroup = subs.get("subgroup")
                    subject = subs.get("subject")
                    teacher = subs.get("teacher")
                    classroom = subs.get("classroom")
                    lesson_type = subs.get("lesson-type")
                    additional_info = subs.get("additional-info")
                    cursor.execute(f'''INSERT INTO layout (facility, gruppa, course, day, lesson, week_type, subgroup, subject, teacher, classroom, lesson_type, additional_info)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (faculty, gruppa, course, day, lesson, week_type, subgroup, subject, teacher, classroom, lesson_type, additional_info))

connection.commit()
connection.close()
def GetGroup(request, gruppa):
    return render(request, 'main/Расписание/' + gruppa + '.html')

year_today = str(date.today())[:4]
cici = 0
faculty_t = '' # Вспомогательная переменная для получения факультета
course_t = '' # Вспомогательная переменная для получения курса
group_t = '' # Вспомогательная переменная для получения группы
with open('list_by_faculties,_courses_and_groups.txt', 'w', encoding='utf-8') as f:
    with open('templates/main/layout.html', 'w', encoding='utf-8') as new:
        new.write(f'{{% load static %}}\n<!doctype html>\n<html lang="ru">\n<head>    \n<meta charset="UTF-8">    \n<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">    \n<meta http-equiv="X-UA-Compatible" content="ie=edge">    \n<title>{{% block title %}}{{% endblock %}}</title>    \n<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">    \n<link rel="stylesheet" href="{{% static \'main/css/main.css\' %}}">\n<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.2/css/all.css">    \n<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.1/css/fontawesome.min.css">    \n<meta http-equiv="X-UA-Compatible" content="IE=edge">    \n<meta name="viewport" content="width=device-width, initial-scale=1.0">    \n<link rel="stylesheet" href="style.css">\n<script type="text/javascript" src="https://ff.kis.v2.scr.kaspersky-labs.com/FD126C42-EBFA-4E12-B309-BB3FDD723AC1/main.js?attr=DGYy6kpCaK9lUmlBYpfwaFwkurK-02hbokS6esVpl05H9Bzwiz9fihPKbkAkVem039BXqApAtAWWnDN8mJ9F2obD8APw_og2uammpnVYSyE1JyhgOWeR7cSyJxrw5f7vijSRSbJ1zDV-1XswQtq85i08O7REH__4Ocmex91W-naZYZlGgyY489d2cCEwBxtAwVrOJX1frUfLaCaMZPMAIOH3vIMGRjyXyvILbm3ogRbRVdW1sYvbEBU8zRP-r6RxzM1yYVvEyL20wUv0t11L2g" charset="UTF-8"></script></head>\n<body>\n<nav>  \n<ul class="menu">    \n<li><a href="/" >Главная</a>    \n</li>      \n<li><a href="{{% url \'admin\' %}}">Авторизация</a></li>      \n<li><a href="">Расписание</a>\n<ul class="submenu">')
        for i in data:
            group = i.get("name")
            faculty = re.search("-(.+?)-", group)
            if faculty:
                faculty = faculty.group(1)
                course = int(year_today) - int(str(group)[:4])
            if course == 0:
                course = 1
            f.write(f"{faculty}, {course}, {group}\n")
            if faculty_t == '':
                new.write(f'<li><a href="">{faculty}</a><ul class="submenu">\n')
            elif faculty_t != faculty and faculty_t != '':
                new.write(f'</ul>\n</li>\n</ul>\n</li>\n<li><a href="">{faculty}</a><ul class="submenu">\n')
            if course_t == '' or course == 1 and course_t != 1:
                new.write(f'<li><a href="">{course} курс</a><ul class="submenu">\n')
            elif course_t != course and course_t != '' and course != 1:
                new.write(f'</ul>\n</li>\n<li><a href="">{course} курс</a><ul class="submenu">\n')
            if group_t != group:
                new.write(f'<li><a href=gr{cici}>{group}</a></li>\n')
            else:
                break
            faculty_t = faculty
            course_t = course
            group_t = group
            cici += 1
        new.write(f'</ul>\n</li>\n</ul>\n</li>\n</ul>\n</li>\n<li><a href="{{% url \'about\' %}}">Разработчики</a></li>\n<li><a href="{{% url \'writetous\' %}}">Техподдержка</a></li>\n</ul>\n</nav>\n<main>\n{{% block content %}}\n{{% endblock %}}\n</main>\n</body>')
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

list_schedule = open('list_by_faculties,_courses_and_groups.txt', 'r', encoding='utf-8') # Лист с группами, если нужно просмотреть
number_of_lines = len(list_schedule.readlines())
list_schedule.seek(0)

urls_update = open('urls.py', 'w', encoding='utf-8') # Автоматически заполняет ссылки
string = "from django.urls import path\nfrom . import views\n\nurlpatterns = [\n    path('', views.index, name='home'),\n    path('about', views.about, name='about'),\n    path('admin', views.admin, name='admin'),\n    path('writetous', views.writetous, name='writetous'), \n     path('GetGroup', views.GetGroup, name='GetGroup'),\n"
urls_update.write(string)

views_update = open('views.py', 'w', encoding='utf-8') #
string = "from django.shortcuts import render\ndef index(request):\n    return render(request, 'main/index.html')\ndef about(request):\n    return render(request, 'main/about.html')\ndef writetous(request):\n    return render(request, 'main/writetous.html')\ndef admin(request):\n    return render(request, '127.0.0.1:8000/admin')\n"
views_update.write(string)
number_of_group = 0

for string in range(number_of_lines):
    schedule = list_schedule.readline().rstrip()
    if schedule.strip():
        schedule = tuple(schedule.split(','))
        data = {
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
        # string = 'gr' + str(number_of_group)
        # number_of_group += 1
        # urls_update.write("    path('" + string + "', views." + string + ", name='" + string + "'),\n")
        # views_update.write("def " + string + "(request):\n")
        # views_update.write("    return render(request,'" + file_path[10:] + "')\n")

        f = open(file_path, 'w', encoding='utf-8')
        f.write("{% extends 'main/layout.html' %}\n{% block title %}Расписание{% endblock %}\n{% block content %}\n")
        f.write(need)
        f.write("\n{% endblock %}")
        f.close()
views_update.write(f"def GetGroup(request, gruppa):\n    return render(request, 'main/Расписание/' + gruppa + '.html')\n")
urls_update.write(']')
urls_update.close()
views_update.close()
list_schedule.close()