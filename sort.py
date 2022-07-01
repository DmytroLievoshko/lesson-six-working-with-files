import pathlib
import sys
import re
import shutil


def images_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def video_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def documents_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def audio_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def archives_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    shutil.unpack_archive(path, folder.joinpath(new_name))
    path.unlink()
    add_log(path, path)


def unknown_processing(path: pathlib.Path, position_of_processed_files: int, folder_name: str):

    folder = path.parents[position_of_processed_files].joinpath(folder_name)
    if not folder.exists():
        folder.mkdir()
    # FileExistsError
    new_path = path.rename(folder.joinpath(path.name))
    add_log(path, new_path)


def normalize(path_name: str) -> str:

    path_name = path_name.translate(TRANS)
    path_name = re.sub(r'\W', r'_', path_name)
    return path_name


def add_log(path: pathlib.Path, new_path: pathlib.Path):
    new_folder = new_path.parent

    log_file = pathlib.Path(new_folder.parent.joinpath('log.txt'))
    if not log_file.exists():
        with open(log_file, 'w') as fh:
            fh.writelines(['known file extensions: \n',
                          'unknown file extensions: \n'])

    with open(log_file, 'r') as fh:

        lines = fh.readlines()
        new_lines = []
        search_string_category = new_folder.name + ':'
        if new_folder.name == 'unknown':
            search_string_extensions = "unknown file extensions:"
        else:
            search_string_extensions = "known file extensions:"
        is_line_category = False
        for line in lines:

            if line.startswith(search_string_extensions):
                line = line.replace(
                    ' \n', '|  ' + path.suffix.lstrip('.').upper() + ' \n')
            elif line.startswith(search_string_category):
                is_line_category = True
                line = line.replace(
                    ' \n', '|  ' + new_path.name + ' \n')
            new_lines.append(line)
        if not is_line_category:
            new_lines.append(search_string_category +
                             '|  ' + new_path.name + ' \n')

    with open(log_file, 'w') as fh:
        fh.writelines(new_lines)


def sort_dir(path: pathlib.Path, position_of_processed_files: int = 0):

    for sub_path in path.iterdir():

        if sub_path.name in IGNORED_FOLDERS:
            continue

        if sub_path.is_dir():
            sort_dir(sub_path, position_of_processed_files + 1)
        else:
            extension = sub_path.suffix.lstrip('.').upper()

            tuple_setting = SETTINGS.get(
                extension, (unknown_processing, 'unknown'))

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


def main():

    if len(sys.argv)-1 < 1:
        print(f'The script must take 1 argumet!')
        return

    user_path = pathlib.Path(" ".join(sys.argv[1:]))

    if user_path.exists():

        if user_path.is_dir():
            sort_dir(user_path)
        else:
            print(f'{str(user_path.absolute())} is no directory')

    else:
        print(f'{str(user_path.absolute())} does not exist')


if __name__ == '__main__':
    main()
