## Qucik Start

### Training
After properly setup the environment and dataset, you may now use several command to start the training process.

All options and their function could be found in the **src/lib/opts.py** file. Most of the value the the **opts.py** file is already given an default value, which allow you to simple type the below command to start training the CenterSAM model:


~~~
#cd src/lib

python main.py ctdet
~~~

you can easily adjust most of training option by command line, for example, if you intend to use **res_18** architecture instead of **hourglass**, with batch size equal to 64 and **l2** regression loss, the following command should be use for the training process:


~~~
python main.py ctdet --arch res_18 --batch_size 64 --reg_loss l2
~~~

There are many option including **conv layer channels for output head**, **learning rate** and so on, explore it by dive into the ***opts.py*** file if you want.


### Testing and Visualization

The trained model will be saved to the path: **CenterSAM/exp/ctdet/TissueNet_ctdet/model_best.pth** or **CenterSAM/exp/ctdet/TissueNet_ctdet/model_last.pth** (here we use example of ctdet task and TissueNet dataset). For convenience， we will use **(Model_path)** as a refer to the **CenterSAM/exp/ctdet/TissueNet_ctdet/model_best.pth** for the following tutorial.

let's say you have multiple images want to test that located under ***CenterSAM/demo_images*** folder, You may type the below command to visulize the effect of trained models：

~~~
python demo.py ctdet --demo CenterSAM/demo_images --load_model CenterSAM/exp/ctdet/TissueNet_ctdet/model_best.pth
~~~

The ***--demo*** argument accept a set of images or a single image.

This **demo.py** script allow you to visulize the result of detection stage, which shows the quality of automatically generated ***prompts*** and also produce the ***json** file of prompts. This json file would be the input file used for the segment stage.

In order to make it easier to use and facilitate subsequent development, we split the segment stage scripts and code and put them in ***CenterSAM/SAM/notebooks***. You can find the scripts and code we use for produce the **evaluation** results and figure in that folder.

Basiclly, here we first generate a json file which storage all the prompts information from the detectoion stage, then generate final instance segment result with the help of SAM. After getting prompts json file from above, you can now run through notebook code in the CenterSAM/SAM/notebooks folders accordingly (dependding on the dataset you are testing). The evaluation and visualization of final instance segment result is all inside the ***ipynb*** files

