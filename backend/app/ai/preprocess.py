import cv2
import numpy as np
from typing import Union, Tuple

def preprocess_image(
    image_bytes_or_path: Union[bytes, str],
    target_size: Tuple[int, int] = (224, 224)
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Preprocess raw image (bytes or path) using OpenCV:
    1. Decode/Read image into BGR NumPy array.
    2. Convert BGR to RGB color space.
    3. Resize to target_size (default 224x224).
    4. Normalize pixel values [0, 255] -> [0.0, 1.0].
    5. Reformat into NCHW shape (1, 3, H, W) for neural network input.

    Returns:
        Tuple of (nchw_tensor, raw_rgb_image)
    """
    if isinstance(image_bytes_or_path, bytes):
        nparr = np.frombuffer(image_bytes_or_path, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image from provided byte stream.")
    elif isinstance(image_bytes_or_path, str):
        img = cv2.imread(image_bytes_or_path)
        if img is None:
            raise ValueError(f"Failed to read image from path: {image_bytes_or_path}")
    else:
        raise TypeError("Input must be image bytes or a valid file path string.")

    # Convert BGR to RGB
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize to target size
    resized = cv2.resize(rgb_img, target_size, interpolation=cv2.INTER_AREA)

    # Normalize pixels [0.0, 1.0]
    normalized = resized.astype(np.float32) / 255.0

    # ImageNet Mean & Std Normalization
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    standardized = (normalized - mean) / std

    # Reformat HWC -> CHW -> NCHW (Batch size = 1)
    chw = np.transpose(standardized, (2, 0, 1))
    nchw = np.expand_dims(chw, axis=0)

    return nchw, resized
