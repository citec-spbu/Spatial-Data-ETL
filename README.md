# Spatial-Data-ETL
## Автоматизация сбора и обработки пространственных данных   
##### !Requirements: sudo, ОС на базе Debian   
##### Установка:   
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