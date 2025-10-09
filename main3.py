from rembg import remove
from PIL import Image
import io


input_path = 'input_image.jpg'       
temp_png_path = 'temp_output.png'    
final_jpg_path = 'final_output.jpg'  


with open(input_path, 'rb') as i:
    input_image = i.read()

output_image = remove(input_image)


with open(temp_png_path, 'wb') as o:
    o.write(output_image)

png_image = Image.open(temp_png_path).convert("RGBA")
bg = Image.new("RGB", png_image.size, (255, 255, 255))  
bg.paste(png_image, mask=png_image.split()[3]) 
bg.save(final_jpg_path, "JPEG")

print(" Final JPG saved with white background:", final_jpg_path)
