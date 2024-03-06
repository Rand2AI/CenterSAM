## Dataset Preparation

In order to be able to start the training of CenterSAM, a setup of the dataset is required. Currently, we provide the example of using ***TissueNet*** dataset as the the target dataset in this github code, steps as follow:

### Download and locate the dataset

For The original TissueNet dataset, you may download it by visit the [official dataset website](https://datasets.deepcell.org/data) (A github account is required for browsing the data).

The TissueNet dataset is originally provided in format of three ***npz*** file, splited by ***train*** ***test*** and ***val*** purpose. Images and annotation information are all compose inside those npz file. 

While the input of CenterSAM model need to seperately handle the images and annotations, you need to follow the ***Readme.md*** file inside the downloaded **tissuenet_v1.1.zip** file to manually extract the images and annotations. In order to provide a more convenient way to start training the model and give you better understand of dataset setup requiments, we provide extracted images and annotations in [**This Google Drive Link**](https://drive.google.com/drive/folders/18MS9NUA0FX8UTmQ0Gxq7HzJC5YtJ5Bx7?usp=drive_link). Please download the images.zip and annotations.zip file via the link and locate as follow:



```
CenterSAM/
└── data/
    └── TissueNet/
        ├── images/
        │   ├── train1.png
        │   ├── train2.png
        │   ├── ...
        │   ├── test1.png        
        │   ├── ...
        │   ├── val1.png
        │   └── ...
        └── annotations/
            ├── train.json
            ├── val.json
            └── test.json
```

Now you can follow [Quick Start](./docs/quick_start.md) to start the training process of CenterSAM.

In case of train custom dataset, please read the section below.

### Train custom dataset

For a custom dataset, in addition to separating images and annotations and placing them under CenterSAM/data/{Your_dataset_name}/ as described above, you need to create a **py** file with the same name as your dataset in the ***CenterSAM/src/lib/datasets/dataset/*** folder, Assuming that the name of your dataset is **CUSTOM**, you can perform the following steps to complete the configuration：

* Copy TissueNet.py file under the ***CenterSAM/src/lib/datasets/dataset/***, rename it to **CUSTOM.py**
* Rename all ***TissueNet*** inside the file to ***CUSTOM***
* Replace the ***mean*** and ***std*** variable with the mean and standard deviation of your CUSTOM dataset images.
* Modify the ***CenterSAM/src/lib/datasets/sample/dataset_factory.py*** file: 
    - Import the **CUSTOM.py** file in the same way as TissueNet: add line ***from .dataset.CUSTOM import CUSTOM***
    - Add ***'TissueNet': TissueNet*** key-value paris in ***dataset_factory*** dictionary

