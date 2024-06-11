from PIL import Image
import os

def resize_image(input_path, output_path, size=(1200, 630)):
    # Abre a imagem
    image = Image.open(input_path)
    
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(output_path, "JPEG", quality=50)
    output_size = os.path.getsize(output_path)
    
    print(f"Image saved to {output_path}, size: {output_size / 1024:.2f} KB")

def process_images(input_folder, output_folder, size=(1200, 630)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        if os.path.isfile(input_path):
            try:
                resize_image(input_path, output_path, size)
            except Exception as e:
                print(f"Could not process {input_path}: {e}")

# Uso:
input_folder = '/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/SERVIDOR/MyWebsites/websites/arquivonc/static/img/news_images/'
output_folder = '/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/SERVIDOR/MyWebsites/websites/arquivonc/static/img/news_images_low_res/'
process_images(input_folder, output_folder)