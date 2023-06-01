import torch
from PIL import Image
from torchvision import transforms
from torch import nn
import numpy as np
from diplom_utils import MainModel, lab_to_rgb, visualize
from matplotlib import pyplot as plt

from dotenv import load_dotenv
import os
load_dotenv()



MODEL_FILE = os.getenv('MODEL_FILE')

# Load model
model = MainModel()

model.load_state_dict(torch.load(MODEL_FILE, map_location='cpu'), strict=False)
model.eval()

def process_image(image):
    img = Image.open(image)
    img = img.resize((256, 256))
    img = transforms.ToTensor()(img)[:1] * 2. - 1.
    model.eval()
    with torch.no_grad():
        preds = model.generator(img.unsqueeze(0).to('cpu'))
        gen_output = lab_to_rgb(img.unsqueeze(0), preds.cpu())[0]
    img = img[0]
    plt.imshow(np.squeeze(img))
    plt.imshow(gen_output)
    plt.axis('off')

    plt.savefig('orig_after.png')

    return img
