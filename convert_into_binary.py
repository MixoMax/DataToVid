import os
import time
import PIL
import PIL.Image as Image
import math

t1 = time.time()


def to_binary(file_path):
    binary_string = ""
    with open(file_path, "r", encoding="latin-1") as f:
        for line in f:
            for char in line:
                binary_string += bin(ord(char))[2:].zfill(8)
    return binary_string

def to_image(binary_string, img_path = "my.png"):
    width = int(math.sqrt(len(binary_string)) + 1)
    height = int(math.sqrt(len(binary_string)) + 1)
    img = Image.new('RGB', (width, height), color = 'white')
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if i * height + j < len(binary_string) and binary_string[i*height + j] == "1":
                pixels[i,j] = (0, 0, 0)
    img.save(img_path)

def to_file(image_path, file_path = "my", file_type = "txt"):
    binary_string = ""
    img = Image.open(image_path)
    
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if img.getpixel((i,j)) == (0, 0, 0):
                binary_string += "1"
            else:
                binary_string += "0"
                
    
    f = open(file_path + "." + file_type, "w")
    
    for i in range(0, len(binary_string), 8):
        f.write(chr(int(binary_string[i:i+8], 2)))
    
    return binary_string

t1 = time.time()

binary_string = to_binary("./test_file.mp4")

t2 = time.time()
time_taken = t2 - t1

speed = (len(binary_string) / time_taken)//1000

print("1/3", time_taken, speed, "kb/s")

to_image(binary_string, "my.png")

t3 = time.time()
time_taken = t3 - t2

print("2/3", time_taken)

to_file("my.png", "my", "mp4")

time_taken = time.time() - t3

print("3/3", time_taken)