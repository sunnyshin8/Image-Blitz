import os
import cv2
import numpy as np
# import pandas as pd
import tempfile
import io

from Image.gfpgan import GFPGANer

import shutil
import glob
# import matplotlib.pyplot as plt
from basicsr.utils import imwrite

# files = ['img59.jpg']

# original_folder = 'tests/original'
# uploads_folder = 'tests/uploads'
results_folder = 'results'


bg_upsampler = None
arch = 'clean'
channel_multiplier = 2
model_name = 'GFPGANv1.4'
url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth'
model_path = url

restorer = GFPGANer(
    model_path=model_path,
    upscale=2,
    arch=arch,
    channel_multiplier=channel_multiplier,
    bg_upsampler=bg_upsampler)

# !python inference_gfpgan.py -i inputs/upload -o results -v 1.3 -s 2 --bg_upsampler realesrgan

# img_list = sorted(glob.glob(os.path.join(uploads_folder, '*')))

def process_image(file_uuid, ext):
    # print(f'Processing {img.filename} ...')
    input_img = cv2.imread(os.path.join('uploads', file_uuid+"."+ext[1:]), cv2.IMREAD_COLOR)

    cropped_faces, restored_faces, restored_img = restorer.enhance(
        input_img,
        has_aligned=False,
        only_center_face=False,
        paste_back=True,
        weight=0.5)

    if restored_img is not None:
        extension = ext[1:]

        save_restore_path = os.path.join(results_folder, f'{file_uuid}.{extension}')
        imwrite(restored_img, save_restore_path)
    return file_uuid+"."+extension


# os.system('python Image/Image-Blitz.py -i tests/uploads -o tests/results -v 1.3 -s 2 --bg_upsampler realesrgan')