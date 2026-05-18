# Payload Schema

Create `listing_payload.json` before running `scripts/prepare_listing_outputs.py`.

```json
{
  "analysis": {
    "product_type": "keychain",
    "material": "Plastic",
    "colors": ["pink", "white"],
    "target_audience": "young women, students, gift buyers",
    "use_scenes": ["keys", "backpack", "bag"],
    "selling_points": ["cute design", "lightweight", "easy to match"],
    "viral_angles": ["small gift", "bag decoration"]
  },
  "category": "Costume Jewelry & Accessories/Keychains",
  "brand": "No brand",
  "product_name": "Llavero Decorativo con Diseño Cute para Mochila, Bolsa o Llaves, Accesorio Ligero para Regalo",
  "product_description": "✨ Descripción del producto\n...\n⚠️ Nota\nEl color puede variar ligeramente por la pantalla y la luz de la foto. Las medidas pueden tener una pequeña diferencia por medición manual.",
  "gtin_type": "",
  "gtin_code": "",
  "property_name_1": "Material",
  "property_value_1": "Plastic",
  "property_1_image": "",
  "property_name_2": "",
  "property_value_2": "",
  "parcel_weight": "100",
  "parcel_length": "16",
  "parcel_width": "13",
  "parcel_height": "5",
  "delivery": "",
  "price": "178",
  "quantity": "100",
  "seller_sku": "",
  "image_urls": {
    "main_image": "",
    "image_2": "",
    "image_3": "",
    "image_4": "",
    "image_5": "",
    "image_6": "",
    "image_7": "",
    "image_8": "",
    "image_9": ""
  },
  "image_files": {
    "main_image": "images/main_image.png",
    "image_2": "images/image_2.png",
    "image_3": "images/image_3.png",
    "image_4": "images/image_4.png",
    "image_5": "images/image_5.png",
    "image_6": "images/image_6.png",
    "image_7": "images/image_7.png",
    "image_8": "images/image_8.png",
    "image_9": "images/image_9.png"
  },
  "image_plan": [
    {
      "slot": "main_image",
      "purpose": "White background main image",
      "cn": "白底主图，产品居中，画面干净。"
    }
  ],
  "image_prompts": [
    {
      "slot": "main_image",
      "cn": "白底主图提示词。",
      "prompt_en": "Create a 1:1 TikTok Shop Mexico ecommerce main image based on the source product photo. Keep the product appearance identical: do not change color, shape, material, pattern, size impression, or structure. Place the product centered on a clean white or very light gray background, bright soft studio lighting, sharp product details, no clutter, no exaggerated text, 1600x1600 px."
    }
  ],
  "variants": [
    {
      "property_name_1": "Color",
      "property_value_1": "Dorado",
      "property_1_image": "PLEASE_UPLOAD_main_image.png",
      "price": "",
      "quantity": "",
      "seller_sku": ""
    },
    {
      "property_name_1": "Color",
      "property_value_1": "Plateado",
      "property_1_image": "PLEASE_UPLOAD_image_2.png",
      "price": "",
      "quantity": "",
      "seller_sku": ""
    }
  ]
}
```

`image_urls` wins over placeholders. If all image URLs are empty or missing, the script fills image fields with `PLEASE_UPLOAD_*.png` placeholders and writes `image_upload_manifest.csv`.

The script accepts extra fields, but it only writes recognized TikTok template fields.

Use `variants` when one listing has multiple SKU options such as sunglasses in `Dorado` and `Plateado`. Each variant becomes one Excel row with shared product information and variant-specific color, image, price, quantity, and SKU fields.
