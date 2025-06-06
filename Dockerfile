FROM sagemath/sagemath:9.7

# Установка переменных окружения
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
ENV QT_X11_NO_MITSHM=1

# Запуск от root для установки пакетов
USER root

# Установка базовых пакетов и зависимостей GUI
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    libgl1-mesa-glx \
    libegl1 \
    libfontconfig1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-cursor0 \
    libxcb-util1 \
    libxcb-xkb1 \
    libxcb-xinput0 \
    libxcb-xfixes0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    xkb-data \
    libxcb-shape0 \
    libx11-xcb1 \
    libglib2.0-0 \
    libnss3 \
    locales \
    # Для запуска GUI приложений в headless режиме
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Настройка локали
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Установка PyQt6, numba и других зависимостей (с указанием совместимых версий)
RUN pip3 install PyQt6 "numpy<1.25.0" "numba<0.58.0" "scipy<1.11.0" 
RUN sage -pip install PyQt6 "numpy<1.25.0" "numba<0.58.0" "scipy<1.11.0" 

# Компиляция библиотеки stribog
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=sage:sage ./GOST/stribog.c /home/sage/app/GOST/
RUN mkdir -p /home/sage/app/GOST && \
    gcc -shared -o /home/sage/app/GOST/libstribog.so -fPIC /home/sage/app/GOST/stribog.c

# Создание рабочей директории
WORKDIR /home/sage/app

# Копирование проекта и установка прав доступа
COPY --chown=sage:sage . /home/sage/app/

# Переключение на пользователя sage
USER sage

# Запуск приложения
CMD ["sage", "main.py"]
