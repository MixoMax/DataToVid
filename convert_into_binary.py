import os
import time
import PIL
import PIL.Image as Image
import math

t1 = time.time()


def to_binary(file_path):
    binary_string = ""
    with open(file_path, "r", encoding="Latin-1") as f:
        for line in f:
            for char in line:
                binary_string += bin(ord(char))[2:].zfill(8)
    return binary_string

def to_image(binary_string, img_path = "my.png"):
    width = 1920*6
    height = 1080*6
    
    if len(binary_string) > width * (height - 1):
        print("File too large")
        return None
    
    img = Image.new("RGB", (width, height), color = "white")
    pixels = img.load()
    
    length_in_binary = bin(len(binary_string))[2:].zfill(32)
    
    for i in range(32):
        if length_in_binary[i] == "1":
            pixels[i, 0] = (0, 0, 0)
    
    for i in range(len(binary_string)):
        if binary_string[i] == "1":
            pixels[i % width, i // width + 1] = (0, 0, 0)
            
    
    
    image_directory = os.path.dirname(img_path)
    if os.path.exists(image_directory) == False:
        os.makedirs(image_directory)
    img.save(img_path)

def to_file(image_path, file_path = "my", file_type = "txt"):
    binary_string = ""
    img = Image.open(image_path)
    
    pixels = img.load()
    
    length_in_binary = ["1" if pixels[i, 0] == (0, 0, 0) else "0" for i in range(32)]
    
    length = int("".join(length_in_binary), 2)
    
    width, height = img.size
    
    for i in range(length): 
        pixel_idx = i
        
        binary_string += "1" if pixels[pixel_idx % width, pixel_idx // width + 1] == (0, 0, 0) else "0"
                
    
    f = open(file_path + "." + file_type, "w", encoding="Latin-1")
    
    for i in range(0, len(binary_string), 8):
        f.write(chr(int(binary_string[i:i+8], 2)))
    
    return binary_string


def main():
    
    input_file = "./Data/Input/Dalle.png"
    
    output_image = "/Data/Output/my.png"
    
    output_file = ("./Data/Output/Final/Dalle", "png")
    
    #remove the output file and image if they exist
    
    if os.path.exists(output_image):
        os.remove(output_image)
    if os.path.exists(output_file[0] + "." + output_file[1]):
        os.remove(output_file[0] + "." + output_file[1])
    
    t1 = time.time()

    binary_string = to_binary(input_file)

    t2 = time.time()
    time_taken = t2 - t1

    speed = (len(binary_string) / time_taken)//1000

    print("1/3", time_taken, speed, "kb/s")

    to_image(binary_string, output_image)

    t3 = time.time()
    time_taken = t3 - t2

    print("2/3", time_taken)

    to_file(output_image, *output_file)

    time_taken = time.time() - t3

    print("3/3", time_taken)

if __name__ == "__main__":
    main()