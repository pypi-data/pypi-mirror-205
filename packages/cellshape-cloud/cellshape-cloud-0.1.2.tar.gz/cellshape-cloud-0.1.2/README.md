[![Python Version](https://img.shields.io/pypi/pyversions/cellshape-cloud.svg)](https://pypi.org/project/cellshape-cloud)
[![PyPI](https://img.shields.io/pypi/v/cellshape-cloud.svg)](https://pypi.org/project/cellshape-cloud)
[![Downloads](https://pepy.tech/badge/cellshape-cloud)](https://pepy.tech/project/cellshape-cloud)
[![Wheel](https://img.shields.io/pypi/wheel/cellshape-cloud.svg)](https://pypi.org/project/cellshape-cloud)
[![Development Status](https://img.shields.io/pypi/status/cellshape-cloud.svg)](https://github.com/Sentinal4D/cellshape-cloud)
[![Tests](https://img.shields.io/github/workflow/status/Sentinal4D/cellshape-cloud/tests)](
    https://github.com/Sentinal4D/cellshape-cloud/actions)
[![Coverage Status](https://coveralls.io/repos/github/Sentinal4D/cellshape-cloud/badge.svg?branch=master)](https://coveralls.io/github/Sentinal4D/cellshape-cloud?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="https://github.com/DeVriesMatt/cellshape-cloud/blob/main/img/cellshape_cloud.png" 
     alt="Cellshape logo by Matt De Vries">
___
Cellshape-cloud is an easy-to-use tool to analyse the shapes of cells using deep learning and, in particular, graph-neural networks. The tool provides the ability to train popular graph-based autoencoders on point cloud data of 2D and 3D single cell masks as well as providing pre-trained networks for inference.



## To install
```bash
pip install cellshape-cloud
```

## Usage
### Basic Usage
```python
import torch
from cellshape_cloud import CloudAutoEncoder

model = CloudAutoEncoder(num_features=128, 
                         k=20,
                         encoder_type="dgcnn",
                         decoder_type="foldingnet")

points = torch.randn(1, 2048, 3)

recon, features = model(points)
```

### To train an autoencoder on a set of point clouds created using cellshape-helper:
```python
import torch
from torch.utils.data import DataLoader

import cellshape_cloud as cloud
from cellshape_cloud.vendor.chamfer_distance import ChamferLoss


input_dir = "path/to/pointcloud/files/"
batch_size = 16
learning_rate = 0.0001
num_epochs = 1
output_dir = "path/to/save/output/"

model = cloud.CloudAutoEncoder(num_features=128, 
                         k=20,
                         encoder_type="dgcnn",
                         decoder_type="foldingnet")

dataset = cloud.PointCloudDataset(input_dir)

dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

criterion = ChamferLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=learning_rate * 16 / batch_size,
    betas=(0.9, 0.999),
    weight_decay=1e-6,
)

cloud.train(model, dataloader, num_epochs, criterion, optimizer, output_dir)
```


## Parameters

- `num_features`: int.  
The size of the latent space of the autoencoder. 
- `k`: int.  
The number of neightbours to use in the k-nearest-neighbours graph construction.
- `encoder_type`: str.  
The type of encoder: 'foldingnet' or 'dgcnn'
- `decoder_type`: str.  
The type of decoder: 'foldingnet' or 'dgcnn'


## References
[1] An Tao, 'Unsupervised Point Cloud Reconstruction for Classific Feature Learning', [GitHub Repo](https://github.com/AnTao97/UnsupervisedPointCloudReconstruction), 2020
