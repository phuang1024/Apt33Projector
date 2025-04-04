"""
Display image or video on the board.
"""

import time

import cv2
import numpy as np

from display import Display

IMG_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
VID_EXTS = (".mp4", ".avi", ".mov")


def display_image(disp: Display, img: np.ndarray, thres=0.5, keep_aspect=True, highpass=False):
    """
    img: Shape (H, W, C). Channels are averaged and values normalized to (0, 1).
    keep_aspect: If True, pads zeros to keep original image aspect.
    highpass: Whether to apply high pass filter.
    """
    if keep_aspect:
        aspect = img.shape[1] / img.shape[0]
        target_aspect = disp.board.shape[1] / disp.board.shape[0]
        if aspect > target_aspect:
            new_img = np.zeros((int(img.shape[1] / target_aspect), img.shape[1], img.shape[2]))
        else:
            new_img = np.zeros((img.shape[0], int(img.shape[0] * target_aspect), img.shape[2]))
        new_img[: img.shape[0], : img.shape[1]] = img
        img = new_img

    img = cv2.resize(img, (disp.board.shape[1], disp.board.shape[0]))
    if highpass:
        kernel = np.array([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1],
        ])
        img = cv2.filter2D(img, -1, kernel)

    img = img.mean(axis=2)
    img = np.interp(img, (img.min(), img.max()), (0, 1))
    img = img > thres
    disp.board[:] = img


def disp_daemon(disp: Display, args):
    if args.file.endswith(IMG_EXTS):
        img = cv2.imread(args.file)
        display_image(disp, img)

    elif args.file.endswith(VID_EXTS):
        cap = cv2.VideoCapture(args.file)
        interval = 1 / cap.get(cv2.CAP_PROP_FPS)
        while disp.run:
            ret, frame = cap.read()
            if not ret:
                break
            display_image(disp, frame)
            time.sleep(interval)


def main():
    disp = Display()
    disp.parser.add_argument("file", type=str)
    args = disp.parser.parse_args()

    disp.add_daemon(disp_daemon, (disp, args))
    disp.start()


if __name__ == "__main__":
    main()
