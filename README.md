Данная ветка пренадлежит Кубицкому А. 2022-ФГиИБ-ИБ-1б.
Нашей задачей являлось написание сайта с расписанием ВУЗа.
Критерии:
1) Наличие ТГ бота
2) Адаптивный интерфейс
3) Система управления ролями
4) Черно-белая тема

Запускать программу лучше сразу из папки "idproject".
ТГ бот запускается отдельно, воизбежанеи ошибок. Сам бот сообщает об изменениях в расписании, если они присутствуют. Также запросить информацию об изменениях можно вручную при помощи одноименной кнопки.
После запуска сайта мы увидим страницу с вкладками:
Главная - Добро пожаловать
Авторитзация - здесь реализована система управления с базой данных + черно-белое оформление.
пользователь: admin, парооль - Sanka5200TOP. Уже выдана роль администратора.
Расписание - собственно, расмписание групп.
Разработчики - разработчики сайта
Техподдержка - никакой актуальной информации. Она будет, если понадобится.
Перед запуском сайта следует запустить файл "\main\create.py", который автоматически распарсит расписание и внесет правки в сам сайт в "\main\urls.py" и в "\main\views.py", а так же обновит файлы в папке "\main\templates\main\Расписание", если же они отсутствуют - создаст новые.
Для запуска сайта, как уже говорилось, следует находиться в директории "idproject" - воспользоваться командой 'python manage.py runserver'.
