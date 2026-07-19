# =========================================================
# CAPA BRONZE
# Ingesta cruda vía STREAM (Auto Loader) desde el Volume.
# Sin transformación, tablas de tipo STREAMING TABLE.
# =========================================================

from pyspark import pipelines as dp

RUTA_BASE = "/Volumes/proyecto_final/landing/raw_data/ventas_retail_marcopuclla"


@dp.table(
    name="proyecto_final.bronze.clientes_raw",
    comment="Ingesta cruda de clientes"
)
def clientes_raw():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .load(f"{RUTA_BASE}/clientes")
    )


@dp.table(
    name="proyecto_final.bronze.productos_raw",
    comment="Ingesta cruda de productos"
)
def productos_raw():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .load(f"{RUTA_BASE}/productos")
    )


@dp.table(
    name="proyecto_final.bronze.pedidos_raw",
    comment="Ingesta cruda de pedidos"
)
def pedidos_raw():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("multiLine", "true")
        .load(f"{RUTA_BASE}/pedidos")
    )


@dp.table(
    name="proyecto_final.bronze.detalle_pedidos_raw",
    comment="Ingesta cruda de detalle_pedidos"
)
def detalle_pedidos_raw():
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("multiLine", "true")
        .load(f"{RUTA_BASE}/detalle_pedidos")
    )
