#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consumidor Spark Streaming para Transacciones de E-commerce
Autor: appsgalvis
Fecha: Octubre 2025
Descripción: Procesa transacciones de ventas en tiempo real desde Kafka
basado en el ejemplo del Anexo 3 pero adaptado para datos de e-commerce
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as spark_sum, count, avg, max as spark_max
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType, TimestampType
import logging

def crear_sesion_spark():
    """Crea y configura la sesión de Spark para streaming"""
    
    spark = SparkSession.builder \
        .appName("EcommerceStreamingAnalytics") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    # Configurar nivel de logs
    spark.sparkContext.setLogLevel("WARN")
    
    print("Sesión de Spark Streaming creada exitosamente")
    return spark

def definir_esquema_transacciones():
    """Define el esquema de los datos de transacciones"""
    
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
    
    return schema

def procesar_streaming(spark, schema):
    """Configura y ejecuta el procesamiento de streaming"""
    
    print("=== CONFIGURANDO SPARK STREAMING ===")
    
    # Configurar el lector de streaming para leer desde Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "transacciones_ventas") \
        .option("startingOffsets", "latest") \
        .load()
    
    print("Configuración de Kafka completada")
    
    # Parsear los datos JSON
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")
    
    # Convertir timestamp a formato correcto
    parsed_df = parsed_df.withColumn(
        "timestamp_parsed", 
        col("timestamp").cast(TimestampType())
    )
    
    print("Parsing de datos JSON completado")
    
    # Calcular estadísticas por ventana de tiempo (1 minuto)
    print("Configurando análisis por ventanas de tiempo...")
    
    # 1. Total de ventas por ventana de tiempo
    ventas_por_ventana = parsed_df \
        .groupBy(window(col("timestamp_parsed"), "1 minute")) \
        .agg(
            spark_sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones"),
            avg("total").alias("promedio_venta")
        ) \
        .orderBy("window")
    
    # 2. Ventas por categoría en tiempo real
    ventas_por_categoria = parsed_df \
        .groupBy(
            window(col("timestamp_parsed"), "1 minute"),
            col("category")
        ) \
        .agg(
            spark_sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones")
        ) \
        .orderBy("window", col("total_ventas").desc())
    
    # 3. Métodos de pago más utilizados
    metodos_pago = parsed_df \
        .groupBy(
            window(col("timestamp_parsed"), "1 minute"),
            col("payment_method")
        ) \
        .agg(
            count("transaction_id").alias("num_transacciones"),
            spark_sum("total").alias("total_ventas")
        ) \
        .orderBy("window", col("num_transacciones").desc())
    
    # 4. Transacciones por estado
    transacciones_estado = parsed_df \
        .groupBy(
            window(col("timestamp_parsed"), "1 minute"),
            col("status")
        ) \
        .agg(
            count("transaction_id").alias("cantidad"),
            spark_sum("total").alias("total_ventas")
        ) \
        .orderBy("window", col("cantidad").desc())
    
    print("Análisis configurado. Iniciando streaming...")
    
    return ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_estado

def ejecutar_queries_streaming(ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_estado):
    """Ejecuta las queries de streaming"""
    
    print("\n=== INICIANDO PROCESAMIENTO EN TIEMPO REAL ===")
    print("Presiona Ctrl+C para detener el streaming")
    
    try:
        # Query 1: Ventas totales por ventana
        print("\n1. TOTAL DE VENTAS POR VENTANA (1 minuto):")
        query1 = ventas_por_ventana \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        # Query 2: Ventas por categoría
        print("\n2. VENTAS POR CATEGORÍA:")
        query2 = ventas_por_categoria \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        # Query 3: Métodos de pago
        print("\n3. MÉTODOS DE PAGO MÁS UTILIZADOS:")
        query3 = metodos_pago \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        # Query 4: Estados de transacción
        print("\n4. TRANSACCIONES POR ESTADO:")
        query4 = transacciones_estado \
            .writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .start()
        
        # Esperar terminación
        query1.awaitTermination()
        
    except KeyboardInterrupt:
        print("\n\nStreaming detenido por el usuario")
        
    except Exception as e:
        print(f"Error durante el streaming: {str(e)}")
        
    finally:
        # Detener todas las queries
        try:
            query1.stop()
            query2.stop()
            query3.stop()
            query4.stop()
            print("Todas las queries de streaming detenidas")
        except:
            pass

def main():
    """Función principal"""
    
    print("=== CONSUMIDOR SPARK STREAMING - TRANSACCIONES E-COMMERCE ===")
    print("Procesando transacciones de ventas en tiempo real desde Kafka...")
    
    # Crear sesión de Spark
    spark = crear_sesion_spark()
    
    try:
        # Definir esquema
        schema = definir_esquema_transacciones()
        
        # Configurar streaming
        ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_estado = procesar_streaming(spark, schema)
        
        # Ejecutar queries de streaming
        ejecutar_queries_streaming(ventas_por_ventana, ventas_por_categoria, metodos_pago, transacciones_estado)
        
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        raise
        
    finally:
        # Cerrar sesión de Spark
        spark.stop()
        print("Sesión de Spark cerrada")

if __name__ == "__main__":
    main()
