# Listing Rules

## Field Mapping

Fill the `Template` worksheet from row 6 or the first allowed product data row after the detected header row.

| Template field | Value |
|---|---|
| category | Selected allowed category |
| brand | `No brand` |
| product_name | Spanish title |
| product_description | Spanish listing description |
| main_image | Public URL or `PLEASE_UPLOAD_main_image.png` |
| image_2 to image_9 | Public URL or matching `PLEASE_UPLOAD_*.png` placeholder |
| gtin_type | Empty unless supplied or required |
| gtin_code | Empty unless supplied |
| property_name_1 | `Material` for keychains; `Material` or `Occasion` for bracelets |
| property_value_1 | Conservative template-compatible material value |
| property_1_image | Main image URL if a variant image exists; otherwise empty |
| property_name_2 | Empty unless needed |
| property_value_2 | Empty unless needed |
| parcel_weight | Fill if the seller provides package weight or if the template requires it |
| parcel_length | Fill if the seller provides package length or if the template requires it |
| parcel_width | Fill if the seller provides package width or if the template requires it |
| parcel_height | Fill if the seller provides package height or if the template requires it |
| delivery | Fill if the seller provides delivery option |
| price | Fill if the seller provides retail price |
| quantity | Fill if the seller provides stock quantity |
| seller_sku | Fill if supplied; otherwise leave blank |

For templates with a sample row, do not overwrite the example. Use the first row covered by the template's data validation, usually row 7.

Default commerce fields for this seller's future products:

- `price`: `178`
- `quantity`: `100`
- `parcel_weight`: `100` g
- `parcel_length`: `16` cm
- `parcel_width`: `13` cm
- `parcel_height`: `5` cm

Use these defaults unless the seller supplies different values for a specific product.

## Material Values

Keychain material values:

- `Fabric`
- `Plastic`
- `Metal Coating`

Bracelet and bangle material values:

- `Fabric`
- `Plastic`
- `Metal Coating`
- `Wood`
- `Leather`

If material is unclear, use `Plastic`. If the image shows mixed materials, choose the dominant visible material, but avoid claiming material details in Spanish copy unless they are clear.

Sunglasses category:

- Category: `Eyewear/Sunglasses`
- Preferred primary variation: `Color`
- Common values for the current product family: `Dorado`, `Plateado`
- Use `Metal Coating` only when a material field is required; otherwise keep color as the SKU variation.

## Risk Words And Claims

Avoid:

- Medical or therapeutic wording: curar, tratamiento, alivia dolor, salud, terapia.
- Absolute guarantees: 100%, garantizado, para siempre, permanente, irrompible.
- Unverifiable commercial claims: oficial, original, autorizado, certificado, premium certificado, el mejor, numero 1.
- Overclaiming durability: indestructible, nunca se rompe, resistente a todo.

Acceptable safer wording:

- `diseño práctico`
- `acabado tipo metálico`
- `ligero para uso diario`
- `fácil de combinar`
- `detalle bonito para regalar`

## Spanish Style

Write for Mexican TikTok Shop buyers:

- Use direct mobile-friendly sentences.
- Prefer `mochila`, `bolso`, `llaves`, `auto`, `regalo`, `uso diario`, `amigas`, `pareja`, `cumpleaños`.
- Avoid English and stiff literal translation.
- Keep tone warm but not exaggerated.

## Confirmation Flow

Default flow:

1. 用户上传产品主图。
2. 先用中文输出产品类型、目标人群、使用场景、核心卖点、推荐类目、标题草稿、listing 草稿、9 张主图规划。
3. 等用户确认后，再生成图片或图片提示词。
4. 图片确认后，再填写 Excel。
5. 最后输出 `completed_tiktok_listing.xlsx`。

If the user clearly says "无需确认，直接生成", skip the staged confirmations and complete the full workflow.

## Required Description Structure

Use exactly this structure for `product_description`:

```text
✨ Descripción del producto
[Presenta brevemente qué es el producto y en qué situaciones se usa.]

✅ Características principales
1. [Beneficio real 1]
2. [Beneficio real 2]
3. [Beneficio real 3]
4. [Beneficio real 4]
5. [Beneficio real 5]

🎁 Ideal para
[Explica si sirve para regalo, uso personal, decorar bolsa/mochila/llaves, outfit diario, etc.]

📦 Contenido del paquete
[Indica de forma conservadora qué incluye el paquete.]

⚠️ Nota
El color puede variar ligeramente por la pantalla y la luz de la foto. Las medidas pueden tener una pequeña diferencia por medición manual.
```

## Output Folder Convention

Use an output folder per product, for example:

```text
product_listing_output/
  completed_tiktok_listing.xlsx
  listing_summary.md
  image_upload_manifest.csv
  listing_payload.json
  images/
    main_image.png
    image_2.png
    ...
    image_9.png
```
