from redis import Redis
import easyocr

import logging
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

import pathlib

PATH_DIAGRAM_GURU_PROJECT = str(pathlib.Path(__file__).parent.resolve())
PATH_DIAGRAM_UPLOADS = PATH_DIAGRAM_GURU_PROJECT + '/uploads/'

app = Flask(__name__)
# redis = Redis(host='redis', port=6379)


@app.route('/api/v1/recognizer', methods=['POST'])
def upload():

    if not request.json or 'image' not in request.json:
        abort(400)

    # get the base64 encoded string
    im_b64 = request.json['image']

    # convert it into bytes
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))

    # convert bytes data to PIL Image object
    img = Image.open(io.BytesIO(img_bytes))

    # PIL image object to numpy array
    img_arr = np.asarray(img)
    print('img shape', img_arr.shape)

    path_remote_diagram_name = request.json['diagram_name']
    diagram_name = path_remote_diagram_name.split('/')[-1]

    path_diagram = save_image_to_local(img, diagram_name)
    dict_diagram_objects = do_cmd_to_shell_diagram_detector(path_diagram)

    # response = {'message': 'success'}
    # return jsonify(response)

    result_dict = dict_diagram_objects
    return result_dict

    # return Response(response=response_pickled, status=200, mimetype="application/json")


def save_image_to_local(img_bytes, diagram_name):
    path_diagram = PATH_DIAGRAM_UPLOADS + diagram_name
    img_bytes.save(path_diagram)
    return path_diagram


def do_cmd_to_shell_diagram_detector(diagram_path_filename):
    """
    Execute a cmd command and return output string
    :param diagram_path_filename: String object.
    :return: dict_objects. Dictionary object. Dictionary with diagram objects.
    """
    logger.info("do_cmd_to_shell_diagram_detector")

    script_path_filename = PATH_DIAGRAM_GURU_PROJECT + '/detector_main.py'

    logger.info("path_diagram_guru_project: %s", PATH_DIAGRAM_GURU_PROJECT)
    logger.info("path_diagram_path_filename: %s", diagram_path_filename)

    cmd_diagram_detector = ["python", script_path_filename,
                            "--diagram_filename", diagram_path_filename,
                            "--display_image", "True"]

    process = subprocess.Popen(cmd_diagram_detector, stdout=subprocess.PIPE, stderr=None)
    cmd_output = process.communicate()

    dict_objects_str = cmd_output[0].decode("utf-8")

    if dict_objects_str and dict_objects_str.strip():
        dict_objects_str = str(dict_objects_str).replace("'", '"')
        dict_objects = eval(dict_objects_str)
    else:
        dict_objects = {}

    return dict_objects


if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # args = parse_arguments(parser)

    app.run()
    # app.run(host="0.0.0.0", debug=True)

