sam_checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"

sam = sam_model_registry[model_type](https://www.notion.so/checkpoint=sam_checkpoint)

[sam.to](http://sam.to/)(device=device)

predictor = SamPredictor(sam)

# Read image

image = cv2.imread(image_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) (512,512,3)

# 设置预测器的输入图像

predictor.set_image(image)

input_boxes = torch.tensor(filtered_data[image_name], device=predictor.device)

input_boxes = input_boxes.to(device=device)