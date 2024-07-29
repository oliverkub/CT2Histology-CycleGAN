# CT2Histology-CycleGAN Repository

This repository includes the preprocessing scripts, evaluation graphs and final model used in the thesis "Transforming Medicine: CT to Histology Scan Translation with Unpaired Data using Cycle-GAN" by Oliver Kubesch, released in 2024. 

Use the provided code to prepare your own dataset for the original PyTorch implementation: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

Comments and some code parts have been optimised with ChatGPT-4o.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [Notes](#notes)

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/oliverkub/CT2Histology-CycleGAN.git
    cd CT2Histology-CycleGAN
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Each file has its own required paths that need to be set before execution.

To use the final model (`latest_model_G_A.pth`), refer to the original CycleGAN repository documentation: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

## Files

- `data_preprocessing.ipynb`: Contains all steps used in this thesis to preprocess the data before training the Cycle-GAN model.
- `latest_net_G_A.pth`: Includes the final model of this thesis. To use this, refer to the original repository: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).
- `evaluation.ipynb`: Highlights all functions used to create the plots for evaluation.
- `image_metrics.py`: Calculates the image similarity metrics between CT and histology images and stores them.
- `run_tmux.sh`: Runs `image_metrics.py` in a tmux session for the whole folder.

## Notes

### Setting Up Your Dataset for Cycle-GAN

To use your own dataset with the PyTorch implementation of Cycle-GAN ([pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)), you need to organize your data in a specific directory structure. For more information, visit the original repository:

1. **Create a main folder with your desired dataset name (`DATASETNAME`).**
2. **Inside this main folder, create the following subdirectories:**
    - `trainA`: This folder should contain your CT images.
    - `trainB`: This folder should contain your histology images.
    - `testA`: (Optional) This folder can contain your test CT images.
    - `testB`: (Optional) This folder can contain your test histology images.

  
After setting up your dataset, you can use the following commands to train and test your Cycle-GAN model.

### Training
To train your Cycle-GAN model, run the following command:
```bash
python3 train.py --dataroot ./datasets/DATASETNAME --name DATASETNAME --model cycle_gan --gpu_ids 0 --display_id 1
```
#### Testing
Before testing, copy the latest trained model checkpoint to the test model checkpoint:
```bash
cp ./checkpoints/DATASETNAME/latest_net_G_A.pth ./checkpoints/DATASETNAME/latest_net_G.pth
```

To test your Cycle-GAN model, run the following command:
```bash
python3 test.py --dataroot ./datasets/DATASETNAME --name DATASETNAME --model test --no_dropout --gpu_ids 0
```
