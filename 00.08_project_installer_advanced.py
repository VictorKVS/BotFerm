# Путь для размещения файла:
# —> 00_installer/04.01_evi/project_installer_advanced.py

import os
import sys
import yaml
import logging

# Настройка логов
logging.basicConfig(
    filename='installer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def load_structure(file_path):
    if not os.path.exists(file_path):
        logging.error(f"Файл структуры {file_path} не найден.")
        print(f"❗ Ошибка: Файл {file_path} не найден.")
        sys.exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Ошибка чтения YAML: {str(e)}")
        print(f"❗ Ошибка чтения YAML: {str(e)}")
        sys.exit(1)

def create_structure(structure, base_path):
    if not structure:
        logging.warning("Структура проекта пуста.")
        print("⚠️ Внимание: Структура проекта пуста.")
        sys.exit(1)

    for item in structure:
        path = os.path.join(base_path, item.get("path"))
        item_type = item.get("type")

        if not path or not item_type:
            logging.warning(f"Пропущен элемент без пути или типа: {item}")
            continue

        try:
            if item_type == "directory":
                os.makedirs(path, exist_ok=True)
                gitkeep_path = os.path.join(path, ".gitkeep")
                open(gitkeep_path, 'a').close()
                logging.info(f"Создана папка: {path}")
                print(f"📂 Папка создана: {path}")
            elif item_type == "file":
                dir_name = os.path.dirname(path)
                if dir_name and not os.path.exists(dir_name):
                    os.makedirs(dir_name, exist_ok=True)
                if not os.path.exists(path):
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(f"# {item.get('description', 'Файл проекта')}\n")
                    logging.info(f"Создан файл: {path}")
                    print(f"📄 Файл создан: {path}")
            else:
                logging.warning(f"Неизвестный тип элемента: {item_type}")
                print(f"⚠️ Неизвестный тип: {item_type} для {path}")
        except Exception as e:
            logging.error(f"Ошибка создания {path}: {str(e)}")
            print(f"❗ Ошибка создания {path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❗ Использование: python project_installer_advanced.py путь_к_yaml путь_куда_развернуть")
        sys.exit(1)

    yaml_path = sys.argv[1]
    base_path = sys.argv[2]

    structure_data = load_structure(yaml_path)
    project_structure = structure_data.get("project_structure") if isinstance(structure_data, dict) else structure_data
    create_structure(project_structure, base_path)

    print("\n✅ Установка структуры проекта завершена успешно!")
    logging.info("Структура проекта успешно установлена.")
