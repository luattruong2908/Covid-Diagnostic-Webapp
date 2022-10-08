import torch
from torch.utils.data import (
    Dataset,
)
import pandas as pd
from skimage import io
import os

class CustomDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.annotations = pd.read_csv(csv_file,delim_whitespace=True,header=None)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.annotations.iloc[index, 1])
        images = io.imread(img_path)
        labels = torch.tensor(int(self.annotations.iloc[index, 2]))

        if self.transform:
            images = self.transform(images)

        return (images, labels)