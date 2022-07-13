#Напишите программу обработки папки "Хлам", которая сортирует файлы в указанной папке по расширениям с использованием asyncio.
#Чтобы перемещать и переименовывать файлы, воспользуйтесь асинхронной версией pathlib: aiopath.

import os
import re
import asyncio
from time import time
from aiopath import AsyncPath

sort_folder = (input (f"Enter a path: "))

files = {"audio": [".mp3", ".ogg", ".wav", ".amr"],
         "video": [".mp4", ".avi", ".mov", ".mkv", ".MOV"],
         "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx", ".rtf", ".PDF", ".xls"],
         "images": [".jpeg", ".png", ".jpg", ".svg", ".bmp", ".BMP"],
         "archives": [".zip", ".gz", ".tar", ".tgz", ".rar"],
         "other": []}


def normalize(name):   # transliteration
    dictionary = {ord("А"): "A", ord("Б"): "B", ord("В"): "V", ord("Г"): "G", ord("Д"): "D", ord("Е"): "E", ord("Ж"): "ZH", ord("З"): "Z",
                  ord("И"): "I", ord("Й"): "J", ord("К"): "K", ord("Л"): "L", ord("М"): "M", ord("Н"): "N", ord("О"): "O", ord("П"): "P",
                  ord("Р"): "R", ord("С"): "S", ord("Т"): "T", ord("У"): "U", ord("Ф"): "F", ord("Х"): "H", ord("Ц"): "TS", ord("Ч"): "CH",
                  ord("Ш"): "SH", ord("Щ"): "SHCH", ord("Ь"): "", ord("Э"): "E", ord("Ю"): "YU", ord("Я"): "YA", ord("Ъ"): "", ord("Ы"): "Y",
                  ord("Ё"): "E", ord("Є"): "E", ord("І"): "Y", ord("Ї"): "YI", ord("Ґ"): "G",
                  ord("а"): "a", ord("б"): "b", ord("в"): "v", ord("г"): "g", ord("д"): "d", ord("е"): "e", ord("ж"): "zh", ord("з"): "z",
                  ord("и"): "y", ord("й"): "j", ord("к"): "k", ord("л"): "l", ord("м"): "m", ord("н"): "n", ord("о"): "o", ord("п"): "p",
                  ord("р"): "r", ord("с"): "s", ord("т"): "t", ord("у"): "y", ord("ф"): "f", ord("х"): "h", ord("ц"): "c", ord("ч"): "ch",
                  ord("ш"): "sh", ord("щ"): "shsc", ord("ь"): "", ord("э"): "e", ord("ю"): "yu", ord("я"): "ya", ord("ъ"): "", ord("ы"): "y",
                  ord("ё"): "e", ord("є"): "e", ord("і"): "y", ord("ї"): "yi", ord("ґ"): "g",
                  ord("1"): "1", ord("2"): "2", ord("3"): "3", ord("4"): "4", ord("5"): "5", ord("6"): "6", ord("7"): "7", ord("8"): "8", ord("9"): "9", ord("0"): "0"}
    en_name = name.translate(dictionary)
    fin_name = re.sub(r"(\W)", '_', en_name)
    return fin_name


dict_keys = list(dict.keys(files)) # Folder creates
for folder in dict_keys:
    os.chdir(sort_folder)
    folder = str(folder)
    if not os.path.isdir(folder):
        os.makedirs(folder)


async def move(path):      # Move files in folders to destination
    file = normalize("".join((path.name).split(".")[0:-1]))+path.suffix
    sort_file = list(files.items())
    if path.suffix:
        el_moved = False
        for value in range(len(sort_file)):
            if path.suffix in sort_file[value][1]:
                os.rename(path, f'{sort_folder}\\other\\{file}')
                #path.replace(f'{sort_folder}\\{sort_file[value][0]}\\{file}')
                print(f'Moving {file} in {sort_file[value][0]} folder\n')
                el_moved = True
        if not el_moved:
            os.rename(path, f'{sort_folder}\\other\\{file}')
            print(f'Moving {file} in other folder\n')


async def folder_sort(path):  # Recursion through folders
    p = AsyncPath(path)
    path = (p.glob('**/*'))
    files_list = []
    async for el in path:
        if el.suffix:
            files_list.append(el) 
    for el in files_list:
        await move(el)

if __name__ == "__main__":
    start = time()
    asyncio.run(folder_sort(sort_folder))
    fin = time() - start 
    print(fin)

#C:\Users\assa\Desktop\test1
#2.877342939376831 sec - result whithout async
#1.4578866958618164 sec - result now