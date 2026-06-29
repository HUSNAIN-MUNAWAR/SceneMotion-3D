import cv2


def laplacian_sharpness(image_path_or_array) -> float:
    img = cv2.imread(str(image_path_or_array), cv2.IMREAD_GRAYSCALE) if not hasattr(image_path_or_array, 'shape') else image_path_or_array
    if img is None: return 0.0
    return float(cv2.Laplacian(img, cv2.CV_64F).var())


def is_blurry(image_path_or_array, threshold: float = 60.0) -> dict:
    score = laplacian_sharpness(image_path_or_array)
    return {"is_blurry": score < threshold, "sharpness": score, "threshold": threshold}
