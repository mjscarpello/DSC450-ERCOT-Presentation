"""Pure source-image geometry for Studio S rectNormalized regions.

This does not create speech timing or establish which chart element is meaningful.
"""
import hashlib
from pathlib import Path

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rect_normalized(rect, image_size):
    x, y, w, h = map(float, rect)
    image_w, image_h = map(float, image_size)
    if image_w <= 0 or image_h <= 0 or w <= 0 or h <= 0:
        raise ValueError("Image and highlight dimensions must be positive")
    if x < 0 or y < 0 or x + w > image_w or y + h > image_h:
        raise ValueError("Region lies outside source image; do not silently clip")
    return [round(x / image_w, 6), round(y / image_h, 6),
            round(w / image_w, 6), round(h / image_h, 6)]

def project_contain(rect, image_size, layout):
    """Preview projected source region within a contain-fitted slide image object."""
    x, y, w, h = map(float, rect)
    iw, ih = map(float, image_size)
    rect_normalized(rect, image_size)
    scale = min(layout["width"] / iw, layout["height"] / ih)
    ox = layout["x"] + (layout["width"] - iw * scale) / 2
    oy = layout["y"] + (layout["height"] - ih * scale) / 2
    return [round(ox + x * scale, 3), round(oy + y * scale, 3),
            round(w * scale, 3), round(h * scale, 3)]

def proposal(image_path, rect, figure_id, region_id, method):
    from PIL import Image
    image_size = Image.open(image_path).size
    return {
        "figure_id": figure_id, "region_id": region_id,
        "source_sha256": sha256(image_path),
        "source_pixels": list(image_size),
        "rect_pixels": list(rect),
        "rectNormalized": rect_normalized(rect, image_size),
        "measurement_method": method,
        "reviewed": False,
        "studio_s_status": "asset region proposal only"
    }
