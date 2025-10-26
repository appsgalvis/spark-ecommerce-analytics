#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Productor de Kafka para Transacciones de E-commerce en Tiempo Real
Autor: appsgalvis
Fecha: Octubre 2025
Descripción: Simula la generación de transacciones de ventas en tiempo real
basado en el ejemplo del Anexo 3 pero adaptado para datos de e-commerce
"""

import time
import json
import random
from datetime import datetime, timedelta
from kafka import KafkaProducer

def generar_transaccion_tiempo_real():
    """Genera una transacción aleatoria para streaming"""
    
    # Categorías de productos
    categorias = ['Electrónica', 'Ropa', 'Hogar', 'Deportes', 'Libros']
    
    # Métodos de pago
    metodos_pago = ['Tarjeta', 'PayPal', 'Transferencia']
    
    # Estados de transacción (mayoría completadas para simular ventas reales)
    estados = ['Completada', 'Completada', 'Completada', 'Pendiente', 'Cancelada']
    
    # Generar datos de la transacción
    transaction_id = random.randint(100000, 999999)
    customer_id = random.randint(1000, 9999)
    product_id = random.randint(10000, 99999)
    categoria = random.choice(categorias)
    cantidad = random.randint(1, 5)  # Cantidades más pequeñas para tiempo real
    
    # Precios por categoría (similares al dataset batch)
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
    
    # Timestamp actual
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        "transaction_id": transaction_id,
        "timestamp": timestamp,
        "customer_id": customer_id,
        "product_id": product_id,
        "category": categoria,
        "quantity": cantidad,
        "unit_price": precio_unitario,
        "total": total,
        "payment_method": metodo_pago,
        "status": estado
    }

def main():
    """Función principal del productor"""
    
    print("=== PRODUCTOR KAFKA - TRANSACCIONES E-COMMERCE ===")
    print("Generando transacciones de ventas en tiempo real...")
    print("Presiona Ctrl+C para detener")
    
    # Configurar el productor de Kafka
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        # Configuraciones adicionales para mejor rendimiento
        batch_size=16384,
        linger_ms=10,
        compression_type='gzip'
    )
    
    contador = 0
    
    try:
        while True:
            # Generar transacción
            transaccion = generar_transaccion_tiempo_real()
            
            # Enviar al topic de Kafka
            producer.send('transacciones_ventas', value=transaccion)
            
            contador += 1
            
            # Mostrar información cada 10 transacciones
            if contador % 10 == 0:
                print(f"[{contador}] Enviada transacción: ID={transaccion['transaction_id']}, "
                      f"Categoría={transaccion['category']}, Total=${transaccion['total']}")
            else:
                print(f"Enviada: {transaccion}")
            
            # Esperar 1 segundo antes de la siguiente transacción
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n\nProductor detenido por el usuario")
        print(f"Total de transacciones enviadas: {contador}")
        
    except Exception as e:
        print(f"Error en el productor: {str(e)}")
        
    finally:
        # Cerrar el productor
        producer.close()
        print("Productor de Kafka cerrado")

if __name__ == "__main__":
    main()
