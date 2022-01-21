import argparse
import cv2
import easyocr
from simplehtr.src.main import infer_textline


def parse_arguments(parser):
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
    args = parser.parse_args()
    return args


def main(args):
    reader = easyocr.Reader(['en', 'es'])
    result, img, img_cv_grey = reader.readtext('data/test02.jpg')
    for aux_text in result:
        print(aux_text)
        infer_textline(img)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)

    main(args)
