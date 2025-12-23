import PyInstaller.__main__
import os
import sys

# Определение пути к текущей папке
current_dir = os.path.dirname(os.path.abspath(__file__))

# Параметры для PyInstaller
args = [
    'swimming_cup_app.py',
    '--name=SwimmingCupApp',
    '--onefile',
    '--windowed',
    '--clean',
    '--noconsole',
]

print("Начало сборки EXE файла...")
PyInstaller.__main__.run(args)
print("Сборка завершена!")
