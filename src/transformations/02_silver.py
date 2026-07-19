# =========================================================
# CAPA SILVER
# Limpieza, tipado y expectations de calidad.
# Tablas de tipo STREAMING TABLE.
#
# Severidades usadas en el proyecto (repartidas a propósito):
#   - expect            -> warn  (registra, no descarta)
#   - expect_or_drop     -> drop  (descarta la fila mala)
#   - expect_or_fail     -> fail  (detiene el pipeline)
# =========================================================

from pyspark import pipelines as dp
from pyspark.sql.functions import col


# ---------------------------------------------------------
# clientes
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.silver.clientes",
    comment="Clientes limpios y validados"
)
@dp.expect_or_drop("customer_id_valido", "customer_id IS NOT NULL")
@dp.expect("email_formato_valido", "email RLIKE '^[^@]+@[^@]+\\\\.[^@]+$'")
@dp.expect_or_drop("segmento_valido", "segmento IN ('Retail', 'Premium')")
def clientes():
    return (
        spark.readStream.table("proyecto_final.bronze.clientes_raw")
        .select(
            col("customer_id").cast("int"),
            col("nombre"),
            col("apellido"),
            col("email"),
            col("ciudad"),
            col("pais"),
            col("fecha_registro").cast("date"),
            col("segmento"),
        )
    )


# ---------------------------------------------------------
# productos
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.silver.productos",
    comment="Productos limpios y validados"
)
@dp.expect_or_fail("product_id_valido", "product_id IS NOT NULL")
@dp.expect_or_drop("precio_unitario_valido", "precio_unitario > 0")
@dp.expect("stock_no_negativo", "stock_actual >= 0")
def productos():
    return (
        spark.readStream.table("proyecto_final.bronze.productos_raw")
        .select(
            col("product_id").cast("int"),
            col("nombre_producto"),
            col("categoria"),
            col("subcategoria"),
            col("precio_unitario").cast("decimal(10,2)"),
            col("proveedor"),
            col("stock_actual").cast("int"),
        )
    )


# ---------------------------------------------------------
# pedidos
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.silver.pedidos",
    comment="Pedidos limpios y validados"
)
@dp.expect_or_drop("order_id_valido", "order_id IS NOT NULL")
@dp.expect("estado_pedido_valido", "estado_pedido IN ('completado', 'en_proceso', 'cancelado')")
@dp.expect_or_drop("total_pedido_no_negativo", "total_pedido >= 0")
def pedidos():
    return (
        spark.readStream.table("proyecto_final.bronze.pedidos_raw")
        .select(
            col("order_id").cast("int"),
            col("customer_id").cast("int"),
            col("fecha_pedido").cast("date"),
            col("canal_venta"),
            col("estado_pedido"),
            col("total_pedido").cast("decimal(10,2)"),
        )
    )


# ---------------------------------------------------------
# detalle_pedidos
# ---------------------------------------------------------
@dp.table(
    name="proyecto_final.silver.detalle_pedidos",
    comment="Detalle de pedidos limpio y validado"
)
@dp.expect_or_drop("order_item_id_valido", "order_item_id IS NOT NULL")
@dp.expect_or_drop("cantidad_valida", "cantidad > 0")
@dp.expect_or_fail("fks_no_nulas", "order_id IS NOT NULL AND product_id IS NOT NULL")
def detalle_pedidos():
    return (
        spark.readStream.table("proyecto_final.bronze.detalle_pedidos_raw")
        .select(
            col("order_item_id").cast("int"),
            col("order_id").cast("int"),
            col("product_id").cast("int"),
            col("cantidad").cast("int"),
            col("precio_unitario").cast("decimal(10,2)"),
            col("descuento").cast("decimal(5,2)"),
        )
    )
