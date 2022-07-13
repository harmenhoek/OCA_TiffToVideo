import os
import ffmpeg
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

'''
This program converts a bunch of images into a video format that can be imported on the Dataphysics OCA 15plus.

Input: folder with images (tiff, png, jpg, jpeg, bmp)
Output: video file (height:768, format:pal8, codec:rawvideo)

NOTE To run this code:
1. install FFmpeg locally with correct enviromental variables! https://www.wikihow.com/Install-FFmpeg-on-Windows
2. install requirements (ffmpeg-python, tk)

Special thanks to Harro Beens for figuring out the correct format, codec and scaling.

July 2022 - Physics of Complex Fluids
'''

#  python -m PyInstaller -F main.py -n OCA_TiffToVideo

print('----- Image to video converter for Dataphysics OCA 15plus -----')
print('Special thanks to Harro Beens for figuring out the correct format, codec and scaling.\n')
print('Select folder with images ...')

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()
now = datetime.now()

filenameExport = f"{os.path.basename(os.path.normpath(folder_path))}_PROC{now.strftime('%Y-%m-%d-%H-%M-%S')}.avi"

images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(".tiff") or img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".bmp")]
if not images:
    raise Exception("No images with extension '.tiff', '.png', '.jpg', '.jpeg' or '.bmp' found in selected folder.")

with open('temp.txt', 'w') as f:
    for image in images:
        f.write(f"file '{image}'\n")


try:
    out, _ = (
        ffmpeg
            .input('temp.txt', r='1', f='concat', safe='0')
            .output(filenameExport, pix_fmt='pal8', vf='scale=768:-1', vcodec='rawvideo')
            .run(overwrite_output=True)
    )
except ffmpeg.Error as e:
    print(e.stderr)
    print('Do you have ffmpeg installed on your computer? https://www.wikihow.com/Install-FFmpeg-on-Windows')

os.remove('temp.txt')
print(f'Video {filenameExport} created successfully!')
print('Note: VLC does not play rawvideo.')