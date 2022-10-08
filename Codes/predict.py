from dataload import *
import torch.nn as nn
from db_task import *
from torchvision.transforms import transforms
from torch.autograd import Variable
import torchvision.models as models
import torch
import numpy as np
import pydicom
from PIL import Image

torch.cuda.empty_cache()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

channel = 3
my_test_transforms = transforms.Compose(
    [  # Compose makes it possible to have many transforms
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=channel),
        transforms.Resize((300, 300)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ]
)

def prediction(img, transformer):
    model = build_model(pretrained=True, fine_tune=True, num_classes=2)
    checkpoint = torch.load(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\eff_b0_finetune.model')
    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()
    img = io.imread(img)
    img = transformer(img)
    img = img.unsqueeze_(0)
    if torch.cuda.is_available():
        img = Variable(img.cuda())

    output = model(img)

    pred = output.cpu().data.numpy().argmax()
    print(pred)
    confi = 100*output.cpu().data.numpy().max()
    return (pred, confi)

#EfficientNet-b7
def build_model(pretrained, fine_tune, num_classes):
    if pretrained:
        print('[INFO]: Loading pre-trained weights')
    else:
        print('[INFO]: Not loading pre-trained weights')
    model = models.efficientnet_b0(pretrained=pretrained)
    if fine_tune:
        print('[INFO]: Fine-tuning all layers...')
        for params in model.parameters():
            params.requires_grad = True
    elif not fine_tune:
        print('[INFO]: Freezing hidden layers...')
        for params in model.parameters():
            params.requires_grad = False

    # Change the final classification head.
    model.classifier = nn.Sequential(
        #nn.Linear(in_features=2560, out_features=1280),
        #nn.ReLU(),
        #nn.Dropout(p=0.2),
        nn.Linear(in_features=1280, out_features=256),
        nn.ReLU(),
        nn.Dropout(p=0.2),
        nn.Linear(in_features=256, out_features=num_classes),
        nn.Softmax(dim=1)
    )

    return model


def read_dicom(img):
    img.seek(0)
    img = pydicom.dcmread(img)
    img = img.pixel_array.astype(float)

    rescaled_img = (np.maximum(img, 0) / img.max()) * 255
    final = np.uint8(rescaled_img)

    final = Image.fromarray(final)
    img_name = 'img_' + str(count_file()) + '.png'
    image_name = 'C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name)
    final.save(image_name)
    return(img_name)

#img_name = read_dicom(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\Dicom\2_covid_574.dcm')
#print(prediction('C:/Users/TRUONGLUAT/PycharmProjects/LVTN/Image/' + str(img_name), my_test_transforms))