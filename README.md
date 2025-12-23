@'# 🏊‍♂️ Кубок ВС РФ по плаванию

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**Профессиональное приложение для подсчета командных результатов соревнований по плаванию**

</div>

## 📋 Описание
Приложение для автоматизации расчета командных результатов Кубка ВС РФ по плаванию среди мужчин. Программа позволяет вводить результаты команд, автоматически рассчитывать сумму 15 лучших результатов из 20 и генерировать итоговые отчеты в формате PDF.

## ✨ Возможности
- Ввод информации о соревнованиях (место, сроки, объект)
- Поддержка до 100 команд
- Автоматический расчет 15 лучших результатов из 20
- Просмотр промежуточных результатов
- Генерация PDF отчетов
- Интуитивный графический интерфейс

## 🚀 Быстрый старт
### Запуск готового приложения:
1. Скачайте `SwimmingCupApp.exe` из [Releases](https://github.com/NoHead73/SwimmingCup/releases)
2. Запустите файл
3. Следуйте инструкциям в приложении

### Запуск из исходного кода:
```bash
git clone https://github.com/NoHead73/SwimmingCup.git
cd SwimmingCup
python swimming_cup_app.py
📁 Структура проекта
text
SwimmingCup/
├── swimming_cup_app.py          # Основной код приложения
├── build_exe.py                 # Скрипт сборки
├── icon.ico                     # Иконка приложения
├── requirements.txt             # Зависимости
├── LICENSE                      # Лицензия MIT
├── build/                       # Временные файлы сборки
└── dist/                        # Готовый исполняемый файл
🔧 Сборка
bash
# Установка зависимостей
pip install -r requirements.txt

# Сборка исполняемого файла
python build_exe.py
📄 Лицензия
MIT License. Подробнее в файле LICENSE.

👨‍💻 Автор
NoHead73
'@ | Out-File -FilePath $readmePath -Encoding UTF8 -Force