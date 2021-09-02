from PIL import Image
import os
# this handler is used to crop the image which users provide to thumbnail size and overwrites the same image

basedir = os.path.abspath('project\static')
size = 320, 320

def crop_image(file_path):
    with Image.open(file_path) as im:
        if im.mode != 'RGB':
            im = im.convert('RGB')
        im.thumbnail(size)
        # print(os.path.join(basedir, file_path.split('.')[0]+'.jpg'))
        im.save(os.path.join(basedir, file_path.split('.')[0]+'.jpg'),'JPEG')