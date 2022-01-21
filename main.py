import argparse
import cv2
import easyocr

def parse_arguments(parser):
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['train', 'validate', 'infer'], default='infer')
    parser.add_argument('--decoder', choices=['bestpath', 'beamsearch', 'wordbeamsearch'], default='bestpath')
    args = parser.parse_args()
    return args

def main(args):
    reader = easyocr.Reader(['en', 'es'])
    result = reader.readtext('data/test01.jpg')
    print(result)

# img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
# assert img is not None
#
# preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
# img = preprocessor.process_img(img)
#
# batch = Batch([img], None, 1)
# recognized, probability = model.infer_batch(batch, True)
# print(f'Recognized: "{recognized[0]}"')
# print(f'Probability: {probability[0]}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    args = parse_arguments(parser)

    main(args)