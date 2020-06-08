import argparse
import ast
import os

import numpy as np
from skimage.io import imread
from skimage.transform import rescale

from api import PRN
from utils.write import write_obj_with_colors


def main(args, name):
    # ---- init PRN
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu  # GPU number, -1 for CPU
    prn = PRN(is_dlib=args.isDlib)

    # ------------- load data
    image_folder = args.inputDir
    save_folder = args.outputDir
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    image = imread(image_folder + name + ".jpg")
    [h, w, c] = image.shape
    if c > 3:
        image = image[:, :, :3]

    max_size = max(image.shape[0], image.shape[1])
    if max_size > 1000:
        image = rescale(image, 1000. / max_size)
        image = (image * 255).astype(np.uint8)
    pos = prn.process(image)  # use dlib to detect face

    image = image / 255.
    if pos is None:
        return

    vertices = prn.get_vertices(pos)
    save_vertices = vertices.copy()
    save_vertices[:, 1] = h - 1 - save_vertices[:, 1]
    colors = prn.get_colors(image, vertices)

    write_obj_with_colors(os.path.join(save_folder, name + '.obj'), save_vertices, prn.triangles,
                          colors)


def driver(name):
    try:
        data_path = os.path.abspath(os.path.join(
            '..', os.getcwd())) + "/instance/uploads/"
        parser = argparse.ArgumentParser(
            description='Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network')

        parser.add_argument('-i', '--inputDir', default=data_path, type=str,
                            help='path to the input directory, where input images are stored.')
        parser.add_argument('-o', '--outputDir', default=data_path, type=str,
                            help='path to the output directory, where results(obj,txt files) will be stored.')
        parser.add_argument('--gpu', default='-1', type=str,
                            help='set gpu id, -1 for CPU')
        parser.add_argument('--isDlib', default=True, type=ast.literal_eval,
                            help='whether to use dlib for detecting face, default is True, if False, the input image should be cropped in advance')
        parser.add_argument('--is3d', default=True, type=ast.literal_eval,
                            help='whether to output 3D face(.obj). default save colors.')

    except:
        return -1
    try:
        main(parser.parse_args(), name)
        return 1
    except:
        return -2
