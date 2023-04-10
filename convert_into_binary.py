import os
import time
import PIL
import PIL.Image as Image

t1 = time.time()


file_path = "./test_file.mp4"

# convert mp4 into binary -> Black and white image (like qr code)

binary_arr = []

f = open(file_path, "rb")

for byte in f.read():
    bits = bin(byte)[2:]
    binary_arr.append(bits.zfill(8))

print("Time taken to convert into binary: ", time.time() - t1)

def to_img(binary_arr) -> Image:
    pixel_amount = len(binary_arr)
    
    img_width = int(pixel_amount ** 0.5) + 1
    imt_height = int(pixel_amount / img_width) + 1
    
    pixels = []
    
    for byte in binary_arr:
        for bit in byte:
            pixels.append((int(bit), int(bit), int(bit)))
    
    img = Image.new("RGB", (img_width, imt_height))
    
    img.putdata(pixels)
    
    return img

def to_file(img, fila_path) -> None:
    # convert binary image into file
    
    binary_arr = []

to_img(binary_arr).save("test_file.png")