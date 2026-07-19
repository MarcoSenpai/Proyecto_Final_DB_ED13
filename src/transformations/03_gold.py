# =========================================================
# CAPA GOLD
# Modelo dimensional en estrella.
# Tablas de tipo MATERIALIZED VIEW (lectura batch, no stream).
#
#              dim_cliente
#                   |
# dim_producto — fact_ventas — dim_fecha
# =========================================================

from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col, year, month, dayofmonth, quarter, date_format, date_format as dfmt
)


# ---------------------------------------------------------
# dim_cliente
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.gold.dim_cliente",
    comment="Dimensión de clientes"
)
def dim_cliente():
    return (
        spark.read.table("proyecto_final.silver.clientes")
        .withColumnRenamed("customer_id", "customer_key")
        .select(
            "customer_key",
            "nombre",
            "apellido",
            "email",
            "ciudad",
            "pais",
            "fecha_registro",
            "segmento",
        )
    )


# ---------------------------------------------------------
# dim_producto
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.gold.dim_producto",
    comment="Dimensión de productos"
)
def dim_producto():
    return (
        spark.read.table("proyecto_final.silver.productos")
        .withColumnRenamed("product_id", "product_key")
        .select(
            "product_key",
            "nombre_producto",
            "categoria",
            "subcategoria",
            "precio_unitario",
            "proveedor",
            "stock_actual",
        )
    )


# ---------------------------------------------------------
# dim_fecha
# Construida a partir de las fechas distintas de pedidos
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.gold.dim_fecha",
    comment="Dimensión de fecha, una fila por día"
)
def dim_fecha():
    fechas = (
        spark.read.table("proyecto_final.silver.pedidos")
        .select("fecha_pedido")
        .distinct()
        .withColumnRenamed("fecha_pedido", "fecha")
    )
    return (
        fechas
        .withColumn("date_key", date_format(col("fecha"), "yyyyMMdd").cast("int"))
        .withColumn("anio", year(col("fecha")))
        .withColumn("mes", month(col("fecha")))
        .withColumn("dia", dayofmonth(col("fecha")))
        .withColumn("trimestre", quarter(col("fecha")))
        .withColumn("nombre_mes", dfmt(col("fecha"), "MMMM"))
        .withColumn("dia_semana", dfmt(col("fecha"), "EEEE"))
        .select("date_key", "fecha", "anio", "mes", "dia", "trimestre", "nombre_mes", "dia_semana")
    )


# ---------------------------------------------------------
# fact_ventas
# Grano: 1 fila por línea de detalle de pedido.
# Junta detalle_pedidos + pedidos (para llegar a customer_id
# y fecha_pedido) para armar las llaves foráneas del fact.
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.gold.fact_ventas",
    comment="Tabla de hechos de ventas"
)
@dp.expect_or_drop("monto_total_no_negativo", "monto_total >= 0")
@dp.expect("cantidad_positiva", "cantidad > 0")
@dp.expect_or_fail("fks_completas", "customer_key IS NOT NULL AND product_key IS NOT NULL AND date_key IS NOT NULL")
def fact_ventas():
    detalle = spark.read.table("proyecto_final.silver.detalle_pedidos")
    pedidos = spark.read.table("proyecto_final.silver.pedidos")

    return (
        detalle
        .join(pedidos, on="order_id", how="left")
        .withColumn("date_key", date_format(col("fecha_pedido"), "yyyyMMdd").cast("int"))
        .withColumnRenamed("customer_id", "customer_key")
        .withColumnRenamed("product_id", "product_key")
        .withColumn(
            "monto_total",
            col("cantidad") * col("precio_unitario") * (1 - col("descuento"))
        )
        .select(
            "order_item_id",
            "customer_key",
            "product_key",
            "date_key",
            "cantidad",
            "precio_unitario",
            "descuento",
            "monto_total",
        )
    )
