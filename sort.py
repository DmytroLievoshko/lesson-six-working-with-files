from os import remove
import pathlib
import sys
import re
import shutil


def make_new_path(path: pathlib.Path, position_of_processed_files: int, folder_name: str, unknown=False, archive=False):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()

    parents_folder = path.parents[:position_of_processed_files]

    new_path = folder
    for paren in parents_folder[::-1]:
        if paren == folder:
            continue
        new_path = new_path.joinpath(normalize(paren.stem))
        if not new_path.exists():
            new_path.mkdir()

    if not unknown:
        if archive:
            new_path = new_path.joinpath(normalize(path.stem))
        else:
            new_path = new_path.joinpath(normalize(path.stem) + path.suffix)
    else:
        new_path = new_path.joinpath(path.name)

    return new_path


def mova_file(path: pathlib.Path, new_path: pathlib.Path, folder_name: str, unknown=False, archive=False):

    if archive:
        try:
            shutil.unpack_archive(path, new_path)
        except FileExistsError:
            print(f'failed to extract archive {path.name}')
        else:
            add_to_log(path.suffix, path.name, folder_name)
            try:
                path.unlink()
            except FileExistsError:
                print(f'failed to delete file {path.name}')
    else:
        try:
            new_path = shutil.move(path, new_path)
        except FileExistsError:
            print(f'failed to write file {path.name}')
        else:
            add_to_log(path.suffix, path.name, folder_name, unknown)


def images_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name)
    mova_file(path, new_path, folder_name)


def video_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name)
    mova_file(path, new_path, folder_name)


def documents_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name)
    mova_file(path, new_path, folder_name)


def audio_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name)
    mova_file(path, new_path, folder_name)


def archives_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name,
                             archive=True)
    mova_file(path, new_path, folder_name,
              archive=True)


def unknown_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    new_path = make_new_path(path, position_of_processed_files, folder_name,
                             unknown=True)
    mova_file(path, new_path, folder_name,
              unknown=True)


def normalize(path_name: str) -> str:

    path_name = path_name.translate(TRANS)
    path_name = re.sub(r'\W', r'_', path_name)
    return path_name


def add_to_log(extension: str, file_name: str, categorie: str, unknown: bool = False):

    global DICT_FILES_BY_CATEGORIES, SET_KNOWN_FILE_EXTENSIONS

    if unknown:
        SET_UNKNOWN_FILE_EXTENSIONS.add(extension.lstrip('.').upper())
    else:
        SET_KNOWN_FILE_EXTENSIONS.add(extension.lstrip('.').upper())

    DICT_FILES_BY_CATEGORIES.setdefault(categorie, []).append(file_name)


def log_print():

    str_known = f"Known file extension: {', '.join(SET_KNOWN_FILE_EXTENSIONS)}"
    str_unknown = f"Unknown file extension: {', '.join(SET_UNKNOWN_FILE_EXTENSIONS)}"
    separator_length = min(80, max(len(str_known), len(str_unknown)))
    print("="*separator_length)
    print(str_known)
    print("="*separator_length)
    print(str_unknown)
    print("="*separator_length)

    print("-"*80)
    for key, value in DICT_FILES_BY_CATEGORIES.items():

        print_str = "{:<15}| ".format(key)
        print_str += f"\n{' '*15}| ".join(value)
        print(print_str)
        print("-"*80)


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
            log_print()
        else:
            print(f'{str(user_path.absolute())} is no directory')

    else:
        print(f'{str(user_path.absolute())} does not exist')


if __name__ == '__main__':
    main()
