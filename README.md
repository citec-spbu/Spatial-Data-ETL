# Spatial-Data-ETL
## Автоматизация сбора и обработки пространственных данных   
### !Requirements: sudo, ОС на базе Debian   
### Установка:   
``` 
git clone https://github.com/citec-spbu/Spatial-Data-ETL.git  
cd Spatial-Data-ETL  
sudo +x setup.sh  
./setup.sh
```  
##### Запуск airflow:  
`airflow standalone`  
##### Добавление нового файла: в src  
`./newFile (cсылка на pbf)`  
##### Запуск дельт в ручном режиме: в src  
`./delt.sh`
### Использование конфиг файлов
- В spatial.config хранятся настройки БД, которая будет создаваться
- В links.config хранятся ссылки на pbf файлы c [geofabrik](https://download.geofabrik.de/), на города/регионы/страны которые вы хотите загрузить. Перед установкой нужно отредактировать список.
### Структура данных
После установки будет создана БД PSQL со структурой  
Таблицы(для каждого файла):  
вашРегион_point  
вашРегион_line  
вашРегион_polygon  
вашРегион_roads  

Таблица(для всех):  
spatial_sys_ref  

View(для всех):  
geography_columns  
geometry_columns