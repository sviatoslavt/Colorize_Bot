import torch
from PIL import Image
from torchvision import transforms
import numpy as np
from diplom_utils import MainModel, lab_to_rgb, build_backbone_unet, Config
from io import BytesIO

from dotenv import load_dotenv
import os
load_dotenv()

MODEL_FILE = os.getenv('MODEL_FILE')

generator = build_backbone_unet(input_channels=1, output_channels=2, size=Config.image_size_1)
# Load model
model = MainModel(generator=generator)

model.load_state_dict(torch.load(MODEL_FILE,map_location=torch.device('cpu')),strict=False)

async def process_image(image):
    img = Image.open(image)
    img = transforms.ToTensor()(img)[:1] * 2. - 1.
    model.eval()
    with torch.no_grad():
        preds = model.generator(img.unsqueeze(0).to('cpu'))
        gen_output = lab_to_rgb(img.unsqueeze(0), preds.cpu())[0]
    buf = BytesIO()
    conv = Image.fromarray(np.uint8(gen_output*255))
    print(type(conv))
    conv.save(buf, format='PNG')
    buf.seek(0)
    return buf
