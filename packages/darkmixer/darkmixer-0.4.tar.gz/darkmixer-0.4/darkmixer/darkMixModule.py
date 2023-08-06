import os
from PIL import Image, ImageOps
import random
from shutil import copyfile


class ImageMixer():

    def select_random_images(input_dir, output_dir, num_images):
        """
        Selects a specified number of random images from a directory and saves them to another directory.

        :param input_dir: The path to the input directory containing images.
        :param output_dir: The path to the output directory where the selected images will be saved.
        :param num_images: The number of images to select.
        :return: None
        """
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Get a list of all image files in the input directory
        image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg') or f.endswith('.png')]

        # Select num_images random image files
        selected_files = random.sample(image_files, num_images)

        # Copy the selected image files to the output directory
        for file in selected_files:
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, file)
            copyfile(input_path, output_path)


    def apply_dark_mix(input_folder_path, output_folder_path, brightness_factor=0.5, contrast_factor=0.5):
        """
        Applies a dark theme to input images by adjusting brightness and contrast.

        :param input_folder_path: The path to the folder containing input image files.
        :param output_folder_path: The path to the folder where output image files will be saved.
        :param brightness_factor: The factor by which to adjust the brightness (default is 0.5).
        :param contrast_factor: The factor by which to adjust the contrast (default is 0.5).
        :return: None
        """
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # Load all image files in the input folder
        for filename in os.listdir(input_folder_path):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                input_path = os.path.join(input_folder_path, filename)
                output_path = os.path.join(output_folder_path, filename)

                # Load the input image
                image = Image.open(input_path)

                # Adjust the brightness and contrast
                enhancer = ImageMixer.Brightness(image)
                image = enhancer.enhance(brightness_factor)

                enhancer = ImageMixer.Contrast(image)
                image = enhancer.enhance(contrast_factor)

                # Invert the colors
                image = ImageOps.invert(image)

                # Save the output image
                image.save(output_path)
