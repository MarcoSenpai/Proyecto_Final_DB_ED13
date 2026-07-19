# Diccionario de Datos — Proyecto Final Ventas Retail

Documenta las 4 entidades fuente del proyecto, ingeridas en la capa **landing** (Volume) y procesadas a través de Bronze → Silver → Gold.

---

## 1. clientes

**Formato de origen:** CSV
**Archivos:** `clientes_batch_1.csv`, `clientes_batch_2.csv`, `clientes_batch_3.csv`
**Grano:** 1 fila por cliente
**Clave primaria:** `customer_id`

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| customer_id | Integer | Identificador único del cliente (PK) | 1001 |
| nombre | String | Nombre del cliente | Rosa |
| apellido | String | Apellido del cliente | Fernandez |
| email | String | Correo electrónico de contacto | rosa.fernandez1001@mail.com |
| ciudad | String | Ciudad de residencia | Lima |
| pais | String | País de residencia | Peru |
| fecha_registro | Date | Fecha de alta del cliente (yyyy-MM-dd) | 2024-01-24 |
| segmento | String | Segmento comercial: Retail o Premium | Premium |

---

## 2. productos

**Formato de origen:** CSV
**Archivos:** `productos_batch_1.csv`, `productos_batch_2.csv`, `productos_batch_3.csv`
**Grano:** 1 fila por producto
**Clave primaria:** `product_id`

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| product_id | Integer | Identificador único del producto (PK) | 2001 |
| nombre_producto | String | Nombre comercial del producto | Laptop Pro 14 |
| categoria | String | Categoría del producto | Tecnologia |
| subcategoria | String | Subcategoría del producto | Computadoras |
| precio_unitario | Decimal | Precio unitario de lista | 2048.78 |
| proveedor | String | Proveedor del producto | TechSupply SA |
| stock_actual | Integer | Unidades disponibles en inventario | 105 |

---

## 3. pedidos

**Formato de origen:** JSON
**Archivos:** `pedidos_batch_1.json`, `pedidos_batch_2.json`, `pedidos_batch_3.json`
**Grano:** 1 fila por pedido (cabecera)
**Clave primaria:** `order_id`
**Relación:** `customer_id` → `clientes.customer_id`

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| order_id | Integer | Identificador único del pedido (PK) | 5001 |
| customer_id | Integer | FK hacia clientes.customer_id | 1013 |
| fecha_pedido | Date | Fecha en la que se realizó el pedido | 2024-01-28 |
| canal_venta | String | Canal por el que se generó el pedido | app_movil |
| estado_pedido | String | Estado: completado, en_proceso, cancelado | completado |
| total_pedido | Decimal | Monto total del pedido | 2943.84 |

---

## 4. detalle_pedidos

**Formato de origen:** JSON
**Archivos:** `detalle_pedidos_batch_1.json`, `detalle_pedidos_batch_2.json`, `detalle_pedidos_batch_3.json`
**Grano:** 1 fila por línea de detalle de pedido (grano de la tabla de hechos `fact_ventas`)
**Clave primaria:** `order_item_id`
**Relaciones:** `order_id` → `pedidos.order_id` · `product_id` → `productos.product_id`

| Campo | Tipo | Descripción | Ejemplo |
|---|---|---|---|
| order_item_id | Integer | Identificador único de la línea (PK) | 9001 |
| order_id | Integer | FK hacia pedidos.order_id | 5010 |
| product_id | Integer | FK hacia productos.product_id | 2013 |
| cantidad | Integer | Unidades compradas de ese producto | 5 |
| precio_unitario | Decimal | Precio unitario aplicado en la venta | 932.99 |
| descuento | Decimal | Porcentaje de descuento aplicado (0 a 1) | 0.0 |

---

## Relaciones entre entidades

```
clientes (1) ────< pedidos (N) ────< detalle_pedidos (N) >──── productos (1)
   customer_id        order_id           order_id, product_id
```

- `pedidos.customer_id → clientes.customer_id`
- `detalle_pedidos.order_id → pedidos.order_id`
- `detalle_pedidos.product_id → productos.product_id`

## Modelo dimensional resultante (capa Gold)

| Rol | Tabla | Grano |
|---|---|---|
| Dimensión | dim_cliente | 1 fila por cliente |
| Dimensión | dim_producto | 1 fila por producto |
| Dimensión | dim_fecha | 1 fila por día |
| Hechos | fact_ventas | 1 fila por línea de detalle de pedido |
