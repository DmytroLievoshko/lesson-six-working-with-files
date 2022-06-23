import pathlib
import sys


def main():

    quantity_args = len(sys.argv)-1
    if quantity_args < 1 or quantity_args > 1:
        print(f'The script must take 1 arg! There are {quantity_args} args.')
        return

    user_path = pathlib.Path(sys.argv[1])
    if user_path.exists():

        if user_path.is_dir():
            print(str(user_path.absolute()))
        else:
            print(f'{str(user_path.absolute())} is no directory')

    else:
        print(f'{str(user_path.absolute())} does not exist')


if __name__ == '__main__':
    main()
