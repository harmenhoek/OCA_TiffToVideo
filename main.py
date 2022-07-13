import os
import ffmpeg

'''
Important: install FFmpeg locally with correct enviromental variables! https://www.wikihow.com/Install-FFmpeg-on-Windows
'''

folder_path = r'C:\Users\HOEKHJ\Dev\OCA_TiffToVideo\testimages'

images = [os.path.join(folder_path, img) for img in os.listdir(folder_path) if img.endswith(".tiff") or img.endswith(".png") or img.endswith(".jpg") or img.endswith(".jpeg") or img.endswith(".bmp")]
if not images:
    raise Exception("No images with extension '.tiff', '.png', '.jpg', '.jpeg' or '.bmp' found in selected folder.")

with open('temp.txt', 'w') as f:
    for image in images:
        f.write(f"file '{image}'\n")


try:
    out, _ = (
        ffmpeg
            .input('temp.txt', r='2', f='concat', safe='0')
            .output('movie.avi', pix_fmt='pal8', crf=0, vf='scale=768:-1')
            .run(overwrite_output=True)
    )
except ffmpeg.Error as e:
    print(e.stderr)

os.remove('temp.txt')


# ffmpeg.exe -r 2 -i Basler acA5472-17uc 24263966 20220629 174621896 %04d.tiff -c:v rawvideo -pix fmt pal8 -vf scale=768:-1
# .filter('scale', size='hd1080', force_original_aspect_ratio='increase')
# .output('movie.mp4', crf=20, preset='slower', movflags='faststart', pix_fmt='yuv420p')
# .run()
# pix_fmt='pal8', format='rawvideo',