# Імпорт потрібних бібліотек
import re
import sys
import shutil
from pathlib import Path, PurePath
from transliterate import translit


# Визначення категорій та розширень
categories_suffixes = {
    'images': ['.jpeg', '.png', '.jpg', '.svg'],
    'documents': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'video': ['.avi', '.mp4', '.mov', '.mkv'],
    'archives': ['.zip', '.gz', '.tar']
}


# Функція для визначення списку категорій
def get_category_list():
    categories = list(categories_suffixes.keys())
    categories.append('others')
    return categories


# Функція для створення папок відповідних категорій
def mkdir_category_dirs(main_path):
    for item in get_category_list():
        category_dir_path = PurePath(main_path).joinpath(item)
        try:
            Path(category_dir_path).mkdir()
        except FileExistsError:
            continue


# Перевірка, чи є файли у папці
def is_items_in_dir(dir_name):
    if dir_name.is_dir():
        files = list(dir_name.glob('*'))
        if len(files) > 0:
            return True
        else:
            return False


# Функція для відвідування всіх папок у вказаній папці
def check_all_dirs(each_dir_path, main_path):
    category_list = get_category_list()
    for file_name in each_dir_path.iterdir():
        if file_name.is_dir():
            if file_name.name in category_list:
                continue
            else:
                if is_items_in_dir(file_name):
                    check_all_dirs(file_name, main_path)
                elif not is_items_in_dir(file_name):
                    file_name.rmdir()
                    continue
        elif file_name.is_file():
            sort_files_func(normalize(file_name), main_path)
    remove_empty_dirs(main_path)
    return 0


# Додаткове видалення порожніх папок
def remove_empty_dirs(main_path):
    category_list = get_category_list()
    for item in main_path.iterdir():
        if item.is_dir():
            if item.name not in category_list and not is_items_in_dir(item):
                item.rmdir()
            elif is_items_in_dir(item):
                remove_empty_dirs(item)
                try:
                    item.rmdir()
                except OSError:
                    continue


# Функція для нормалізації назв папок та файлів
def normalize(file_path):
    norm_file_name = translit(file_path.stem, 'uk', reversed=True)
    norm_file_name = re.sub(r'\W', '_', norm_file_name)
    full_file_name = file_path.with_name(norm_file_name + file_path.suffix)
    try:
        return file_path.rename(Path(full_file_name))
    except FileExistsError:
        norm_file_name = norm_file_name + '_to_check' + file_path.suffix
        full_file_name = file_path.with_name(norm_file_name)
        return file_path.rename(Path(full_file_name))


# Функція для перенесення файлу у іншу папку
def file_moving_func(file, category_dir):
    new_file_path = PurePath(category_dir).joinpath(file.name)
    file_name = file.stem
    while True:
        try:
            file.rename(Path(new_file_path))
            break
        except FileExistsError:
            file_name += '_to_check'
            new_file_path = PurePath(category_dir).joinpath(file_name + file.suffix)
            continue
        except FileNotFoundError:
            print('Файл у вказаній папці не знайдено.')
    return new_file_path


# Функція для перекидання файлу у відповідну папку
def sort_files_func(file_path, main_path):
    file_suffix = file_path.suffix.lower()
    is_moved = False
    for each_category, category_suffixes in categories_suffixes.items():
        if file_suffix in category_suffixes:
            dir_path = PurePath(main_path).joinpath(each_category)
            new_file_path = file_moving_func(file_path, dir_path)
            if each_category == 'archives':
                unpack_archive_func(new_file_path, dir_path)
            is_moved = True
            break
    if not is_moved:
        dir_path = PurePath(main_path).joinpath('others')
        file_moving_func(file_path, dir_path)


# Функція, яка розпаковує архів у відповідну папку та видаляє початковий архів
def unpack_archive_func(archive_file, archive_path):
    shutil.unpack_archive(archive_file, archive_path)
    Path(archive_file).unlink()

# Головна функція
def sort_files_in_folder(main_path):
    mkdir_category_dirs(main_path)
    check_all_dirs(main_path, main_path)
