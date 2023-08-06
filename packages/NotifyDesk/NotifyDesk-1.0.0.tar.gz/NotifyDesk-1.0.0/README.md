# NotifyDesk

EN:

The NotifyDesk library provides an easy way to send notifications in Linux.
To work, notify-send is used from the libnotify-bin package, which is preinstalled on most Linux systems.
The library is able to work together with QT/GTK.
You can use it to output important information, to notify about an error in the program, and in many other cases.

Arguments:
- title: defines the title of the notification. The default value is "Title"
- message: defines the text of the notification. The default value is "Message"
- delay: specifies the delay in seconds until the notification appears on the desktop. The default value is 0.
- icon: contains the path to the file in the format .ico to display the icon in the notification.
  To work correctly, you should use a relative path. The default value is None.
  The relative path is the path to the file relative to the current directory (the one in which the program is running)

P.S: title and message accept the str type (other types are not recommended, but it is also possible)); delay accepts int and float; icon accepts only str

Return values:
- True: when the notification is sent successfully.
- False: if the notification was sent unsuccessfully.

Usage examples:
   from NotifyDesk import push or import NotifyDesk ( In this case, you need to write NotifyDesk.push() )

1. Sending a standard notification:
   push(title="NotifyDesk", message="Test message")

2. Sending a notification with an icon:
   push(title="NotifyDesk", message="Test message", icon="path")
P.S: Instead of your own icon, you can use the built-in icons.
   A list with them (perhaps not complete) can be found on the project's GitHub ( https://github.com/krator3/NotifyDesk )
Or you can search for these names on the internet.

3. Sending a delayed notification:
   push(title="NotifyDesk", message="Test message", delay=6) # the notification will appear 6 seconds after calling the push() function

4. Sending a notification with a delay and an icon:
   push(title="NotifyDesk", message="Test message", delay=3, icon="path") # example of combining arguments

P.S: If the path to the icon is not correct and it is not the name of the built-in icon, then an icon will be displayed signaling this.



RU:

Библиотека NotifyDesk предоставляет простой способ отправки уведомлений в Linux.
Для работы используется notify-send из пакета libnotify-bin, который предустановлен в большинстве систем Linux.
Библиотека способна работать вместе с QT/GTK.
Вы можете использовать её для вывода важной информации, для уведомления об ошибке в программе и во многих других случаях.

Аргументы:
- title: определяет заголовок уведомления. Значение по умолчанию - "Title"
- message: определяет текст уведомления. Значение по умолчанию - "Message"
- delay: указывает задержку в секундах до появления уведомления на рабочем столе. Значение по умолчанию - 0.
- icon: содержит путь к файлу в формате .ico для отображения иконки в уведомлении.
  Для корректной работы следует использовать относительный путь. Значение по умолчанию - None.
  Относительный путь — это путь к файлу относительно текущего каталога (тот, в котором запускается программа)

P.S: title и message принимают тип str (другие типы не рекомендуется, но тоже можно) ); delay принимает int и float; icon принимает только str

Возвращаемые значения:
- True: при успешной отправке уведомления.
- False: при неудачной отправке уведомления.

Примеры использования:
   from NotifyDesk import push или import NotifyDesk ( В таком случае нужно писать NotifyDesk.push() )

1. Отправка стандартного уведомления:
   push(title="NotifyDesk", message="Тестовое сообщение")

2. Отправка уведомления с иконкой:
   push(title="NotifyDesk", message="Тестовое сообщение", icon="path")
   P.S: вместо собственной иконки вы можете использовать встроенные иконки.
   Список с ними (возможно не полный) вы сможете найти на GitHub проекта ( https://github.com/krator3/NotifyDesk )
   Или вы можете поискать эти названия в интернете.

3. Отправка уведомления с задержкой:
   push(title="NotifyDesk", message="Тестовое сообщение", delay=6) # уведомление появится через 6 секунд после вызова функции push()

4. Отправка уведомления с задержкой и иконкой:
   push(title="NotifyDesk", message="Тестовое сообщение", delay=3, icon="path") # пример комбинирования аргументов

P.S: Если путь до иконки не верен и это не является названием встроенной иконки, то будет отображаться значок, сигнализирующий об этом.
