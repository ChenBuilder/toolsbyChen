from PIL import Image, ImageFile
import os


def convert_and_compress_image(input_path, output_format, output_path, target_size_kb, max_dims):
    with Image.open(input_path) as img:
        # Convert CMYK images to RGB
        if img.mode == 'CMYK':
            img = img.convert('RGB')

        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height
        print(aspect_ratio)

        # Calculate new dimensions that preserve the aspect ratio within the limits
        new_width = min(max_dims[0], img.width)
        new_height = int(new_width / aspect_ratio)
        if new_height > max_dims[1]:
            new_height = max_dims[1]
            new_width = int(new_height * aspect_ratio)
        
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # If converting to GIF, convert the image mode to 'P' (palette-based)
        if output_format == 'GIF':
            img = img.convert('P')
        
        # Iteratively reduce the image quality to achieve the desired file size
        temp_output_path = "temp_output_image.png"
        for _ in range(10):  # try at most 10 times
            img.save(temp_output_path, format=output_format, optimize=True)
            file_size_kb = os.path.getsize(temp_output_path) / 1024
            if file_size_kb <= target_size_kb:
                print(file_size_kb)
                break
            else:
                img = img.quantize(colors=256).convert("RGB")
                
        # Check if file exists and delete it
        if os.path.exists(output_path):
            os.remove(output_path)
            
        os.rename(temp_output_path, output_path)

        # Print for verification
        print(f"Final file size: {file_size_kb:.2f}KB")


def resize_and_fill(input_path, output_path, desired_dims=(320, 132)):
    with Image.open(input_path) as img:
        # Convert the image to RGBA (to ensure the transparency layer is preserved)
        img = img.convert("RGBA")

        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height

        # Calculate new dimensions based on aspect ratio
        new_width = desired_dims[0]
        new_height = int(new_width / aspect_ratio)

        # If calculated height exceeds desired height, then recalculate
        if new_height > desired_dims[1]:
            new_height = desired_dims[1]
            new_width = int(new_height * aspect_ratio)

        # Resize the image
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Create a blank transparent canvas with the desired dimensions
        background = Image.new("RGBA", desired_dims, (255, 255, 255, 0))

        # Calculate the position to paste the resized image onto the canvas
        # (to center it)
        paste_position = ((desired_dims[0] - new_width) // 2, (desired_dims[1] - new_height) // 2)

        # Paste the resized image onto the canvas
        background.paste(img, paste_position, img)

        background.save(output_path, "PNG", optimize=True)



if __name__ == "__main__":
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    filepath = r'PLEASE INPUT YOUR FILEPATH HERE'
    pngpath = r'PLEASR YOUR FILEPATHE HERE(TRANSFERED PATH)'
    resizepath = r'PLEASR YOUR FILEPATHE HERE(RESIZED PATH)'
    outputformat = 'PNG'
    targetsize = 30
    dims_info = (320, 132)
    # convert_and_compress_image(filepath, outputformat, pngpath,target_size_kb=targetsize, max_dims=dims_info)
    resize_and_fill(filepath, resizepath,desired_dims=dims_info)