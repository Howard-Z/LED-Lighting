from numpy import ndarray, astype


def get_color_affine(color1: ndarray, color2: ndarray, total_frames: int, current_frame: int):
    t = current_frame / total_frames
    return (color2 * t + color1 * (1 - t)).astype(int)

for i in range(50):
    print(get_color_affine(begin, end, 50, i))