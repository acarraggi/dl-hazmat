import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import argparse
import random
import os


def start_viewer(full_path, classes_names):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)

    while (True):
        classes = classes_names[0]
        gts_folder = os.path.join(full_path, classes, "gts")
        img_folder = os.path.join(full_path, classes)
        gt_output = glob(gts_folder + "/*")
        
        # Get random image index
        idx = random.randint(0, len(gt_output)-1)
        # Read image 
        img = cv2.imread(os.path.join(img_folder, str(idx)+".jpg"))
        h,w, _ = img.shape

        # Read gt lines
        lines = []
        with open(os.path.join(gts_folder, str(idx)+".txt"), "r") as fp:
            lines = fp.readlines()

        if(len(lines) == 0):
            print("ERROR ON", idx)
        
        # convert gt to polygon vertex coordinates
        values = lines[0].split(",")
        
        tl = [float(values[1])*w, float(values[2])*h]
        tr = [float(values[3])*w, float(values[4])*h]
        bl = [float(values[5])*w, float(values[6])*h]
        br = [float(values[7])*w, float(values[8])*h]

        pts = np.array([

            [int(tl[0]), int(tl[1])],
            [int(bl[0]), int(bl[1])],
            [int(br[0]), int(br[1])],
            [int(tr[0]), int(tr[1])]
            
        ], dtype=np.int32)

        # Draw the rectangle
        pts = pts.reshape((-1, 1, 2))
        img =cv2.polylines(img, [pts], isClosed=True, color=(0,255,0), thickness=3, lineType=cv2.LINE_8)

        # show image
        cv2.imshow("image", img)
        key = cv2.waitKey(0)

        if(key == ord("q")):
            break
        
        # Re-shuffle the data
        np.random.shuffle(classes_names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset_root_path', required=True, type=str, 
                        help="path which contains train and test zip experiences.")
    parser.add_argument("-e", "--experience", required=True, type=int,
                        help="path which extract all the experience with the dataset structure")
    parser.add_argument("-t", "--type", default="train", help="List of dataset to extract. The accepted values are: 'train', 'test'")
    args = parser.parse_args()

    full_path = os.path.join(args.dataset_root_path, args.type, "experience_{}".format(args.experience))
    assert os.path.exists(full_path), "This path doesn't found {}".format(full_path)
    classes_names = os.listdir(full_path)

    np.random.shuffle(classes_names)

    print("################ VIEWER ####################################")
    print(" - Please press q to quit the viewer")
    print(" - other keys for next image")

    start_viewer(full_path, classes_names)

    