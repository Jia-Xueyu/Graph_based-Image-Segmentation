from graph import segmentation_graph
from PIL import Image,ImageFilter
import numpy as np
from random import random



def segmentation_generate(forest,width,height):
    color=lambda : (int(random()*255), int(random()*255), int(random()*255))
    colors=[color() for i in range(width*height)]
    image=Image.new('RGB',(height,width))
    img=image.load()
    for i in range(height):
        for j in range(width):
            temp_parent=forest.find(i*width+j)
            img[i,j]=colors[temp_parent]
    return image.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)



file_path='./assets/seg_test.jpg'
out_path='./assets/output.jpg'
sigma=1.0
const_value=10.0
min_size=200
image_file=Image.open(file_path)
size=image_file.size#(width,height)
filiter_img=image_file.filter(ImageFilter.GaussianBlur(sigma))
filiter_img=np.array(filiter_img).astype(int)
temp_forest=segmentation_graph(filiter_img,size[1],size[0],const_value,min_size)
image=segmentation_generate(temp_forest,size[0],size[1])
image.save(out_path)
print('segmentation nums: {}'.format(temp_forest.num_size))
