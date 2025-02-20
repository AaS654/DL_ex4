from torch.utils.data import Dataset
import torch
from pathlib import Path
from skimage.io import imread
from skimage.color import gray2rgb
import numpy as np
import torchvision.transforms as tv
import pandas as pd

train_mean = [0.59685254, 0.59685254, 0.59685254]
train_std = [0.16043035, 0.16043035, 0.16043035]


class ChallengeDataset(Dataset):

    def __init__(self, data: pd.DataFrame, mode: str): # mode ['val', 'train']
        self.data = data
        self.mode = mode


        # Define transformations
        if self.mode == 'train':
            self.transform = tv.Compose([
                tv.ToPILImage(),
                tv.ToTensor(),
                tv.Normalize(mean=train_mean, std=train_std),
                tv.RandomHorizontalFlip(p=0.3),
                tv.RandomVerticalFlip(p=0.3)
            ])
        elif self.mode == 'val':  # Validation transformations
            self.transform = tv.Compose([
                tv.ToPILImage(),
                tv.ToTensor(),
                tv.Normalize(mean=train_mean, std=train_std),
                tv.RandomHorizontalFlip(p=0.3),
                tv.RandomVerticalFlip(p=0.3)
            ])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int):
        row = self.data.iloc[index]
        image_path = row['filename']
        labels = row[['crack', 'inactive']].values.astype(np.float32)

        image = imread(image_path, as_gray=True)
        image = gray2rgb(image)

        if self.transform:
            image = self.transform(image)

        # Convert label to tensor
        labels = torch.tensor(labels, dtype=torch.long)
        # labels = np.array([row['crack'], row['inactive']])
        return image, labels


