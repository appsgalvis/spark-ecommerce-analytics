#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesamiento Batch de Transacciones de E-commerce con Apache Spark
Autor: appsgalvis
Fecha: Octubre 2025
Descripción: Análisis exploratorio de datos (EDA) usando Spark DataFrames
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

def crear_sesion_spark():
    """Crea y configura la sesión de Spark"""
    
    spark = SparkSession.builder \
        .appName("EcommerceAnalytics") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    # Configurar nivel de logs
    spark.sparkContext.setLogLevel("WARN")
    
    print("Sesión de Spark creada exitosamente")
    return spark

def cargar_datos(spark, archivo_csv):
    """Carga los datos desde el archivo CSV"""
    
    print(f"Cargando datos desde: {archivo_csv}")
    
    # Definir esquema para optimizar la carga
    esquema = StructType([
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
    
    # Cargar datos
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "false") \
        .schema(esquema) \
        .csv(archivo_csv)
    
    print(f"Datos cargados: {df.count()} registros")
    return df

def limpiar_datos(df):
    """Realiza limpieza de datos"""
    
    print("\n=== LIMPIEZA DE DATOS ===")
    
    # Mostrar información inicial
    print(f"Registros iniciales: {df.count()}")
    print(f"Columnas: {df.columns}")
    
    # Verificar valores nulos
    print("\nValores nulos por columna:")
    df.select([count(when(col(c).isNull(), c)).alias(c) for c in df.columns]).show()
    
    # Eliminar registros con valores nulos críticos
    df_limpio = df.filter(
        (col("transaction_id").isNotNull()) &
        (col("customer_id").isNotNull()) &
        (col("total").isNotNull()) &
        (col("total") > 0)
    )
    
    print(f"Registros después de limpieza: {df_limpio.count()}")
    
    # Eliminar duplicados
    df_limpio = df_limpio.dropDuplicates(["transaction_id"])
    print(f"Registros después de eliminar duplicados: {df_limpio.count()}")
    
    return df_limpio

def analisis_exploratorio(df):
    """Realiza análisis exploratorio de datos"""
    
    print("\n=== ANÁLISIS EXPLORATORIO DE DATOS ===")
    
    # 1. Estadísticas descriptivas básicas
    print("\n1. Estadísticas descriptivas:")
    df.select("quantity", "unit_price", "total").describe().show()
    
    # 2. Total de ventas por categoría
    print("\n2. Total de ventas por categoría:")
    ventas_categoria = df.groupBy("category") \
        .agg(
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones"),
            avg("total").alias("promedio_venta")
        ) \
        .orderBy(desc("total_ventas"))
    
    ventas_categoria.show()
    
    # 3. Ventas por método de pago
    print("\n3. Ventas por método de pago:")
    ventas_metodo = df.groupBy("payment_method") \
        .agg(
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones"),
            avg("total").alias("promedio_venta")
        ) \
        .orderBy(desc("total_ventas"))
    
    ventas_metodo.show()
    
    # 4. Top 10 productos más vendidos
    print("\n4. Top 10 productos más vendidos:")
    top_productos = df.groupBy("product_id") \
        .agg(
            sum("quantity").alias("total_cantidad"),
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones")
        ) \
        .orderBy(desc("total_cantidad")) \
        .limit(10)
    
    top_productos.show()
    
    # 5. Análisis temporal - ventas por día
    print("\n5. Ventas por día:")
    df_con_fecha = df.withColumn("fecha", to_date(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))
    
    ventas_dia = df_con_fecha.groupBy("fecha") \
        .agg(
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones")
        ) \
        .orderBy("fecha")
    
    ventas_dia.show(20)
    
    # 6. Análisis por hora del día
    print("\n6. Ventas por hora del día:")
    df_con_hora = df.withColumn("hora", hour(to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")))
    
    ventas_hora = df_con_hora.groupBy("hora") \
        .agg(
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones")
        ) \
        .orderBy("hora")
    
    ventas_hora.show()
    
    # 7. Distribución de estados de transacción
    print("\n7. Distribución de estados de transacción:")
    estados = df.groupBy("status") \
        .agg(
            count("transaction_id").alias("cantidad"),
            sum("total").alias("total_ventas")
        ) \
        .orderBy(desc("cantidad"))
    
    estados.show()
    
    return df_con_fecha

def guardar_resultados(df, df_con_fecha):
    """Guarda los resultados procesados"""
    
    print("\n=== GUARDANDO RESULTADOS ===")
    
    # Crear directorio de resultados
    os.makedirs("resultados", exist_ok=True)
    
    # Guardar datos limpios en formato Parquet
    print("Guardando datos limpios en formato Parquet...")
    df.write.mode("overwrite").parquet("resultados/transacciones_limpias.parquet")
    
    # Guardar datos con fecha procesada
    print("Guardando datos con fecha procesada...")
    df_con_fecha.write.mode("overwrite").parquet("resultados/transacciones_con_fecha.parquet")
    
    # Guardar resumen de ventas por categoría
    print("Guardando resumen de ventas por categoría...")
    ventas_categoria = df.groupBy("category") \
        .agg(
            sum("total").alias("total_ventas"),
            count("transaction_id").alias("num_transacciones"),
            avg("total").alias("promedio_venta")
        ) \
        .orderBy(desc("total_ventas"))
    
    ventas_categoria.write.mode("overwrite").parquet("resultados/ventas_por_categoria.parquet")
    
    print("Resultados guardados exitosamente en la carpeta 'resultados/'")

def main():
    """Función principal"""
    
    print("=== PROCESAMIENTO BATCH CON APACHE SPARK ===")
    print("Análisis de Transacciones de E-commerce")
    
    # Crear sesión de Spark
    spark = crear_sesion_spark()
    
    try:
        # Cargar datos
        archivo_csv = "datos/transacciones_ventas.csv"
        df = cargar_datos(spark, archivo_csv)
        
        # Mostrar esquema y muestra de datos
        print("\nEsquema de los datos:")
        df.printSchema()
        
        print("\nMuestra de los datos:")
        df.show(5)
        
        # Limpiar datos
        df_limpio = limpiar_datos(df)
        
        # Análisis exploratorio
        df_con_fecha = analisis_exploratorio(df_limpio)
        
        # Guardar resultados
        guardar_resultados(df_limpio, df_con_fecha)
        
        print("\n=== PROCESAMIENTO COMPLETADO EXITOSAMENTE ===")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")
        raise
    
    finally:
        # Cerrar sesión de Spark
        spark.stop()
        print("Sesión de Spark cerrada")

if __name__ == "__main__":
    main()
