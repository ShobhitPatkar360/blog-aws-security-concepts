from PIL import Image, ImageOps
import os
import sys

def add_border_to_images(folder_name, border_width, border_color):
    """
    Adds a border to all images in a specified folder within the current directory.

    Args:
        folder_name (str): The name of the folder containing the images.
        border_width (int): The width of the border in pixels.
        border_color (tuple or str): The color of the border (e.g., (0, 0, 0) for black, "red").
    """
    image_directory = os.path.join(os.getcwd(), folder_name)  # Construct the full path

    try:
        if not os.path.exists(image_directory):
            raise FileNotFoundError(f"Folder '{folder_name}' not found in the current directory.")

        for filename in os.listdir(image_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(image_directory, filename)
                try:
                    img = Image.open(image_path)
                    bordered_img = ImageOps.expand(img, border=border_width, fill=border_color)
                    bordered_img.save(image_path)  # Overwrite the original image
                    print(f"Border added to {filename}")
                except IOError:
                    print(f"Cannot open or save image: {filename}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <folder_name> <border_width> <border_color>")
        sys.exit(1)

    folder_name = sys.argv[1]
    try:
        border_width = int(sys.argv[2])
    except ValueError:
        print("Error: Border width must be an integer.")
        sys.exit(1)

    border_color = sys.argv[3]

    add_border_to_images(folder_name, border_width, border_color)