import cv2
from pilmoji import Pilmoji #pip3 install pilmoji
from PIL import Image, ImageFont

def extract_first_frame(video_path, output_image_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(output_image_path, image)


def put_emoji_on_img():
    my_string = '😎'
    
    with Image.open("test.jpg") as image:
        
        font = ImageFont.truetype('fonts/arial.ttf', 100)

        with Pilmoji(image) as pilmoji:
            pilmoji.text((int(image.width)- 100, int(image.height) - 200), my_string.strip(), (0, 0, 0), font)

        image.show()