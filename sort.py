import pathlib
import sys
import re
import shutil


def images_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('images')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def video_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('video')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def documents_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('documents')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def audio_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('audio')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    # FileExistsError
    new_path = path.rename(folder.joinpath(new_name + path.suffix))
    add_log(path, new_path)


def archives_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('archives')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    shutil.unpack_archive(path, folder.joinpath(new_name))
    path.unlink()
    add_log(path, path)


def unknown_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('unknown')
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

            FILE_EXTENSIONS.get(extension, unknown_processing)(
                sub_path, position_of_processed_files)

    if not list(path.iterdir()):
        path.rmdir()


FILE_EXTENSIONS = {'BMP': images_processing, 'JPEG': images_processing, 'PNG': images_processing, 'JPG': images_processing, 'SVG': images_processing,
                   'AVI': video_processing, 'MP4': video_processing, 'MOV': video_processing, 'MKV': video_processing,
                   'DOC': documents_processing, 'DOCX': documents_processing, 'TXT': documents_processing, 'PDF': documents_processing, 'XLSX': documents_processing, 'PPTX': documents_processing,
                   'MP3': audio_processing, 'OGG': audio_processing, 'WAV': audio_processing, 'AMR': audio_processing,
                   'ZIP': archives_processing, 'GZ': archives_processing, 'TAR': archives_processing}
IGNORED_FOLDERS = ['images', 'documents', 'audio', 'video', 'archives']

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
