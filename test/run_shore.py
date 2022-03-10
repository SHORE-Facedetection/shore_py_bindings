"""Example script to demonstrate pyshore usage

Runs Shore on images and saves the resulting images to disk
"""
import argparse
import pathlib
import sys
import time
import warnings

import numpy as np
from PIL import Image, ImageDraw

import pyshore

EXTENSIONS = ('.jpg', '.jpeg', '.tif', '.png')

warnings.simplefilter('ignore', Image.DecompressionBombWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--shore-model', default='Face.Front',
                    choices=('Face.Front', 'Face.Profile'),
                    help='Shore model')
parser.add_argument('--scale', default=1, type=float,
                    help='Shore imageScale parameter')
parser.add_argument('-e', '--extension', default='jpg',
                    help='Image extension')
parser.add_argument('-o', '--output_dir', help='Path to output directory')
parser.add_argument('inputs', nargs='+',
                    help='Path to input image or directory')


def draw_rect(pil_img, region):
    def extend_rect(r, by=1):
        return (r[0] - by, r[1] + by, r[2] - by, r[3] + by)

    draw = ImageDraw.Draw(pil_img)

    rect = tuple(region)
    draw.rectangle(rect, outline=(255, 0, 0))
    draw.rectangle(extend_rect(rect, by=1), outline=(255, 0, 0))
    draw.rectangle(extend_rect(rect, by=2), outline=(255, 0, 0))


def main(argv):
    args = parser.parse_args(argv)

    input_paths = [pathlib.Path(inp) for inp in args.inputs]
    input_files = []

    for input_path in input_paths:
        if input_path.is_dir():
            input_files.extend(input_path.glob('*.{}'.format(args.extension)))
        elif input_path.is_file():
            if input_path.suffix.lower() not in EXTENSIONS:
                print('Input path `{}` does not have supported image extension'
                      .format(input_path))
            input_files.append(input_path)
        else:
            print('Input path `{}` does not exist'.format(input_path))
            return

    print('Found {} images to process'.format(len(input_files)))
    if len(input_files) == 0:
        return

    if args.output_dir:
        output_dir = pathlib.Path(args.output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
    else:
        output_dir = None

    engine = pyshore.create_face_engine(modelType=args.shore_model,
                                        imageScale=args.scale)

    for image_path in input_files:
        img_pil_rgb = Image.open(str(image_path))
        print('Processing image `{}` with shape {}'.format(image_path,
                                                           img_pil_rgb.size))
        img_pil_gray = img_pil_rgb.convert('L')
        image = np.array(img_pil_gray)

        start_time = time.time()
        content = engine(image, 'GRAYSCALE')
        duration = time.time() - start_time
        print('- Processed image in {:.3f} seconds'.format(duration))

        print('- Content: {}'.format(content))
        if content.num_infos > 0:
            for key, info in content.infos().items():
                print('  * {}: {}'.format(key, info))

        if content is not None:
            print('- Detected {} objects'.format(content.num_objects))
            for obj in content.objects():
                print(repr(obj))
                draw_rect(img_pil_rgb, obj.region)

        if output_dir is not None:
            out_path = output_dir / 'processed_{}'.format(image_path.name)
            if out_path.suffix == '.tif':
                out_path = out_path.parent / '{}.png'.format(out_path.stem)
            print('- Saving marked image to `{}`'.format(out_path))
            img_pil_rgb.save(str(out_path))


if __name__ == '__main__':
    main(sys.argv[1:])
