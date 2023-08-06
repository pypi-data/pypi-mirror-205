# Watermark

A simple command-line tool to add a watermark to all images in a folder. This package uses the Python Imaging Library (PIL) to add a watermark (logo) with customizable position, transparency, rotation, and scale.

## Installation

Install the package using pip:

```
pip install MarkMyImage
```


## Usage

After installing the package, you can use the `mmi` command in your terminal or command prompt:

```
mmi input_folder watermark_path output_folder [--position X Y] [--transparency VALUE] [--rotation_angle VALUE] [--logo_scale VALUE]
```


### Arguments

- `input_folder`: Path to the folder containing the input images.
- `watermark_path`: Path to the watermark logo image (PNG format recommended for transparency support).
- `output_folder`: Path to the folder where the watermarked images will be saved.

### Options

- `--position X Y`: Coordinates (X, Y) of the top-left corner of the logo. Default: 0 0
- `--transparency VALUE`: Transparency level of the logo (0-1, 0 is fully transparent, 1 is opaque). Default: 1
- `--rotation_angle VALUE`: Rotation angle of the logo (in degrees). Default: 0
- `--logo_scale VALUE`: Size of the logo in relation to the image (0-1, where 1 is equal to the size of the image). Default: 1

### Example

```
mmi /path/to/input/folder /path/to/watermark/logo.png /path/to/output/folder --position 10 10 --transparency 0.7 --rotation_angle 45 --logo_scale 0.15
```


This will add the watermark logo to all images in the input folder with the specified options and save the watermarked images in the output folder.

## License

MIT License
