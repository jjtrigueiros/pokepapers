import cv2
import numpy as np


def transform_image(
    img: cv2.Mat, width: int, height: int, scaling: float = 1.0
) -> cv2.Mat:
    """
    Tile and crop an image `img` up to the resolution given by `width`x`height`.

    The `scaling` factor allows downscaling of the original tile image, to allow hiding
    undesirable visual artifacts, ex. due to compression.
    Since there is no benefit in upscaling, `scaling` should always be `>=1.0`.
    """

    source_resolution = np.array(img.shape)
    target_resolution = np.array((height, width, 3))
    resolution_scaler = np.array((scaling, scaling, 1))

    crop_size = (target_resolution * resolution_scaler).astype(int)
    tile_factor = np.ceil((crop_size / source_resolution)).astype(int)

    img = np.tile(img, tile_factor)
    img = img[: crop_size[0], : crop_size[1], :]  # crop
    img = cv2.resize(img, target_resolution[1::-1])

    return img
