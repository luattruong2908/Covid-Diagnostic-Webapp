from tqdm.auto import tqdm
from predict import *
from torch.utils.data import (
    DataLoader,
)

# from efficientnet_pytorch import EfficientNet
a = 0
my_test_transforms = transforms.Compose(
    [  # Compose makes it possible to have many transforms
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=channel),
        transforms.Resize((300, 300)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ]
)

dataset = CustomDataset(
    csv_file = r"C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\test_set/.txt",
    root_dir = r"C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\test_set",
    transform=my_test_transforms,
)

model = build_model(pretrained=True, fine_tune=True, num_classes=2).to(device)
test_loader = DataLoader(dataset)
checkpoint = torch.load(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\eff_b0_finetune.model')
model.load_state_dict(checkpoint)
model.eval()

test_accuracy = 0.0
test_count = 400

for i, (images, labels) in enumerate(tqdm(test_loader)):
    if torch.cuda.is_available():
        images = Variable(images.cuda())
        labels = Variable(labels.cuda())

    outputs = model(images)
    _, prediction = torch.max(outputs.data, 1)
    test_accuracy += int(torch.sum(prediction == labels.data))
    pred = outputs.cpu().data.numpy().argmax()
    a += int(torch.sum(prediction == labels.data))

test_accuracy = test_accuracy / test_count

print(a)
print('Caculating Test accuracy ............')
print('Test accuracy: ' + str(test_accuracy))