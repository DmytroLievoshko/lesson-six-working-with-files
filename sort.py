from os import remove
import pathlib
import sys
import re
import shutil


def images_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS
    SET_KNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))


def video_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS
    SET_KNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))


def documents_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS
    SET_KNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))


def audio_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS
    SET_KNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))


def archives_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS
    SET_KNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    shutil.unpack_archive(path, folder.joinpath(new_name))
    path.unlink()


def unknown_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    global DICT_FILES_BY_CATEGORIES, SET_UNKNOWN_FILE_EXTENSIONS
    SET_UNKNOWN_FILE_EXTENSIONS.add(path.suffix.lstrip('.').upper())
    DICT_FILES_BY_CATEGORIES.setdefault(folder_name, []).append(path.name)

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    # FileExistsError
    new_path = path.rename(folder.joinpath(path.name))


def normalize(path_name: str) -> str:

    path_name = path_name.translate(TRANS)
    path_name = re.sub(r'\W', r'_', path_name)
    return path_name


def sort_dir(path: pathlib.Path, position_of_processed_files: int = 0):

    for sub_path in path.iterdir():

        if sub_path.name in IGNORED_FOLDERS:
            continue

        if sub_path.is_dir():
            sort_dir(sub_path, position_of_processed_files + 1)
        else:
            extension = sub_path.suffix.lstrip('.').upper()

            tuple_setting = SETTINGS.get(
                extension, (unknown_processing, 'unknowns'))

            tuple_setting[0](
                sub_path, position_of_processed_files, tuple_setting[1])

    if not list(path.iterdir()):
        path.rmdir()


SETTINGS = {'BMP': (images_processing, 'images'), 'JPEG': (images_processing, 'images'), 'PNG': (images_processing, 'images'), 'JPG': (images_processing, 'images'), 'SVG': (images_processing, 'images'),
            'AVI': (video_processing, 'video'), 'MP4': (video_processing, 'video'), 'MOV': (video_processing, 'video'), 'MKV': (video_processing, 'video'),
            'DOC': (documents_processing, 'documents'), 'DOCX': (documents_processing, 'documents'), 'TXT': (documents_processing, 'documents'), 'PDF': (documents_processing, 'documents'), 'XLSX': (documents_processing, 'documents'), 'PPTX': (documents_processing, 'documents'),
            'MP3': (audio_processing, 'audio'), 'OGG': (audio_processing, 'audio'), 'WAV': (audio_processing, 'audio'), 'AMR': (audio_processing, 'audio'),
            'ZIP': (archives_processing, 'archives'), 'GZ': (archives_processing, 'archives'), 'TAR': (archives_processing, 'archives')}

IGNORED_FOLDERS = {tuple_setting[1] for tuple_setting in SETTINGS.values()}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.title()

DICT_FILES_BY_CATEGORIES = dict()
SET_UNKNOWN_FILE_EXTENSIONS = set()
SET_KNOWN_FILE_EXTENSIONS = set()


def main():

    if len(sys.argv)-1 < 1:
        print(f'The script must take 1 argumet!')
        return

    user_path = pathlib.Path(" ".join(sys.argv[1:]))

    if user_path.exists():

        if user_path.is_dir():
            sort_dir(user_path)
            print(SET_KNOWN_FILE_EXTENSIONS)
            print(SET_UNKNOWN_FILE_EXTENSIONS)
            print(DICT_FILES_BY_CATEGORIES)
        else:
            print(f'{str(user_path.absolute())} is no directory')

    else:
        print(f'{str(user_path.absolute())} does not exist')


if __name__ == '__main__':
    main()
