import cv2
from pilmoji import Pilmoji #pip3 install pilmoji
from PIL import Image, ImageFont

def extract_first_frame(video_path):
    output_image_path = video_path.split(".")[0] + "_first_frame.jpg"
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(output_image_path, image)

    return output_image_path

def extract_last_frame(video_path):
    output_image_path = "assets_produced/last_thumbnail.jpg"

    vidcap = cv2.VideoCapture(video_path)
    
    # Find the total frame count
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Set the video's current position to the last frame
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
    
    success, image = vidcap.read()
    if success:
        cv2.imwrite(output_image_path, image)
    
    return output_image_path
    
    
def put_emoji_on_img():
    my_string = '😎'
    
    with Image.open("test.jpg") as image:
        
        font = ImageFont.truetype('fonts/arial.ttf', 100)

        with Pilmoji(image) as pilmoji:
            pilmoji.text((int(image.width)- 100, int(image.height) - 200), my_string.strip(), (0, 0, 0), font)

        image.show()