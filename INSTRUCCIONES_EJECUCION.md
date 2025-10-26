# Instrucciones de Ejecución - Spark E-commerce Analytics

## Guía Paso a Paso para Ejecutar en la Máquina Virtual

### Prerrequisitos

1. **Conexión SSH a la VM**
   - IP: `192.168.0.x` (verificar IP actual)
   - Usuario: `vboxuser`
   - Contraseña: `bigdata`

2. **Verificar Servicios**
   ```bash
   # Verificar que Hadoop esté ejecutándose
   jps
   
   # Verificar que Spark esté disponible
   spark-shell --version
   ```

### Paso 1: Preparar el Entorno

```bash
# Conectarse por SSH
ssh vboxuser@192.168.0.x

# Crear directorio del proyecto
mkdir -p ~/spark-ecommerce-analytics
cd ~/spark-ecommerce-analytics

# Crear estructura de directorios
mkdir -p datos batch streaming resultados
```

### Paso 2: Instalar Dependencias

```bash
# Instalar kafka-python
pip install kafka-python

# Verificar instalación
python3 -c "import kafka; print('Kafka instalado correctamente')"
```

### Paso 3: Configurar Kafka

```bash
# Descargar Kafka (si no está instalado)
wget https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
tar -xzf kafka_2.13-3.6.2.tgz
sudo mv kafka_2.13-3.6.2 /opt/Kafka

# Iniciar ZooKeeper (en terminal separada)
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &

# Esperar unos segundos y presionar Enter

# Iniciar Kafka (en terminal separada)
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &

# Esperar unos segundos y presionar Enter

# Crear topic para transacciones
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transacciones_ventas

# Verificar que el topic se creó
/opt/Kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Paso 4: Subir Archivos del Proyecto

**Opción A: Usando SCP (desde Windows)**
```bash
# Desde PowerShell en Windows
scp generar_dataset_ventas.py vboxuser@192.168.0.x:~/spark-ecommerce-analytics/
scp procesamiento_batch.py vboxuser@192.168.0.x:~/spark-ecommerce-analytics/batch/
scp kafka_productor_ventas.py vboxuser@192.168.0.x:~/spark-ecommerce-analytics/streaming/
scp spark_streaming_consumidor.py vboxuser@192.168.0.x:~/spark-ecommerce-analytics/streaming/
scp requirements.txt vboxuser@192.168.0.x:~/spark-ecommerce-analytics/
```

**Opción B: Crear archivos directamente en la VM**
```bash
# Usar nano para crear cada archivo
nano generar_dataset_ventas.py
# Copiar y pegar el contenido del archivo
# Ctrl+O para guardar, Enter, Ctrl+X para salir
```

### Paso 5: Generar Dataset

```bash
# Ejecutar generador de dataset
python3 generar_dataset_ventas.py

# Verificar que se creó el archivo
ls -la datos/
head datos/transacciones_ventas.csv
```

### Paso 6: Ejecutar Procesamiento Batch

```bash
# Ejecutar análisis batch
spark-submit procesamiento_batch.py

# Verificar resultados
ls -la resultados/
```

### Paso 7: Ejecutar Streaming en Tiempo Real

**Terminal 1 - Productor Kafka:**
```bash
cd ~/spark-ecommerce-analytics/streaming
python3 kafka_productor_ventas.py
```

**Terminal 2 - Consumidor Spark Streaming:**
```bash
cd ~/spark-ecommerce-analytics/streaming
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumidor.py
```

### Paso 8: Monitoreo

1. **Interfaz Web de Spark**
   - Abrir navegador: `http://192.168.0.x:4040`
   - Ver jobs ejecutándose
   - Monitorear métricas

2. **Verificar Kafka**
   ```bash
   # Ver mensajes en el topic
   /opt/Kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic transacciones_ventas --from-beginning
   ```

### Paso 9: Capturar Resultados

1. **Capturas de Pantalla Necesarias:**
   - Ejecución del procesamiento batch
   - Resultados del análisis exploratorio
   - Kafka producer generando datos
   - Spark Streaming procesando en tiempo real
   - Interfaz web de Spark (puerto 4040)

2. **Archivos de Resultado:**
   ```bash
   # Copiar resultados para análisis
   cp resultados/* ~/capturas_resultados/
   ```

### Solución de Problemas Comunes

#### Error: "No se puede conectar a Kafka"
```bash
# Verificar que Kafka esté ejecutándose
sudo netstat -tlnp | grep 9092

# Reiniciar Kafka si es necesario
sudo pkill -f kafka
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

#### Error: "Puerto 4040 ocupado"
```bash
# Cambiar puerto de Spark UI
spark-submit --conf spark.ui.port=4041 procesamiento_batch.py
```

#### Error: "Memoria insuficiente"
```bash
# Ajustar memoria de Spark
spark-submit --driver-memory 2g --executor-memory 2g procesamiento_batch.py
```

#### Error: "Topic no existe"
```bash
# Recrear topic
/opt/Kafka/bin/kafka-topics.sh --delete --bootstrap-server localhost:9092 --topic transacciones_ventas
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transacciones_ventas
```

### Comandos de Limpieza

```bash
# Detener servicios
sudo pkill -f kafka
sudo pkill -f zookeeper

# Limpiar logs
sudo rm -rf /tmp/kafka-logs
sudo rm -rf /tmp/zookeeper
```

### Verificación Final

Antes de finalizar, verificar que:

1. ✅ Dataset generado (100,000 transacciones)
2. ✅ Procesamiento batch completado
3. ✅ Kafka ejecutándose
4. ✅ Productor enviando datos
5. ✅ Spark Streaming procesando datos
6. ✅ Interfaz web accesible
7. ✅ Resultados guardados en Parquet
8. ✅ Capturas de pantalla tomadas

### Notas Importantes

- **Orden de Ejecución**: Siempre iniciar Kafka antes que los scripts de streaming
- **Memoria**: La VM tiene recursos limitados, ajustar memoria según sea necesario
- **Red**: Verificar conectividad de red entre Windows y la VM
- **Logs**: Revisar logs de Spark y Kafka para diagnosticar problemas
- **Backup**: Hacer backup de resultados importantes antes de limpiar

---

**Autor**: appsgalvis  
**Curso**: Big Data UNAD  
**Fecha**: Octubre 2025
