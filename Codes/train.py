from torch.utils.data import (DataLoader)
from tqdm.auto import tqdm
from predict import *
from torch.optim import Adam
import torch


torch.cuda.empty_cache()

channel = 3
batch_size = 8

my_transforms = transforms.Compose(
    [  # Compose makes it possible to have many transforms
        transforms.ToPILImage(),
        transforms.Grayscale(num_output_channels=channel),
        transforms.ColorJitter(brightness=(0.8,1.2)),
        transforms.Resize((720, 720)),
        transforms.CenterCrop(640),
        transforms.RandomRotation(degrees=(-10,10)),
        transforms.ToTensor(),
    ]
)

dataset = CustomDataset(
    csv_file=r"C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\train_set/txt.txt",
    root_dir=r"C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\train_set",
    transform=my_transforms,
)

train_set,valid_set, non_used = torch.utils.data.random_split(dataset, [14000, 1000, 951])
#train_set,valid_set, non_used = torch.utils.data.random_split(dataset, [200, 100, 100])
train_loader = DataLoader(dataset=train_set, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(dataset=valid_set, batch_size=batch_size, shuffle=True)

def train():
    #checkpoint = torch.load(r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\eff_b7_new_checkpoint.model')
    model = build_model(pretrained=True, fine_tune=False, num_classes=2)
    #model.load_state_dict(checkpoint)
    model.to(device)
    optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

    loss_function = nn.CrossEntropyLoss()
    num_epochs = 5
    best_accuracy = 0.0
    train_count = 14000
    valid_count = 1000

    for epoch in range(num_epochs):

        # Evaluation and training on training dataset
        model.train()
        train_accuracy = 0.0
        train_loss = 0.0

        for i, (images, labels) in enumerate(tqdm(train_loader)):

            if torch.cuda.is_available():
                images = Variable(images.cuda())
                labels = Variable(labels.cuda())

            optimizer.zero_grad()

            outputs = model(images)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.cpu().data * images.size(0)
            _, prediction = torch.max(outputs.data, 1)

            train_accuracy += int(torch.sum(prediction == labels.data))

        train_accuracy = train_accuracy / train_count
        train_loss = train_loss / train_count

        # Evaluation on validation dataset
        model.eval()

        valid_accuracy = 0.0
        for i, (images, labels) in enumerate(valid_loader):
            if torch.cuda.is_available():
                images = Variable(images.cuda())
                labels = Variable(labels.cuda())

            outputs = model(images)
            _, prediction = torch.max(outputs.data, 1)
            valid_accuracy += int(torch.sum(prediction == labels.data))

        valid_accuracy = valid_accuracy / valid_count

        print('Epoch: ' + str(epoch) + ' Train Loss: ' + str(train_loss) + ' Train Accuracy: ' + str(
            train_accuracy) + ' Valid Accuracy: ' + str(valid_accuracy))

        # Save the best model
        if valid_accuracy > best_accuracy:
            torch.save(model.state_dict(), r'C:\Users\TRUONGLUAT\PycharmProjects\LVTN\Dataset\effb7_checkpoint.model')
            print("Save best state model")
            best_accuracy = valid_accuracy

train()