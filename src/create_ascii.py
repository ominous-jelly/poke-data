import PIL.Image

#ASCII_CHARS = [" ", "@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
ASCII_CHARS = [" ", "#", "%", "*", ";", "."]   
def resize(image, new_width=80):
    old_width, old_height = image.size
    new_height = (new_width * old_height / old_width) / 2
    return image.resize((int(new_width), int(new_height)))

def to_greyscale(image):
    return image.convert("L")

def pixel_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//50]
    return ascii_str

def main(path):
    try: 
        image = PIL.Image.open("/home/jelly/Development/poke-data/img/" + str(path) + ".png")
    except:
        print(path, "Unable to find image.")

    image = resize(image)
    
    grayscale_image = to_greyscale(image)
    
    ascii_str = pixel_to_ascii(grayscale_image)
    
    img_width = grayscale_image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
        
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_img)
        f.close()