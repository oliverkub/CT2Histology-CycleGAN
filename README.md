# CT2Histology-CycleGAN Repository

This repository includes the preprocessing scripts and final model used in the thesis "Transforming Medicine: CT to Histology Scan Translation with Unpaired Data using Cycle-GAN". 

Use this code to prepare your own dataset for the original PyTorch implementation: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix). 

Comments and some code parts have been optimised with ChatGPT-4o.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)

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

Run each Jupyter notebook separately and add the required paths. To use the final model (`latest_model_G_A.pth`), refer to the original CycleGAN repository documentation: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).

## Files

- `data_preprocessing.ipynb`: Contains all steps used in this thesis to preprocess the data before training the Cycle-GAN model.
- `latest_model_G_A.pth`: Includes the final model of this thesis. To use this, refer to the original repository: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).
- `evaluation.ipynb`: Highlights all functions used to create the plots for evaluation.
