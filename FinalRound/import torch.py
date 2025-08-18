import torch
import cv2
import numpy as np
import torchvision.transforms as transforms

# Load MiDaS model
model_type = "DPT_Large"  # Options: "DPT_Hybrid", "MiDaS_small" (for speed)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.hub.load("intel-isl/MiDaS", model_type).to(device)
model.eval()

# MiDaS's recommended image transformation
midas_transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform

def estimate_depth(image_path):
    # Load image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Transform image to MiDaS format
    input_tensor = midas_transform(image).unsqueeze(0).to(device)

    # Predict depth map
    with torch.no_grad():
        depth_map = model(input_tensor)

    depth_map = depth_map.squeeze().cpu().numpy()

    # Normalize depth map for visualization
    depth_map = cv2.normalize(depth_map, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    return depth_map

# Estimate depth
depth = estimate_depth("object.jpg")

# Display depth map
cv2.imshow("Depth Map", depth)
cv2.waitKey(0)
cv2.destroyAllWindows()
