# it-registry

Реестр аккредитованных IT орагнизаций по РФ на VueJS + Flask 

## Установка зависимостей (*NIX, Debian-based)
```sh
sudo apt update
sudo apt install build-essential checkinstall libssl-dev python-software-properties python3-venv g++ make
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt update
sudo apt install nodejs npm
```

## Клонирование и запуск development сервера
```sh
git clone https://github.com/tinytengu/it-registry.git
cd it-registry
npm install
npm run dev
```

## Cборка проекта во Flask приложение
### *NIX
```sh
# Cборка продакш версии проекта
npm run build

# Конвертация папки dist в папку во Flask проект
python3 vtf.py --output=../it-registry-flask

# Запуск проекта
cd ../it-registry-flask
source env/bin/activate
python main.py
```

### Windows
```sh
# Cборка продакш версии проекта
npm run build

# Конвертация папки dist в папку во Flask проект
vtf.py --output=..\it-registry-flask

# Запуск проекта
cd ..\it-registry-flask
env\Scripts\activate
python main.py
```