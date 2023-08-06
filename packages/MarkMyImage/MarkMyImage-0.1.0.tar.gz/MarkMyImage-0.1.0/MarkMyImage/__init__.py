import os
import argparse
from PIL import Image, ImageEnhance

def apply_transparency(watermark, transparency):
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
    watermark.putalpha(alpha)
    return watermark

def add_watermark(input_folder, watermark_path, output_folder, position, transparency, rotation_angle, logo_scale):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    watermark = Image.open(watermark_path).convert("RGBA")
    watermark = apply_transparency(watermark, transparency)

    for item in os.listdir(input_folder):
        if item.endswith(".jpg") or item.endswith(".png"):
            image_path = os.path.join(input_folder, item)
            img = Image.open(image_path).convert("RGB")

            # Adjust logo size in relation to the image size
            ratio = min(img.width, img.height) * logo_scale / max(watermark.width, watermark.height)
            new_size = (int(watermark.width * ratio), int(watermark.height * ratio))
            resized_watermark = watermark.resize(new_size, Image.ANTIALIAS)

            # Rotate the logo
            rotated_watermark = resized_watermark.rotate(rotation_angle, expand=True, resample=Image.BICUBIC)

            x, y = position
            img.paste(rotated_watermark, (x, y, x + rotated_watermark.width, y + rotated_watermark.height), rotated_watermark)
            img.save(os.path.join(output_folder, item))

def main():
    parser = argparse.ArgumentParser(description="Add a watermark to all images in a folder.")
    parser.add_argument("input_folder", help="Path to the input image folder.")
    parser.add_argument("watermark_path", help="Path to the watermark logo image.")
    parser.add_argument("output_folder", help="Path to the output image folder.")
    parser.add_argument("--position", nargs=2, type=int, default=[10, 10], help="Coordinates (x, y) of the top-left corner of the logo. Default: 10 10")
    parser.add_argument("--transparency", type=float, default=0.5, help="Transparency level of the logo (0-1, 0 is fully transparent, 1 is opaque). Default: 0.5")
    parser.add_argument("--rotation_angle", type=float, default=30, help="Rotation angle of the logo (in degrees). Default: 30")
    parser.add_argument("--logo_scale", type=float, default=0.2, help="Size of the logo in relation to the image (0-1, where 1 is equal to the size of the image). Default: 0.2")

    args = parser.parse_args()

    add_watermark(args.input_folder, args.watermark_path, args.output_folder, args.position, args.transparency, args.rotation_angle, args.logo_scale)
