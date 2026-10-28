# Real vs Fake Face Detector

Веб-приложение на базе глубокого обучения (**MobileNetV2**) для распознавания настоящих фотографий лиц (`Real`) и изображений, сгенерированных искусственным интеллектом (`Fake`).

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?logo=tensorflow&logoColor=white)

---

## Возможности

- **Загрузка изображений** — поддержка Drag & Drop и выбора файлов (`PNG`, `JPG`, `JPEG` до 16 МБ).
- **Быстрая классификация** — предобученная свёрточная нейросеть `MobileNetV2` анализирует изображение размером `128×128` пикселей.
- **Наглядная визуализация** — отображение итогового вердикта (`REAL` / `FAKE`), уверенности модели и шкалы вероятностей для обоих классов.
- **Тестовый набор данных** — в папке `test_pictures/` уже подготовлены примеры настоящих (`real/`) и сгенерированных (`fake/`) лиц для быстрой проверки.

---

## Быстрый старт

### Требования
- **Python 3.11** (рекомендуется для совместимости с `TensorFlow 2.15`)

### 1. Клонирование репозитория
```bash
git clone https://github.com/MLA-Yersultan-Kuanysh-Rasul/face_classification.git
cd face_classification
```

### 2. Установка и запуск

#### Windows
Используйте готовые скрипты для автоматической настройки виртуального окружения и запуска:
```cmd
setup.bat
run.bat
```

#### Linux / macOS
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

#### Ручной запуск
```bash
python -m venv venv
# Активация на Windows:
venv\Scripts\activate
# Активация на Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

После запуска откройте в браузере: **[http://localhost:5000](http://localhost:5000)**

---

## О модели

- **Архитектура:** `MobileNetV2` (Transfer Learning) + `GlobalAveragePooling2D` + полносвязный слой с `Dropout` и `Sigmoid`-выходом.
- **Входное разрешение:** `128 × 128` (RGB).
- **Порог классификации:** `0.42` (при вероятности класса `Real` $\ge 42\%$ изображение классифицируется как настоящее, иначе — как сгенерированное ИИ).

---

## Структура проекта

```text
face_classification/
├── app.py               # Flask-сервер и логика инференса модели
├── model/
│   └── best_model.h5    # Обученные веса модели MobileNetV2
├── static/
│   ├── css/style.css    # Стили интерфейса
│   └── js/script.js     # Клиентская логика загрузки и отображения результатов
├── templates/
│   └── index.html       # Главная страница приложения
├── test_pictures/       # Примеры изображений для тестирования (real / fake)
├── requirements.txt     # Зависимости Python
├── render.yaml          # Конфигурация для деплоя на Render
├── setup.bat / setup.sh # Скрипты установки окружения
└── run.bat / run.sh     # Скрипты запуска сервера
```
