## Instructions

This is the environment setup tutorial for paper: **CenterSAM: Fully Automatic Prompt for Dense Nucleus Segmentation**

The following steps has been tested on the **Ubuntu 20.04** OS with **RTX 3090 GPU**. You may experience errors if you have different hardware and OS systems that may not be able to follow this tutorial exactly, but most of the errors are in the compatibility between python version, cuda version torch library version and GPU in your local machine.

## Installation

### Prompt Generate Stage
* Create virtual environment

```python
conda create -n CenterSAM python=3.8
```

* Clone the CenterSAM source code:

```python
git clone https://github.com/Daeda1used/CenterSAM.git
```
* Install pytorch, torchvision, Cython, matplotlib and other requirements. pytorch=1.7.0 and torchvision=0.8.0 is used by default, since it meet the minimum requiment for SAM(Segment Anything Model) used in segment stage.

```python
pip install pytorch
pip install torchvision
pip install matplotlib
pip install Cython
pip install -r requirements.txt
```

* Use conda to install cudnn:

```python
conda install cudnn
```

* Install [COCOAPI](https://github.com/cocodataset/cocoapi):

```python
git clone https://github.com/cocodataset/cocoapi.git $COCOAPI
cd $COCOAPI/PythonAPI
make
python setup.py install --user
```

* Now is the hard part, we should first compile **nms** and then compile **DCNv2**:
Following the link to do so: https://github.com/xingyizhou/CenterNet/issues/7
 

```python
cd CenterNet\src\lib\external
#python setup.py install
python setup.py build_ext --inplace
```

* After build **nms,** you will meet problem will compile the DCNv2, here we need to find the specific version of DCNv2 support using this link:

    [Trying to build CenterNet on pytorch1.6, fail to build DCN · Issue #861 · xingyizhou/CenterNet](https://github.com/xingyizhou/CenterNet/issues/861#issuecomment-745271016)

    Download the DCNv2 from this github and replace the original DCNv2 folder under `CenterSAM\lib\models\networks`

    Enter DCNv2 folder:

```python
vim cuda/dcn_va_cuda.cu
"""
# extern THCState *state;
THCState *state = at::globalContext().lazyInitCUDA();
"""

python setup.py build develop
```


### Segment Stage (Base on provided box prompts)
* Next, to be able to perform segment with the help of SAM, it is recommend to follow installation tutorial from official SAM github: 

    [Official SAM Github][def]

[def]: https://github.com/facebookresearch/segment-anything


At this point, all the environment configuration has been completed, if you encounter difficult to reconcile the compatibility issues in the process of environment configuration, we recommend that you independently create two different virtual environments to achieve the CenterSAM prompt generate stage and segment stage (SAM).

In order to make it easier for users with different environment configuration options to experiment, we have provided jupyter notebook code in the notebooks folder of the root directory that splits the stage based on the generated prompts, allowing anyone to test the results if they already have box prompts.