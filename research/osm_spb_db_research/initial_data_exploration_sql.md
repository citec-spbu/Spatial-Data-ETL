Исследование данных из OSM с использованием PostgreSQL, PostGis, QGis.

Данные были взяты по ссылке: https://download.geofabrik.de/russia/northwestern-fed-district-latest.osm.pbf

Исследование полезных полей:

![Снимок экрана 2024-03-30 222133](https://github.com/citec-spbu/Spatial-Data-ETL/assets/57402279/bf4dcc8f-3e67-42a7-898b-bc712cb27970)

Пример отображения данных в QGis. Выбираем геометрическую примитиву point, где amenity = restaurant:

![image](https://github.com/citec-spbu/Spatial-Data-ETL/assets/57402279/6a5dc944-30cb-4f3a-82fd-6a52204f5e85)

Также видно, что некоторые рестораны имеют тип не point, а polygon:

![image](https://github.com/citec-spbu/Spatial-Data-ETL/assets/57402279/5e75a827-8c26-4480-bad5-7e8cffe2769d)

