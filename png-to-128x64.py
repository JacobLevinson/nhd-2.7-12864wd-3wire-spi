import os
import sys
from PIL import Image

def process_pixel(pixel_value):
    # Convert 8-bit grayscale (0-255) to 4-bit grayscale (0-15)
    return pixel_value // 16

def convert_image_to_4bit_grayscale(image_path, output_path=None):
    # Open the image
    img = Image.open(image_path)
    
    # Handle transparency by converting to RGBA and applying a white background
    if img.mode == 'P' or img.mode == 'RGBA':
        img = img.convert('RGBA')
        # Create a new image with a white background
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        # Paste the original image on the background, using alpha channel as mask
        img = Image.alpha_composite(background, img)

    # Convert image to grayscale ('L' mode)
    img = img.convert('L')

    # Resize image to 128x64
    img = img.resize((128, 64))

    # Initialize an empty list to hold the converted pixel data
    bitmap_data = []

    # Process the image in pairs of pixels (two 4-bit pixels per byte)
    for y in range(64):  # Ensuring 64 rows
        for x in range(0, 128, 2):  # Step through pixels two at a time
            # Get the first pixel value (0-255 grayscale) and convert it
            pixel_value1 = img.getpixel((x, y))
            first_pixel = process_pixel(pixel_value1)

            # Get the second pixel value (0-255 grayscale) and convert it
            pixel_value2 = img.getpixel((x + 1, y))
            second_pixel = process_pixel(pixel_value2)

            # Combine two 4-bit values into one byte
            combined_byte = (first_pixel << 4) | second_pixel

            # Add the processed byte to the bitmap data
            bitmap_data.append(combined_byte)

    # Ensure the final size is exactly 4096 bytes
    if len(bitmap_data) != 128 * 64 // 2:
        print(f"Error: Expected 4096 bytes, got {len(bitmap_data)} bytes.")
        return

    # If no output path is provided, create a default one
    if output_path is None:
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}-4bit.bin"

    # Save the bitmap data to the output file
    with open(output_path, 'wb') as f:
        f.write(bytearray(bitmap_data))

    print(f"Image successfully converted and saved to {output_path}")

def print_usage():
    usage_text = """
Usage: python script.py <input_image> [output_file]

Arguments:
  <input_image>   Path to the input image file (required).
  [output_file]   Optional. Path to the output binary file. If not provided, the output will be named as the input image with '-4bit.bin' appended.

Options:
  -h, --help      Show this help message and exit.
"""
    print(usage_text)

if __name__ == "__main__":
    # Check for help flag
    if len(sys.argv) == 2 and sys.argv[1] in ("-h", "--help"):
        print_usage()
        sys.exit(0)

    # Check for at least one argument (input file)
    if len(sys.argv) < 2:
        print("Error: Input image is required.")
        print_usage()
        sys.exit(1)

    # Input image path
    input_image = sys.argv[1]

    # Optional output path
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    # Call the conversion function
    convert_image_to_4bit_grayscale(input_image, output_file)
