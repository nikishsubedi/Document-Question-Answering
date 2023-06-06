from transformers import pipeline
from PIL import Image
import cv2
import random
Image.MAX_IMAGE_PIXELS = 1e10


def answers(question, filepath):
    number = random.randint(1, 1e6)
    pipe = pipeline(model="impira/layoutlm-document-qa")
    images = list()
    for filename in filepath:
        image = cv2.imread(filename)
        images.append(image)
    concatenated_images = cv2.vconcat(images)
    cv2.imwrite(f'created_img/{number}_concat.png', concatenated_images)
    image = Image.open(f'created_img/{number}_concat.png')
    answers = pipe(image, question=question)
    answer = answers[0]['answer']
    return answer

# huggingface models

# layoutLM model: model="impira/layoutlm-document-qa"

# donut model: model = "naver-clova-ix/donut-base-finetuned-docvqa"
