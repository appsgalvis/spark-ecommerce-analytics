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

## Conexión al Servidor

Antes de comenzar, necesitas conectarte al servidor Hadoop por SSH:

### Windows

```bash
# Conectarse al servidor Hadoop por SSH
ssh vboxuser@192.168.0.4
```

**Nota**: Reemplaza `192.168.0.4` con la IP de tu servidor Hadoop si es diferente.

### Linux/Mac

```bash
# Conectarse al servidor Hadoop por SSH
ssh vboxuser@<IP_DEL_SERVIDOR>
```

## Instrucciones de Instalación y Ejecución

**Nota**: El servidor Hadoop y Spark ya deben estar preconfigurados y funcionando correctamente. Estas instrucciones cubren la configuración de Kafka y la ejecución de la aplicación.

### 1. Actualización del Sistema

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y
```

![Actualización del Sistema](imagenes/Toma%20captura%20de%20la%20actualizaci%C3%B3n%20del%20sistema.png)

### 2. Verificación de Versiones

```bash
# Verificar versiones de Python y pip
python3 --version
pip3 --version
```

![Versiones de Python y pip](imagenes/Captura%20las%20versiones%20de%20Python%20y%20pip.png)

### 3. Clonación del Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/appsgalvis/spark-ecommerce-analytics.git
cd spark-ecommerce-analytics
```

![Clonación del Repositorio](imagenes/Toma%20captura%20de%20la%20clonaci%C3%B3n%20exitosa%20del%20repositorio.png)

### 3.1. Transferir Dataset al Servidor

**Opción A: Desde Windows (usando SCP)**
```bash
# Desde PowerShell en Windows, transferir el dataset al servidor
scp datos/transacciones_ventas.csv vboxuser@192.168.0.4:~/spark-ecommerce-analytics/datos/
```

**Opción B: Generar el dataset directamente en el servidor**
```bash
# En el servidor Hadoop, ejecutar el generador
python3 generar_dataset_ventas.py
```

### 4. Instalación de Dependencias

```bash
# Instalar dependencias Python
pip3 install -r requirements.txt
```

![Instalación de Dependencias](imagenes/Captura%20la%20instalaci%C3%B3n%20exitosa%20de%20las%20dependencias%20Python.png)

```bash
# Verificar librerías instaladas
pip3 list | grep -E "(pyspark|kafka|pandas|numpy)"
```

![Verificación de Librerías](imagenes/Captura%20la%20verificaci%C3%B3n%20de%20las%20librer%C3%ADas%20instaladas.png)

```bash
# Verificar importación de librerías
python3 -c "import kafka; print('Kafka instalado correctamente')"
python3 -c "import pandas; print('Pandas instalado correctamente')"
```

### 5. Verificación de Servicios Hadoop

```bash
# Verificar servicios Hadoop ejecutándose
jps
```

![Servicios Hadoop](imagenes/Captura%20la%20salida%20de%20jps%20mostrando%20los%20servicios%20de%20Hadoop.png)

```bash
# Verificar versión de Spark
spark-shell --version
```

![Versión de Spark](imagenes/Captura%20la%20versi%C3%B3n%20de%20Spark%20instalada.png)

### 6. Verificación del Dataset

```bash
# Verificar que el dataset existe
ls -la datos/
head -5 datos/transacciones_ventas.csv
```

![Dataset CSV](imagenes/Captura%20la%20verificaci%C3%B3n%20del%20dataset%20CSV.png)

### 7. Configuración de Kafka

```bash
# Descargar Kafka
wget https://archive.apache.org/dist/kafka/3.6.2/kafka_2.13-3.6.2.tgz

# Descomprimir y mover
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka
```

![Descarga de Kafka](imagenes/Captura%20la%20descarga%20%2C%20descompresi%C3%B3n%20y%20configuraci%C3%B3n%20de%20Kafka..png)

```bash
# Iniciar ZooKeeper (en una terminal separada)
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Iniciar Kafka (en otra terminal separada)
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

![Inicio de Kafka](imagenes/Captura%20el%20inicio%20de%20Kafka.png)

```bash
# Crear topic para transacciones
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transacciones_ventas

# Verificar que el topic fue creado
/opt/Kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

![Creación del Topic](imagenes/Captura%20la%20creaci%C3%B3n%20exitosa%20del%20topic.png)

## Código Python del Proyecto

### 1. Generador de Dataset (`generar_dataset_ventas.py`)

```python
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generar_datos_ecommerce(num_registros=100000):
    """
    Genera un dataset sintético de transacciones de e-commerce
    """
    # Configuración de datos
    categorias = ['Electrónica', 'Ropa', 'Hogar', 'Deportes', 'Libros']
    metodos_pago = ['Tarjeta', 'PayPal', 'Transferencia']
    estados = ['Completada', 'Pendiente', 'Cancelada']
    
    # Generar datos aleatorios
    datos = []
    fecha_inicio = datetime.now() - timedelta(days=30)
    
    for i in range(num_registros):
        # Generar timestamp aleatorio en los últimos 30 días
        timestamp = fecha_inicio + timedelta(
            seconds=random.randint(0, 30 * 24 * 60 * 60)
        )
        
        # Generar datos de la transacción
        transaction_id = i + 1
        customer_id = random.randint(1, 10000)
        product_id = random.randint(1, 5000)
        category = random.choice(categorias)
        quantity = random.randint(1, 10)
        unit_price = round(random.uniform(10, 1000), 2)
        total = round(quantity * unit_price, 2)
        payment_method = random.choice(metodos_pago)
        status = random.choice(estados)
        
        datos.append({
            'transaction_id': transaction_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'customer_id': customer_id,
            'product_id': product_id,
            'category': category,
            'quantity': quantity,
            'unit_price': unit_price,
            'total': total,
            'payment_method': payment_method,
            'status': status
        })
    
    return pd.DataFrame(datos)

if __name__ == "__main__":
    print("=== GENERADOR DE DATASET E-COMMERCE ===")
    print("Generando 100,000 transacciones sintéticas...")
    
    # Generar dataset
    df = generar_datos_ecommerce(100000)
    
    # Crear directorio si no existe
    import os
    os.makedirs('datos', exist_ok=True)
    
    # Guardar dataset
    df.to_csv('datos/transacciones_ventas.csv', index=False)
    
    print(f"✅ Dataset generado exitosamente!")
    print(f"📊 Total de registros: {len(df):,}")
    print(f"📁 Archivo guardado: datos/transacciones_ventas.csv")
    print(f"📈 Categorías: {df['category'].nunique()}")
    print(f"💰 Rango de ventas: ${df['total'].min():.2f} - ${df['total'].max():.2f}")
```

### 2. Procesamiento Batch (`procesamiento_batch.py`)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, desc, to_timestamp, hour, dayofweek, date_format
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType

def crear_sesion_spark():
    """Crear sesión de Spark"""
    return SparkSession.builder \
        .appName("EcommerceBatchAnalytics") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def cargar_datos(spark):
    """Cargar datos desde CSV"""
    schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("timestamp", StringType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("total", DoubleType(), True),
        StructField("payment_method", StringType(), True),
        StructField("status", StringType(), True)
    ])
    
    return spark.read \
        .option("header", "true") \
        .schema(schema) \
        .csv("datos/transacciones_ventas.csv")

def limpiar_datos(df):
    """Limpiar datos eliminando nulos y duplicados"""
    print("🧹 Limpiando datos...")
    
    # Eliminar registros con valores nulos
    df_limpio = df.filter(col("transaction_id").isNotNull())
    df_limpio = df_limpio.filter(col("customer_id").isNotNull())
    df_limpio = df_limpio.filter(col("total").isNotNull())
    df_limpio = df_limpio.filter(col("total") > 0)
    
    # Eliminar duplicados
    df_limpio = df_limpio.dropDuplicates(["transaction_id"])
    
    print(f"✅ Datos limpiados: {df_limpio.count():,} registros")
    return df_limpio

def agregar_columnas_temporales(df):
    """Agregar columnas de análisis temporal"""
    print("📅 Agregando columnas temporales...")
    
    df_con_fecha = df.withColumn("timestamp_parsed", 
                                to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))
    df_con_fecha = df_con_fecha.withColumn("hora", hour(col("timestamp_parsed")))
    df_con_fecha = df_con_fecha.withColumn("dia_semana", dayofweek(col("timestamp_parsed")))
    df_con_fecha = df_con_fecha.withColumn("fecha", date_format(col("timestamp_parsed"), "yyyy-MM-dd"))
    
    return df_con_fecha

def analisis_exploratorio(df):
    """Realizar análisis exploratorio de datos"""
    print("\n📊 === ANÁLISIS EXPLORATORIO DE DATOS ===")
    
    # Estadísticas básicas
    print("\n1. ESTADÍSTICAS BÁSICAS:")
    df.select("total").describe().show()
    
    # Ventas por categoría
    print("\n2. VENTAS POR CATEGORÍA:")
    ventas_categoria = df.groupBy("category") \
        .agg(
            count("*").alias("total_transacciones"),
            sum("total").alias("ventas_totales"),
            avg("total").alias("promedio_venta")
        ) \
        .orderBy(desc("ventas_totales"))
    ventas_categoria.show()
    
    # Métodos de pago más utilizados
    print("\n3. MÉTODOS DE PAGO MÁS UTILIZADOS:")
    metodos_pago = df.groupBy("payment_method") \
        .agg(
            count("*").alias("total_transacciones"),
            sum("total").alias("ventas_totales")
        ) \
        .orderBy(desc("total_transacciones"))
    metodos_pago.show()
    
    # Top 10 productos más vendidos
    print("\n4. TOP 10 PRODUCTOS MÁS VENDIDOS:")
    top_productos = df.groupBy("product_id") \
        .agg(
            count("*").alias("total_transacciones"),
            sum("quantity").alias("total_cantidad"),
            sum("total").alias("ventas_totales")
        ) \
        .orderBy(desc("total_transacciones")) \
        .limit(10)
    top_productos.show()
    
    # Análisis temporal
    print("\n5. ANÁLISIS TEMPORAL:")
    ventas_por_hora = df.groupBy("hora") \
        .agg(
            count("*").alias("transacciones"),
            sum("total").alias("ventas_totales")
        ) \
        .orderBy("hora")
    ventas_por_hora.show()
    
    # Estados de transacción
    print("\n6. DISTRIBUCIÓN DE ESTADOS:")
    estados = df.groupBy("status") \
        .agg(
            count("*").alias("total_transacciones"),
            sum("total").alias("ventas_totales")
        ) \
        .orderBy(desc("total_transacciones"))
    estados.show()
    
    return ventas_categoria

def guardar_resultados(df_limpio, df_con_fecha, ventas_categoria):
    """Guardar resultados procesados"""
    print("\n💾 Guardando resultados...")
    
    # Crear directorio de resultados
    import os
    os.makedirs("resultados", exist_ok=True)
    
    # Guardar datos limpios
    df_limpio.write.mode("overwrite").parquet("resultados/transacciones_limpias.parquet")
    
    # Guardar datos con columnas temporales
    df_con_fecha.write.mode("overwrite").parquet("resultados/transacciones_con_fecha.parquet")
    
    # Guardar análisis por categoría
    ventas_categoria.write.mode("overwrite").parquet("resultados/ventas_por_categoria.parquet")
    
    print("✅ Resultados guardados en formato Parquet")

def main():
    """Función principal"""
    print("=== PROCESAMIENTO BATCH - E-COMMERCE ANALYTICS ===")
    
    # Crear sesión de Spark
    spark = crear_sesion_spark()
    spark.sparkContext.setLogLevel("WARN")
    
    try:
        # Cargar datos
        print("📂 Cargando datos...")
        df = cargar_datos(spark)
        print(f"✅ Datos cargados: {df.count():,} registros")
        
        # Limpiar datos
        df_limpio = limpiar_datos(df)
        
        # Agregar columnas temporales
        df_con_fecha = agregar_columnas_temporales(df_limpio)
        
        # Análisis exploratorio
        ventas_categoria = analisis_exploratorio(df_con_fecha)
        
        # Guardar resultados
        guardar_resultados(df_limpio, df_con_fecha, ventas_categoria)
        
        print("\n🎉 Procesamiento batch completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
```

### 3. Productor Kafka (`kafka_productor_ventas.py`)

```python
import time
import json
import random
from kafka import KafkaProducer
from datetime import datetime

def generar_datos_transaccion():
    """Generar datos de transacción simulada"""
    categorias = ['Electrónica', 'Ropa', 'Hogar', 'Deportes', 'Libros']
    metodos_pago = ['Tarjeta', 'PayPal', 'Transferencia']
    estados = ['Completada', 'Pendiente', 'Cancelada']
    
    # Generar datos aleatorios
    transaction_id = random.randint(100001, 999999)
    customer_id = random.randint(1, 10000)
    product_id = random.randint(1, 5000)
    category = random.choice(categorias)
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(10, 1000), 2)
    total = round(quantity * unit_price, 2)
    payment_method = random.choice(metodos_pago)
    status = random.choice(estados)
    
    return {
        'transaction_id': transaction_id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'customer_id': customer_id,
        'product_id': product_id,
        'category': category,
        'quantity': quantity,
        'unit_price': unit_price,
        'total': total,
        'payment_method': payment_method,
        'status': status
    }

def main():
    """Función principal del productor"""
    print("=== PRODUCTOR KAFKA - TRANSACCIONES E-COMMERCE ===")
    print("Enviando transacciones simuladas a Kafka...")
    
    # Configurar productor
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    
    try:
        contador = 0
        while True:
            # Generar transacción
            transaction_data = generar_datos_transaccion()
            
            # Enviar a Kafka
            producer.send('transacciones_ventas', value=transaction_data)
            
            contador += 1
            print(f"📤 Transacción #{contador} enviada: ID {transaction_data['transaction_id']} - ${transaction_data['total']:.2f} - {transaction_data['category']}")
            
            # Esperar 1 segundo antes de enviar la siguiente
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Productor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error en el productor: {str(e)}")
    finally:
        producer.close()
        print("✅ Productor cerrado correctamente")

if __name__ == "__main__":
    main()
```

### 4. Consumidor Spark Streaming (`spark_streaming_consumidor.py`)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, count, avg
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType
import logging

def crear_sesion_spark():
    """Crear sesión de Spark para streaming"""
    return SparkSession.builder \
        .appName("EcommerceStreamingAnalytics") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3") \
        .getOrCreate()

def configurar_kafka_stream(spark):
    """Configurar stream de Kafka"""
    print("=== CONFIGURANDO SPARK STREAMING ===")
    
    # Definir esquema de datos
    schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("timestamp", StringType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DoubleType(), True),
        StructField("total", DoubleType(), True),
        StructField("payment_method", StringType(), True),
        StructField("status", StringType(), True)
    ])
    
    # Crear stream desde Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transacciones_ventas") \
        .load()
    
    print("Configuración de Kafka completada")
    
    # Parsear datos JSON
    df_parsed = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    print("Parsing de datos JSON completado")
    
    return df_parsed

def configurar_analisis_streaming(df):
    """Configurar análisis de streaming"""
    print("Configurando análisis por ventanas de tiempo...")
    
    # 1. Total de ventas por ventana (1 minuto)
    ventas_por_ventana = df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(window(col("timestamp"), "1 minute")) \
        .agg(
            count("*").alias("total_transacciones"),
            sum("total").alias("ventas_totales"),
            avg("total").alias("promedio_venta")
        ) \
        .select(
            col("window.start").alias("inicio_ventana"),
            col("window.end").alias("fin_ventana"),
            col("total_transacciones"),
            col("ventas_totales"),
            col("promedio_venta")
        )
    
    # 2. Ventas por categoría
    ventas_por_categoria = df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(window(col("timestamp"), "1 minute"), col("category")) \
        .agg(
            count("*").alias("transacciones"),
            sum("total").alias("ventas_totales")
        ) \
        .select(
            col("window.start").alias("inicio_ventana"),
            col("category"),
            col("transacciones"),
            col("ventas_totales")
        )
    
    # 3. Métodos de pago más utilizados
    metodos_pago = df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(window(col("timestamp"), "1 minute"), col("payment_method")) \
        .agg(count("*").alias("total_transacciones")) \
        .select(
            col("window.start").alias("inicio_ventana"),
            col("payment_method"),
            col("total_transacciones")
        )
    
    # 4. Transacciones por estado
    transacciones_por_estado = df \
        .withWatermark("timestamp", "1 minute") \
        .groupBy(window(col("timestamp"), "1 minute"), col("status")) \
        .agg(count("*").alias("total_transacciones")) \
        .select(
            col("window.start").alias("inicio_ventana"),
            col("status"),
            col("total_transacciones")
        )
    
    print("Análisis configurado. Iniciando streaming...")
    
    return ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_por_estado

def iniciar_streaming(ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_por_estado):
    """Iniciar el procesamiento de streaming"""
    print("\n=== INICIANDO PROCESAMIENTO EN TIEMPO REAL ===")
    print("Presiona Ctrl+C para detener el streaming\n")
    
    # Configurar queries de streaming
    query1 = ventas_por_ventana \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    query2 = ventas_por_categoria \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    query3 = metodos_pago \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    query4 = transacciones_por_estado \
        .writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    print("1. TOTAL DE VENTAS POR VENTANA (1 minuto):")
    print("2. VENTAS POR CATEGORÍA:")
    print("3. MÉTODOS DE PAGO MÁS UTILIZADOS:")
    print("4. TRANSACCIONES POR ESTADO:")
    
    # Esperar a que terminen las queries
    try:
        query1.awaitTermination()
        query2.awaitTermination()
        query3.awaitTermination()
        query4.awaitTermination()
    except KeyboardInterrupt:
        print("\n🛑 Streaming detenido por el usuario")
        query1.stop()
        query2.stop()
        query3.stop()
        query4.stop()

def main():
    """Función principal"""
    print("=== CONSUMIDOR SPARK STREAMING - TRANSACCIONES E-COMMERCE ===")
    print("Procesando transacciones de ventas en tiempo real desde Kafka...")
    
    # Crear sesión de Spark
    spark = crear_sesion_spark()
    spark.sparkContext.setLogLevel("WARN")
    
    print("Sesión de Spark Streaming creada exitosamente")
    
    try:
        # Configurar stream de Kafka
        df_stream = configurar_kafka_stream(spark)
        
        # Configurar análisis
        ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_por_estado = configurar_analisis_streaming(df_stream)
        
        # Iniciar streaming
        iniciar_streaming(ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_por_estado)
        
    except Exception as e:
        print(f"❌ Error durante el streaming: {str(e)}")
    finally:
        spark.stop()
        print("✅ Sesión de Spark cerrada correctamente")

if __name__ == "__main__":
    main()
```

### 5. Archivo de Dependencias (`requirements.txt`)

```
pyspark==3.5.3
kafka-python==2.0.2
pandas==2.0.3
numpy==1.24.3
py4j==0.10.9.7
```

## Ejecución del Proyecto

### 8. Procesamiento Batch

```bash
# Ejecutar procesamiento batch
spark-submit procesamiento_batch.py
```

![Ejecución Batch a](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20a.png)

![Ejecución Batch b](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20b.png)

![Ejecución Batch c](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20c.png)

![Ejecución Batch d](imagenes/Captura%20la%20ejecuci%C3%B3n%20del%20procesamiento%20batch%20y%20los%20resultados%20del%20an%C3%A1lisis%20exploratorio%20d.png)

```bash
# Verificar archivos Parquet generados
ls -la resultados/
```

![Archivos Parquet](imagenes/Captura%20los%20archivos%20Parquet%20generado.png)

### 8.1. Descargar Resultados del Servidor (Opcional)

**Para descargar los archivos Parquet generados desde el servidor:**

```bash
# Desde Windows, descargar los resultados del servidor
scp -r vboxuser@192.168.0.4:~/spark-ecommerce-analytics/resultados/ ./resultados/
```

**Nota**: Los archivos de resultados se generan automáticamente en el servidor durante el procesamiento batch y permanecen allí para análisis posterior.

### 9. Streaming en Tiempo Real

#### Terminal 1 - Productor Kafka:

```bash
# Ejecutar productor Kafka
python3 kafka_productor_ventas.py
```

![Productor Kafka](imagenes/Captura%20el%20productor%20enviando%20transacciones.png)

#### Terminal 2 - Consumidor Spark Streaming:

```bash
# Ejecutar consumidor Spark Streaming
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumidor.py
```

![Consumidor Streaming](imagenes/Captura%20el%20consumidor%20procesando%20datos%20en%20tiempo%20real.png)

### 10. Interfaz Web de Spark

Acceder a la interfaz web de Spark en: `http://192.168.0.4:4040`

![Spark UI Jobs](imagenes/Captura%20la%20interfaz%20web%20de%20Spark%20mostrando%20jobs..png)

![Spark UI Streaming](imagenes/Captura%20la%20interfaz%20web%20de%20Spark%20mostrando%20StreamingQuery.png)

### 11. Estructura del Proyecto

```bash
# Ver estructura de directorios
tree spark-ecommerce-analytics/
```

![Estructura de Directorios](imagenes/Captura%20la%20estructura%20de%20directorios%20creada.png)

## Estructura del Proyecto

```
spark-ecommerce-analytics/
├── datos/
│   └── transacciones_ventas.csv          # Dataset de entrada
├── resultados/                            # Resultados del procesamiento batch (generados en el servidor)
│   ├── transacciones_limpias.parquet
│   ├── transacciones_con_fecha.parquet
│   └── ventas_por_categoria.parquet
├── imagenes/                              # Capturas de pantalla del proceso
│   ├── Toma captura de la actualización del sistema.png
│   ├── Captura las versiones de Python y pip.png
│   └── ... (todas las capturas)
├── generar_dataset_ventas.py             # Generador de dataset
├── procesamiento_batch.py                 # Script de procesamiento batch
├── kafka_productor_ventas.py             # Productor de Kafka
├── spark_streaming_consumidor.py         # Consumidor Spark Streaming
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

## Monitoreo y Visualización

### Interfaz Web de Spark
Acceder a: `http://192.168.0.4:4040` para ver:
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

**Cristian Johan Galvis Bernal** - Estudiante de Ingeniería de Sistemas UNAD
Curso: Big Data (202016911)
Tarea 3: Procesamiento de Datos con Apache Spark

## Repositorio GitHub

🔗 **URL del Repositorio**: [https://github.com/appsgalvis/spark-ecommerce-analytics](https://github.com/appsgalvis/spark-ecommerce-analytics)

## Licencia

Este proyecto es parte de una actividad académica de la Universidad Nacional Abierta y a Distancia (UNAD).