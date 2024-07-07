import os

# Путь к папке img
img_folder = 'img'

# Проверка содержимого папки
if not os.path.exists(img_folder):
    print(f"Папка {img_folder} не существует.")
else:
    files = os.listdir(img_folder)
    if not files:
        print(f"Папка {img_folder} пуста.")
    else:
        print(f"Содержимое папки {img_folder}:")
        for file in files:
            print(file)
