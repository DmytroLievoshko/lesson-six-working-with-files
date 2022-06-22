# lesson-six-working-with-files

Задача
У многих на рабочем столе есть папка, которая называется как-то вроде "Разобрать". Как правило, разобрать эту папку руки никогда так и не доходят.

Этот скрипт разберет эту папку. Приложение проверяет расширение файла (последние символы в имени файла, как правило, после точки) и, в зависимости от расширения, принимаэт решение, к какой категории отнести этот файл.

Скрипт принимает один аргумент при запуске — это имя папки, в которой он будет проводить сортировку. Пример вызова скрипта - чтобы отсортировать папку /user/Desktop/Хлам, надо запустить скрипт командой python sort.py /user/Desktop/Хлам

Логика обработки папки содержится в отдельную функции.
Скрипт могжет пройти на любую глубину вложенности, функция обработки папок рекурсивно вызываэт сама себя, когда ей встречаются вложенные папки.
Скрипт проходит по указанной во время вызова папке и сортировать все файлы по группам:

изображения ('JPEG', 'PNG', 'JPG', 'SVG');
видео файлы ('AVI', 'MP4', 'MOV', 'MKV');
документы ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
музыка ('MP3', 'OGG', 'WAV', 'AMR');
архивы ('ZIP', 'GZ', 'TAR');
неизвестные расширения.
Список может быть дополнет разаботчиком

В результатах работы скрипс создает файл с:

Список файлов в каждой категории (музыка, видео, фото и пр.)
Перечень всех известных скрипту расширений, которые встречаются в целевой папке.
Перечень всех расширений, которые скрипту неизвестны.

за обработку каждого типа файлов отвечает отдельная функция.

Все файлы и папке переименовиваються. Для этого к именам файлов применяется функция normalize. Переименование файла не изменяет расширения файлов.

Функция normalize:

Проводит транслитерацию кириллического алфавита на латинский.
Заменяет все символы кроме латинских букв, цифр на '_'.

Функция normalize:
принимает на вход строку и возвращает строку;
проводит транслитерацию кириллических символов на латиницу;
заменяет все символы, кроме букв латинского алфавита и цифр, на символ '_';
транслитерация может не соответствовать стандарту, но читабельна;
большие буквы остаются большими, а меленькие — маленькими после транслитерации.

Описание работы скрипта:
изображения переносятся в папку images
документы переносятся в папку documents
аудио файлы переносятся в audio
видео файлы в video
архивы распаковываются и их содержимое переносится в папку archives

Критерии корректности работы скрипта:
все файлы и папки переименованы при помощи функции normalize.
расширения файлов не изменились после переименования.
пустые папки удалены
скрипт игнорирует папки archives, video, audio, documents, images;
распакованное содержимое архива переносится в папку archives в подпапку, названную точно так же, как и архив, но без расширения в конце;
файлы, расширения которых неизвестны, остаются без изменений.