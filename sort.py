import pathlib
import sys


def images_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('images')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    path.rename(folder.joinpath(new_name + path.suffix))


def video_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('video')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    path.rename(folder.joinpath(new_name + path.suffix))


def documents_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('documents')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    path.rename(folder.joinpath(new_name + path.suffix))


def audio_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('audio')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    path.rename(folder.joinpath(new_name + path.suffix))


def archives_processing(path: pathlib.Path, position_of_processed_files: int):

    folder = path.parents[position_of_processed_files].joinpath('archives')
    if not folder.exists():
        folder.mkdir()
    new_name = normalize(path.stem)
    path.rename(folder.joinpath(new_name + path.suffix))


def unknown_processing(path: pathlib.Path, position_of_processed_files: int):
    folder = path.parents[position_of_processed_files].joinpath('unknown')
    if not folder.exists():
        folder.mkdir()
    path.rename(folder.joinpath(path.name))


def normalize(path_name: str) -> str:

    return path_name


def sort_dir(path: pathlib.Path, position_of_processed_files: int = 0):

    for sub_path in path.iterdir():

        if sub_path.is_dir():
            if sub_path.name not in settings['ignored_folders']:
                sort_dir(sub_path, position_of_processed_files + 1)
        else:
            extension = sub_path.suffix.lstrip('.').upper()
            processing_func = settings['file_extensions'].get(extension)
            if processing_func:
                processing_func(sub_path, position_of_processed_files)
            else:
                unknown_processing(sub_path, position_of_processed_files)
    if not list(path.iterdir()):
        path.rmdir()


settings = {'file_extensions': {'JPEG': images_processing, 'PNG': images_processing, 'JPG': images_processing, 'SVG': images_processing,
                                'AVI': video_processing, 'MP4': video_processing, 'MOV': video_processing, 'MKV': video_processing,
                                'DOC': documents_processing, 'DOCX': documents_processing, 'TXT': documents_processing, 'PDF': documents_processing, 'XLSX': documents_processing, 'PPTX': documents_processing,
                                'MP3': audio_processing, 'OGG': audio_processing, 'WAV': audio_processing, 'AMR': audio_processing,
                                'ZIP': archives_processing, 'GZ': archives_processing, 'TAR': archives_processing},
            'ignored_folders': ['images', 'documents', 'audio', 'video', 'archives']}


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
