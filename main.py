import argparse
import easyocr
from simplehtr.src.main import infer_textline, main2
from PIL import Image
import matplotlib.pyplot as plt

def parse_arguments(parser):
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
    args = parser.parse_args()
    return args


def main(args):
    reader = easyocr.Reader(['en', 'es'])
    result, img, img_cv_grey = reader.readtext('data/test02.jpg')
    for aux_text, aux_img in zip(result, img_cv_grey):
        print('******', aux_text)
        # print(img.size)
        # print(img_cv_grey.size)

        print(img_cv_grey.shape)
        plt.imshow(img_cv_grey)
        plt.show()

        # img = Image.open(StringIO(img))
        # img = Image.fromarray(aux_img, 'RGB')
        # img.show()
        # main2(aux_img)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)

    main(args)
