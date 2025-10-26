#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Dataset de Transacciones de E-commerce
Autor: appsgalvis
Fecha: Octubre 2025
Descripción: Genera datos sintéticos de transacciones de comercio electrónico
para análisis con Apache Spark
"""

import pandas as pd
import random
import datetime
import os

def generar_transaccion(id_transaccion):
    """Genera una transacción aleatoria"""
    
    # Categorías de productos
    categorias = ['Electrónica', 'Ropa', 'Hogar', 'Deportes', 'Libros']
    
    # Métodos de pago
    metodos_pago = ['Tarjeta', 'PayPal', 'Transferencia']
    
    # Estados de transacción
    estados = ['Completada', 'Pendiente', 'Cancelada']
    
    # Generar timestamp aleatorio en los últimos 30 días
    fecha_base = datetime.datetime.now() - datetime.timedelta(days=30)
    dias_aleatorios = random.randint(0, 30)
    horas_aleatorias = random.randint(0, 23)
    minutos_aleatorios = random.randint(0, 59)
    
    timestamp = fecha_base + datetime.timedelta(
        days=dias_aleatorios, 
        hours=horas_aleatorias, 
        minutes=minutos_aleatorios
    )
    
    # Generar datos de la transacción
    customer_id = random.randint(1000, 9999)
    product_id = random.randint(10000, 99999)
    categoria = random.choice(categorias)
    cantidad = random.randint(1, 10)
    
    # Precios por categoría
    precios_base = {
        'Electrónica': (50, 2000),
        'Ropa': (20, 500),
        'Hogar': (30, 800),
        'Deportes': (25, 600),
        'Libros': (10, 100)
    }
    
    precio_min, precio_max = precios_base[categoria]
    precio_unitario = round(random.uniform(precio_min, precio_max), 2)
    total = round(cantidad * precio_unitario, 2)
    
    metodo_pago = random.choice(metodos_pago)
    estado = random.choice(estados)
    
    return {
        'transaction_id': id_transaccion,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'customer_id': customer_id,
        'product_id': product_id,
        'category': categoria,
        'quantity': cantidad,
        'unit_price': precio_unitario,
        'total': total,
        'payment_method': metodo_pago,
        'status': estado
    }

def generar_dataset(numero_transacciones=100000):
    """Genera el dataset completo de transacciones"""
    
    print(f"Generando {numero_transacciones} transacciones...")
    
    transacciones = []
    
    for i in range(1, numero_transacciones + 1):
        if i % 10000 == 0:
            print(f"Procesadas {i} transacciones...")
        
        transaccion = generar_transaccion(i)
        transacciones.append(transaccion)
    
    # Crear DataFrame
    df = pd.DataFrame(transacciones)
    
    # Crear directorio si no existe
    os.makedirs('datos', exist_ok=True)
    
    # Guardar en CSV
    archivo_csv = 'datos/transacciones_ventas.csv'
    df.to_csv(archivo_csv, index=False)
    
    print(f"\nDataset generado exitosamente!")
    print(f"Archivo guardado: {archivo_csv}")
    print(f"Total de registros: {len(df)}")
    print(f"Tamaño del archivo: {os.path.getsize(archivo_csv) / (1024*1024):.2f} MB")
    
    # Mostrar estadísticas básicas
    print(f"\nEstadísticas del dataset:")
    print(f"- Categorías: {df['category'].nunique()}")
    print(f"- Clientes únicos: {df['customer_id'].nunique()}")
    print(f"- Productos únicos: {df['product_id'].nunique()}")
    print(f"- Rango de fechas: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"- Total de ventas: ${df['total'].sum():,.2f}")
    
    return df

if __name__ == "__main__":
    # Generar dataset con 100,000 transacciones
    dataset = generar_dataset(100000)
    
    # Mostrar muestra de los datos
    print(f"\nPrimeras 5 transacciones:")
    print(dataset.head())
    
    print(f"\nÚltimas 5 transacciones:")
    print(dataset.tail())
