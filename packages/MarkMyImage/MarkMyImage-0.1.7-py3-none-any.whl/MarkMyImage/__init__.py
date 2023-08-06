import os
import argparse
import logging
from PIL import Image, ImageEnhance, ImageFile
import pyheif

ImageFile.LOAD_TRUNCATED_IMAGES = True
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def apply_transparency(watermark, transparency):
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
    watermark.putalpha(alpha)
    return watermark


def open_heic_image(image_path):
    heif_file = pyheif.read(image_path)
    return Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
    )


def add_watermark(input_folder, watermark_path, output_folder, position, transparency, rotation_angle, logo_scale):
    if not os.path.exists(output_folder):
        logging.info(f"Specified output_folder does not exist, it will be created -> {output_folder}.")
        os.makedirs(output_folder)

    try:
        watermark = Image.open(watermark_path).convert("RGBA")
    except FileNotFoundError:
        logging.error(f"Watermark file not found: {watermark_path}")
        return
    except IOError:
        logging.error(f"Unable to open watermark file: {watermark_path}")
        return

    watermark = apply_transparency(watermark, transparency)

    for item in os.listdir(input_folder):

        if not item.endswith((".jpg", ".jpeg", ".png", ".heic")):
            logging.info(f"File {item} is not supported. Only jpg, jpeg, heic and png files allowed")
            continue

        logging.info(f'Processing image: {item}')
        image_path = os.path.join(input_folder, item)
        try:
            if item.lower().endswith(".heic"):
                img = open_heic_image(image_path).convert("RGB")
            else:
                img = Image.open(image_path).convert("RGB")
        except IOError:
            logging.error(f"Unable to open image file: {image_path}")
            continue

        # Adjust logo size in relation to the image size
        ratio = min(img.width, img.height) * logo_scale / max(watermark.width, watermark.height)
        new_size = (int(watermark.width * ratio), int(watermark.height * ratio))
        resized_watermark = watermark.resize(new_size, Image.ANTIALIAS)

        # Rotate the logo
        rotated_watermark = resized_watermark.rotate(rotation_angle, expand=True, resample=Image.BICUBIC)

        x, y = position
        if x == 0 and y == 0:
            x = (img.width - rotated_watermark.width) // 2
            y = (img.height - rotated_watermark.height) // 2
        img.paste(rotated_watermark, (x, y, x + rotated_watermark.width, y + rotated_watermark.height),
                  rotated_watermark)
        img.save(os.path.join(output_folder, item))
        logging.info(f'Saved watermarked image to: {os.path.join(output_folder, item)}')


def main():
    parser = argparse.ArgumentParser(description="Add a watermark to all images in a folder.")
    parser.add_argument("input_folder", help="Path to the input image folder.")
    parser.add_argument("watermark_path", help="Path to the watermark logo image.")
    parser.add_argument("output_folder", help="Path to the output image folder.")
    parser.add_argument("-p", "--position", nargs=2, type=int, default=[0, 0],
                        help="Coordinates (x, y) of the logo's center. Default: 0 0")
    parser.add_argument("-t", "--transparency", type=float, default=1,
                        help="Transparency level of the logo (0-1, 0 is fully transparent, 1 is opaque). Default: 1")
    parser.add_argument("-r", "--rotation_angle", type=float, default=0,
                        help="Rotation angle of the logo (in degrees). Default: 0")
    parser.add_argument("-l", "--logo_scale", type=float, default=1,
                        help="Size of the logo in relation to the image (0-1, where 1 is equal to the size of the image). Default: 1")

    args = parser.parse_args()

    add_watermark(args.input_folder, args.watermark_path, args.output_folder, args.position, args.transparency,
                  args.rotation_angle, args.logo_scale)
