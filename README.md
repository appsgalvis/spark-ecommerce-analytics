# Actividad Spark Streaming y Kafka

## Descripción
Este repositorio contiene la implementación de análisis de datos en tiempo real utilizando Apache Spark Streaming y Apache Kafka, desarrollado como parte del curso de Big Data de la Universidad Nacional Abierta y a Distancia.

## Autor
- **Nombre:** Cristian Johan
- **Email:** johancjgb@gmail.com
- **Curso:** Big Data (Código: 202016911)

## Tecnologías Utilizadas
- Apache Spark Streaming
- Apache Kafka
- Python
- Hadoop
- ZooKeeper

## Estructura del Proyecto
```
├── README.md
├── Anexo 3. Instructivo Spark Streaming y Kafka.txt
├── Guía de aprendizaje - Tarea 3 - Procesamiento de Datos con Apache Spark.txt
├── kafka_producer.py
├── spark_streaming_consumer.py
└── datos_sensores.json
```

## Instalación y Configuración

### Prerrequisitos
- Máquina virtual con Ubuntu 22.04.5 LTS
- Hadoop configurado
- Spark instalado
- Python 3.x

### Credenciales de Acceso
- **IP:** 192.168.0.4
- **Usuario:** vboxuser
- **Password:** bigdata

### Pasos de Instalación

1. **Instalar librería de Python Kafka:**
```bash
pip install kafka-python
```

2. **Descargar e instalar Apache Kafka:**
```bash
wget https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka
```

3. **Iniciar servicios:**
```bash
# Iniciar ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Iniciar Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

4. **Crear topic:**
```bash
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data
```

## Ejecución

1. **Ejecutar productor:**
```bash
python3 kafka_producer.py
```

2. **Ejecutar consumidor Spark Streaming:**
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py
```

## Monitoreo
- **Consola Web de Spark:** http://192.168.0.4:4040

## Funcionalidades
- Generación de datos simulados de sensores IoT
- Procesamiento en tiempo real con Spark Streaming
- Análisis de temperatura y humedad por ventanas de tiempo
- Almacenamiento de estadísticas agregadas

## Datos de Sensores
El sistema simula sensores que generan datos de:
- Temperatura (15-35°C)
- Humedad (20-80%)
- Presión atmosférica
- Timestamp
- Ubicación del sensor

## Contribuciones
Este proyecto es parte de una actividad académica y está sujeto a las políticas de la Universidad Nacional Abierta y a Distancia.

## Licencia
Uso académico - Universidad Nacional Abierta y a Distancia
