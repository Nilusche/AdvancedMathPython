from PIL import Image
from FourierTransform import *

im = Image.open("./image1.png")
width, height = im.size

def write_rgba_to_file():
    with open("./data/r.txt","w") as r_file, \
        open("./data/g.txt","w") as g_file, \
        open("./data/b.txt","w") as b_file:
        for x in range(width):
            for y in range(height):
                r,g,b,a =im.getpixel((x,y))
                r_file.write(str(r) +"\t"+ str(0)+ "\n")
                g_file.write(str(g) +"\t" + str(0)+ "\n")
                b_file.write(str(b) +"\t" + str(0)+ "\n")

def read_single_data_from_file(file):
    vec =[]
    with open(file) as data:
        data.readline()
        for line in data:
            array = line.split()
            vec.append((Complex(float(array[0]), float(array[1]))))
    return vec;

write_rgba_to_file()
vecA = read_single_data_from_file("./data/r.txt")
