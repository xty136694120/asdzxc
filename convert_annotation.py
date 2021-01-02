import xml.etree.ElementTree as ET
import pickle
import os
from PIL import Image
from os import listdir, getcwd
from os.path import join

classes = ['with_mask', 'without_mask','mask_weared_incorrect'] #对应里面的name，按照实际情况修改
Annotation_path = 'dataset/annotations'
Labels_path = 'dataset/labels'
Image_path = 'dataset/images'
#这个函数是voc自己的不用修改，在下面的函数中调用
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = round(x * dw, 6)
    w = round(w * dw, 6)
    y = round(y * dh, 6)
    h = round(h * dh, 6)
    return (x,y,w,h)

#生成标签函数，从xml文件中提取有用信息写入txt文件
def convert_annotation(image_id):
    in_file = open(Annotation_path +'/%s.xml'%(image_id)) #Annotations文件夹地址
    out_file = open(Labels_path + '/%s.txt'%(image_id), 'w') #labels文件夹地址
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    print(Image_path +'/%s.jpg'%(image_id))
    if size is None:
        img = Image.open(Image_path + '/%s.jpg' % (image_id))
        w = int(img.width)
        h = int(img.height)
    else:
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        if w == 0 or h == 0:
            img = Image.open(Image_path + '/%s.jpg' % (image_id))
            w = int(img.width)
            h = int(img.height)



    for obj in root.iter('object'):
        cls = obj.find('name').text
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if not os.path.exists(Labels_path):#不存在文件夹
    os.makedirs(Labels_path)

image_adds = os.listdir( Image_path )

for image_add in image_adds:
    image_add =  image_add.strip().replace('.png','')
    convert_annotation(image_add)

print("Finished")
