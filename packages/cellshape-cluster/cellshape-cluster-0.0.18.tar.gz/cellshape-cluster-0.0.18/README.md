[![Project Status: Active – The project has reached a stable, usable
state and is being actively
developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Python Version](https://img.shields.io/pypi/pyversions/cellshape-cluster.svg)](https://pypi.org/project/cellshape-cluster)
[![PyPI](https://img.shields.io/pypi/v/cellshape-cluster.svg)](https://pypi.org/project/cellshape-cluster)
[![Downloads](https://pepy.tech/badge/cellshape-cluster)](https://pepy.tech/project/cellshape-cluster)
[![Wheel](https://img.shields.io/pypi/wheel/cellshape-cluster.svg)](https://pypi.org/project/cellshape-cluster)
[![Development Status](https://img.shields.io/pypi/status/cellshape-cluster.svg)](https://github.com/Sentinal4D/cellshape-cluster)
[![Tests](https://img.shields.io/github/workflow/status/Sentinal4D/cellshape-cluster/tests)](
    https://github.com/Sentinal4D/cellshape-cluster/actions)
[![Coverage Status](https://coveralls.io/repos/github/Sentinal4D/cellshape-cluster/badge.svg?branch=master)](https://coveralls.io/github/Sentinal4D/cellshape-cluster?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="https://github.com/Sentinal4D/cellshape-cluster/blob/main/img/cellshape_cluster_logo.png" 
     alt="Cellshape logo by Matt De Vries">
___
Cellshape-cluster is an easy-to-use tool to analyse the cluster cells by their shape using deep learning and, in particular, deep-embedded-clustering. The tool provides the ability to train popular graph-based or convolutional autoencoders on point cloud or voxel data of 3D single cell masks as well as providing pre-trained networks for inference.


## To install
```bash
pip install cellshape-cluster
```

## Usage
### Basic usage:
```python
import torch
from cellshape_cloud import CloudAutoEncoder
from cellshape_cluster import DeepEmbeddedClustering

autoencoder = CloudAutoEncoder(
    num_features=128, 
    k=20, 
    encoder_type="dgcnn"
)

model = DeepEmbeddedClustering(autoencoder=autoencoder, 
                               num_clusters=10,
                               alpha=1.0)

points = torch.randn(1, 2048, 3)

recon, features, clusters = model(points)
```

### To load a trained graph-based autoencoder and perform deep embedded clustering: 
```python
import torch
from torch.utils.data import DataLoader

import cellshape_cloud as cloud
import cellshape_cluster as cluster
from cellshape_cloud.vendor.chamfer_distance import ChamferDistance

dataset_dir = "path/to/pointcloud/dataset/"
autoencoder_model = "path/to/autoencoder/model.pt"
num_features = 128
k = 20
encoder_type = "dgcnn"
num_clusters = 10
num_epochs = 1
learning_rate = 0.00001
gamma = 1
divergence_tolerance = 0.01
output_dir = "path/to/output/"


autoencoder = CloudAutoEncoder(
    num_features=128, 
    k=20, 
    encoder_type="dgcnn"
)

checkpoint = torch.load(autoencoder_model)

autoencoder.load_state_dict(checkpoint['model_state_dict']

model = DeepEmbeddedClustering(autoencoder=autoencoder, 
                               num_clusters=10,
                               alpha=1.0)

dataset = cloud.PointCloudDataset(dataset_dir)

dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False) # it is very important that shuffle=False here!
dataloader_inf = DataLoader(dataset, batch_size=1, shuffle=False) # it is very important that batch_size=1 and shuffle=False here!

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=learning_rate * 16 / batch_size,
    betas=(0.9, 0.999),
    weight_decay=1e-6,
)

reconstruction_criterion = ChamferDistance()
cluster_criterion = nn.KLDivLoss(reduction="sum")

train(
    model,
    dataloader,
    dataloader_inf,
    num_epochs,
    optimizer,
    reconstruction_criterion,
    cluster_criterion,
    update_interval,
    gamma,
    divergence_tolerance,
    output_dir
)
```

## Parameters

- `autoencoder`: CloudAutoEncoder or VoxelAutoEncoder.  
Instance of autoencoder class from cellshape-cloud or cellshape-voxel
- `num_clusters`: int.  
The number of clusters to use in deep embedded clustering algorithm.
- `alpha`: float.  
Degrees of freedom for the Student's t-distribution. Xie et al. (ICML, 2016) let alpha=1 for all experiments.

