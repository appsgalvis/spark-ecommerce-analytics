# Spark E-commerce Analytics

## Descripción del Proyecto

Este proyecto implementa una solución completa de análisis de datos de transacciones de e-commerce utilizando Apache Spark para procesamiento batch y streaming en tiempo real con Apache Kafka.

### Características Principales

- **Procesamiento Batch**: Análisis exploratorio de datos (EDA) de 100,000 transacciones de ventas
- **Procesamiento en Tiempo Real**: Streaming de transacciones simuladas usando Kafka y Spark Streaming
- **Análisis Completo**: Estadísticas por categoría, método de pago, productos más vendidos, análisis temporal
- **Visualización**: Resultados en consola y archivos Parquet para análisis posterior

## Dataset Utilizado

El proyecto utiliza un dataset sintético de transacciones de e-commerce que incluye:

- **100,000 transacciones** generadas aleatoriamente
- **5 categorías**: Electrónica, Ropa, Hogar, Deportes, Libros
- **3 métodos de pago**: Tarjeta, PayPal, Transferencia
- **3 estados**: Completada, Pendiente, Cancelada
- **Período**: Últimos 30 días con timestamps realistas

### Campos del Dataset

| Campo | Tipo | Descripción |
|-------|------|-------------|
| transaction_id | Integer | ID único de la transacción |
| timestamp | String | Fecha y hora de la transacción |
| customer_id | Integer | ID del cliente |
| product_id | Integer | ID del producto |
| category | String | Categoría del producto |
| quantity | Integer | Cantidad vendida |
| unit_price | Double | Precio unitario |
| total | Double | Total de la transacción |
| payment_method | String | Método de pago utilizado |
| status | String | Estado de la transacción |

## Requisitos Previos

### En la Máquina Virtual (Ubuntu con Hadoop/Spark)

**Nota Importante**: Este proyecto asume que ya tienes un servidor Hadoop preconfigurado y funcionando en la máquina virtual con los siguientes componentes instalados:

- Apache Spark 3.5.3 (preinstalado y configurado)
- Python 3.x (preinstalado)
- Java 8 o superior (preinstalado)
- Apache Kafka 3.6.2 (se instalará durante el proceso)

### Dependencias Python

```bash
pip install -r requirements.txt
```

## Instrucciones de Instalación

**Nota**: El servidor Hadoop y Spark ya deben estar preconfigurados y funcionando correctamente. Estas instrucciones cubren la configuración de Kafka y la ejecución de la aplicación.

### 1. Configuración de Kafka (en la VM)

```bash
# Instalar kafka-python
pip install kafka-python

# Descargar y configurar Kafka
wget https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka

# Iniciar ZooKeeper
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Iniciar Kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

# Crear topic para transacciones
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transacciones_ventas
```

## Comandos de Ejecución

### 1. Generar Dataset (Ejecutar localmente)

```bash
python3 generar_dataset_ventas.py
```

### 2. Procesamiento Batch (En la VM)

```bash
spark-submit procesamiento_batch.py
```

### 3. Streaming en Tiempo Real (En la VM)

#### Terminal 1 - Productor Kafka:
```bash
python3 kafka_productor_ventas.py
```

#### Terminal 2 - Consumidor Spark Streaming:
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumidor.py
```

## Estructura del Proyecto

```
spark-ecommerce-analytics/
├── datos/
│   └── transacciones_ventas.csv          # Dataset generado
├── batch/
│   └── procesamiento_batch.py            # Script de procesamiento batch
├── streaming/
│   ├── kafka_productor_ventas.py         # Productor de Kafka
│   └── spark_streaming_consumidor.py    # Consumidor Spark Streaming
├── resultados/                            # Resultados del procesamiento batch
│   ├── transacciones_limpias.parquet
│   ├── transacciones_con_fecha.parquet
│   └── ventas_por_categoria.parquet
├── README.md                             # Este archivo
├── requirements.txt                       # Dependencias Python
└── INSTRUCCIONES_EJECUCION.md           # Guía detallada de ejecución
```

## Análisis Realizados

### Procesamiento Batch

1. **Limpieza de Datos**
   - Eliminación de valores nulos
   - Eliminación de duplicados
   - Validación de datos

2. **Análisis Exploratorio**
   - Estadísticas descriptivas
   - Ventas por categoría
   - Ventas por método de pago
   - Top 10 productos más vendidos
   - Análisis temporal (ventas por día/hora)
   - Distribución de estados de transacción

### Procesamiento en Tiempo Real

1. **Métricas por Ventana de Tiempo (1 minuto)**
   - Total de ventas
   - Número de transacciones
   - Promedio de venta

2. **Análisis por Categoría**
   - Ventas por categoría en tiempo real
   - Ranking de categorías más vendidas

3. **Análisis de Métodos de Pago**
   - Métodos más utilizados
   - Volumen de transacciones por método

4. **Estados de Transacción**
   - Distribución de estados en tiempo real
   - Monitoreo de transacciones completadas vs pendientes

## Capturas de Pantalla del Proceso

**Nota**: Las capturas de pantalla están organizadas por carpeta `imagenes/` e integradas en las secciones de instalación y ejecución arriba.

#### Actualización del Sistema
![Actualización del Sistema](imagenes/Toma%20captura%20de%20la%20actualizaci%C3%B3n%20del%20sistema.png)

#### Versiones de Python y pip
![Versiones de Python y pip](imagenes/Captura%20las%20versiones%20de%20Python%20y%20pip.png)

#### Clonación del Repositorio
![Clonación del Repositorio](imagenes/Toma%20captura%20de%20la%20clonaci%C3%B3n%20exitosa%20del%20repositorio.png)

### 2. Instalación de Dependencias

#### Instalación de Dependencias Python
![Instalación de Dependencias](imagenes/Captura%20la%20instalaci%C3%B3n%20exitosa%20de%20las%20dependencias%20Python.png)

#### Verificación de Librerías
![Verificación de Librerías](imagenes/Captura%20la%20verificaci%C3%B3n%20de%20las%20librer%C3%ADas%20instaladas.png)

### 3. Configuración de Servicios

#### Servicios Hadoop (jps)
![Servicios Hadoop](imagenes/Captura%20la%20salida%20de%20jps%20mostrando%20los%20servicios%20de%20Hadoop.png)

#### Versión de Spark
![Versión de Spark](imagenes/Captura%20la%20versi%C3%B3n%20de%20Spark%20instalada.png)

#### Dataset CSV Verificado
![Dataset CSV](imagenes/Captura%20la%20verificaci%C3%B3n%20del%20dataset%20CSV.png)

### 4. Configuración de Kafka

#### Descarga y Configuración de Kafka
![Descarga de Kafka](imagenes/Captura%20la%20descarga%20%2C%20descompresi%C3%B3n%20y%20configuraci%C3%B3n%20de%20Kafka..png)

#### Inicio de Kafka
![Inicio de Kafka](imagenes/Captura%20el%20inicio%20de%20Kafka.png)

#### Creación del Topic
![Creación del Topic](imagenes/Captura%20la%20creaci%C3%B3n%20exitosa%20del%20topic.png)

### 5. Procesamiento Batch

#### Ejecución del Procesamiento Batch
![Ejecución Batch a](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20a.png)

![Ejecución Batch b](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20b.png)

![Ejecución Batch c](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20c.png)

![Ejecución Batch d](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20d.png)

#### Archivos Parquet Generados
![Archivos Parquet](imagenes/Captura%20los%20archivos%20Parquet%20generado.png)

### 6. Spark Streaming en Tiempo Real

#### Productor Kafka
![Productor Kafka](imagenes/Captura%20el%20productor%20enviando%20transacciones.png)

#### Consumidor Spark Streaming
![Consumidor Streaming](imagenes/Captura%20el%20consumidor%20procesando%20datos%20en%20tiempo%20real.png)

#### Interfaz Web de Spark
![Spark UI Jobs](imagenes/Captura%20la%20interfaz%20web%20de%20Spark%20mostrando%20jobs..png)

![Spark UI Streaming](imagenes/Captura%20la%20interfaz%20web%20de%20Spark%20mostrando%20StreamingQuery.png)

### 7. Estructura del Proyecto

#### Estructura de Directorios
![Estructura de Directorios](imagenes/Captura%20la%20estructura%20de%20directorios%20creada.png)

## Monitoreo y Visualización

### Interfaz Web de Spark
Acceder a: `http://192.168.0.x:4040` para ver:
- Jobs ejecutándose
- Stages del procesamiento
- Métricas de rendimiento
- Historial de aplicaciones

### Salida en Consola
Los resultados se muestran en tiempo real en la consola con:
- Ventanas de tiempo con métricas agregadas
- Rankings de categorías y productos
- Estadísticas de métodos de pago

## Resultados Esperados

### Procesamiento Batch
- Dataset limpio de ~100,000 transacciones
- Estadísticas por categoría (Electrónica lidera en ventas)
- Distribución temporal de ventas
- Top productos más vendidos

### Streaming en Tiempo Real
- Procesamiento continuo de transacciones
- Actualización de métricas cada minuto
- Monitoreo de patrones de venta en tiempo real
- Detección de tendencias por categoría

## Solución de Problemas

### Error de Conexión a Kafka
```bash
# Verificar que Kafka esté ejecutándose
sudo /opt/Kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Error de Memoria en Spark
```bash
# Ajustar memoria en spark-submit
spark-submit --driver-memory 2g --executor-memory 2g procesamiento_batch.py
```

### Puerto 4040 Ocupado
```bash
# Cambiar puerto de la interfaz web
spark-submit --conf spark.ui.port=4041 procesamiento_batch.py
```

## Estado del Proyecto

### ✅ Completado

- [x] **Configuración del entorno**: Actualización del sistema, instalación de dependencias
- [x] **Dataset generado**: 100,000 transacciones sintéticas de e-commerce
- [x] **Kafka configurado**: ZooKeeper y Kafka funcionando correctamente
- [x] **Topic creado**: `transacciones_ventas` listo para streaming
- [x] **Spark Streaming**: Consumidor funcionando y procesando datos en tiempo real
- [x] **Documentación**: README completo con capturas de pantalla del proceso

### 🔄 En Progreso

- [ ] **Productor Kafka**: Ejecutándose para enviar transacciones simuladas
- [ ] **Procesamiento Batch**: Análisis exploratorio de datos completado
- [ ] **Monitoreo**: Interfaz web de Spark disponible en puerto 4040

### 📊 Resultados Obtenidos

- **Dataset**: 100,000 transacciones procesadas exitosamente
- **Kafka**: Streaming en tiempo real funcionando
- **Spark**: Análisis batch y streaming operativos
- **Capturas**: Documentación completa del proceso de implementación

## Autor

**appsgalvis** - Estudiante de Ingeniería de Sistemas UNAD
Curso: Big Data (202016911)
Tarea 3: Procesamiento de Datos con Apache Spark

## Repositorio GitHub

🔗 **URL del Repositorio**: [https://github.com/appsgalvis/spark-ecommerce-analytics](https://github.com/appsgalvis/spark-ecommerce-analytics)

## Licencia

Este proyecto es parte de una actividad académica de la Universidad Nacional Abierta y a Distancia (UNAD).