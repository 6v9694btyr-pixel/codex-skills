---
name: tiktok-mx-product-listing-generator
description: Use when creating Mexico TikTok Shop product listings from product photos for keychains, bracelets, bangles, or small fashion accessories, especially when filling TikTok Seller Center Excel templates, generating Spanish titles/descriptions, image plans, image prompts, image files, image URL placeholders, or upload manifests.
---

# TikTok MX Product Listing Generator

## Overview

Create a Mexico TikTok Shop listing package from a product image and the Seller Center Excel template. Keep consumer-facing copy in natural Mexican Spanish, keep explanations to the seller in Chinese, and preserve the original workbook structure.

## Required Inputs

- Product main image or real product photo.
- TikTok Seller Center template workbook. Default to the bundled asset `assets/Tiktoksellercenter_Fashion Accessories_20260514_Bracelets & Bangles,Keychains_template.xlsx`; if the user provides a newer template, use that newer file instead.
- Optional image upload interface, object storage interface, or public image URLs. If none is provided, use local files plus upload placeholders.
- Optional GTIN, product size, package details, material, or upload naming preferences.
- Optional retail price, stock quantity, seller SKU, delivery option, and package weight/dimensions. Default future product values for this seller are price `178`, quantity `100`, package weight `100` g, and package dimensions `16 x 13 x 5` cm unless the user supplies different values.

## Workflow

1. Analyze the image first. Identify product type, conservative material guess, color, target audience, use scenes, core selling points, TikTok viral angles, and category.
2. Draft the Mexico Spanish title, listing description, and 9-image plan. Show this to the user in Chinese and wait for confirmation.
3. If the user explicitly asks to skip confirmation and generate directly, skip confirmation and complete all steps.
4. Generate 9 image files when image generation/editing is available. Use the original product image as reference and preserve product color, shape, pattern, material, and structure.
5. If image generation is not available, output 9 directly usable image-generation prompts instead, and explain that image generation must be completed before upload.
6. Upload images only when the user provides a usable upload interface or public URLs. Otherwise create local image placeholders and `image_upload_manifest.csv`.
7. Prepare a structured `listing_payload.json`, then run `scripts/prepare_listing_outputs.py` to fill the workbook and create `listing_summary.md`.
8. Verify quality checks before final delivery.

## Category Rules

Allowed categories only:

- `Costume Jewelry & Accessories/Bracelets & Bangles`
- `Costume Jewelry & Accessories/Keychains`
- `Eyewear/Sunglasses` when the supplied template includes sunglasses and the product is clearly eyewear.

Choose `Costume Jewelry & Accessories/Keychains` when the product is clearly a keychain, bag charm, backpack charm, car-key charm, or has a ring/clip for keys.

Choose `Costume Jewelry & Accessories/Bracelets & Bangles` when the product is clearly a bracelet, bangle, wrist accessory, friendship bracelet, charm bracelet, or wearable wrist jewelry.

Choose `Eyewear/Sunglasses` when the product is clearly sunglasses, photochromic glasses, tinted fashion glasses, or eyewear.

Always set brand to `No brand`. Never invent a brand, authorization, certification, official status, or guaranteed performance claim.

## Listing Copy Rules

Generate one title in Mexican Spanish:

- Maximum 300 characters.
- Natural, local, and simple; avoid machine-translation phrasing.
- Recommended structure: product core term + main selling point + use scene/audience + gift angle.
- No medical, therapeutic, permanent, guaranteed, official, certified, or exaggerated claims.

Generate one product description in Spanish using the exact mobile listing structure in `references/listing_rules.md`.

Use 3-5 real selling points. If a fact is uncertain, use conservative wording such as "apariencia", "estilo", "tipo", or "acabado" instead of hard material/performance claims.

## Image Set

Create or prompt for 9 square ecommerce images, minimum 1600 x 1600 px, JPG or PNG. Keep the real product appearance consistent with the source image.

| Slot | Filename | Purpose |
|---|---|---|
| main_image | `main_image.png` | White or light-gray main image, product centered, clean, no exaggerated text |
| image_2 | `image_2.png` | Lifestyle scene: keychain on keys/bag/backpack/car key, or bracelet on wrist/outfit |
| image_3 | `image_3.png` | Detail close-up: material, clasp, texture, finish, color |
| image_4 | `image_4.png` | Size-feel image with hand, bag, keys, or ruler-style reference; avoid exact dimensions unless provided |
| image_5 | `image_5.png` | Selling point 1: lightweight, cute, easy to match, refined, or durable, with short Spanish text if useful |
| image_6 | `image_6.png` | Multi-scene use: mochila, bolso, llaves, auto, regalo |
| image_7 | `image_7.png` | Gift scene for birthdays, friends, couples, or small everyday gifts |
| image_8 | `image_8.png` | Simple product and packaging/set layout; do not invent luxury packaging |
| image_9 | `image_9.png` | TikTok-style conversion mood image with short Spanish text such as "Un detalle bonito para todos los dias" |

If generating prompts instead of images, output Chinese explanation plus English prompt for each slot. Each prompt must explicitly say to keep the product appearance identical to the source photo and not alter color, shape, material, pattern, or structure.

## Excel Output

Use `scripts/prepare_listing_outputs.py` after the user confirms copy and images/prompts. The script fills only the `Template` worksheet, preserves hidden sheets, formatting, validation, and workbook structure, and writes to the first allowed data row after the header, usually row 7 when row 6 is a sample row. Use the bundled template asset unless the user explicitly supplies another TikTok Seller Center workbook.

Expected outputs:

- `completed_tiktok_listing.xlsx`
- `listing_summary.md`
- `image_upload_manifest.csv` when no upload interface or full image URLs are available
- `images/` with generated images when image generation was completed

Create `listing_payload.json` using the schema in `references/payload_schema.md`. For detailed field and quality rules, read `references/listing_rules.md`.

Run:

```bash
python scripts/prepare_listing_outputs.py --template "<template.xlsx>" --payload "<listing_payload.json>" --output-dir "<output-folder>"
```

Bundled template path:

```text
assets/Tiktoksellercenter_Fashion Accessories_20260514_Bracelets & Bangles,Keychains_template.xlsx
```

Bundled sunglasses-capable template path:

```text
assets/Tiktoksellercenter_Fashion Accessories_20260514_Bracelets & Bangles,Sunglasses,Keychains_template.xlsx
```

The script requires `openpyxl`. In Codex Desktop, call `load_workspace_dependencies` when the default Python cannot import spreadsheet libraries, then run the script with the bundled Python executable.

## Image URL Handling

Mode A, upload interface or public URLs available:

- Upload all 9 images.
- Put public accessible URLs in `image_urls`.
- Fill Excel image fields with URLs.
- Do not generate `image_upload_manifest.csv` unless some URLs are missing.

Mode B, no upload interface:

- Store local images in `images/` if generated.
- Fill Excel image fields with placeholders such as `PLEASE_UPLOAD_main_image.png`.
- Generate `image_upload_manifest.csv` with `image_slot`, `local_file_name`, `recommended_upload_name`, and `purpose`.
- Tell the user to upload images to TikTok Media Center or a public image host and replace placeholders with URLs before TikTok upload.

## Quality Gate

Before final delivery, confirm:

- `product_name` is not empty and is under 300 characters.
- `product_description` is not empty and is Spanish.
- `category` is one of the two allowed categories.
- `brand` is exactly `No brand`.
- `main_image` is filled.
- At least 5 image fields are filled.
- Risky exaggerated or unverifiable claims are absent.
- The workbook remains `.xlsx` and based on the original template.
- The `Template` worksheet still exists and hidden sheets were not deleted.

## Common Mistakes

- Do not classify keychains as bracelets or bracelets as keychains.
- Do not invent exact dimensions, luxury packaging, brand, certification, or material.
- Do not use English in title, description, or image text.
- Do not rebuild the workbook from scratch.
- Do not fill image fields with local file paths unless the template explicitly accepts them; use URLs or placeholders.
