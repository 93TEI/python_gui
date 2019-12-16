import os
import sys
import argparse
import cv2
import time
# 아래 3개는 얘네가 만든거
from config_reader import config_reader # 모델 옵션값, 모델 불러올 때 사용하는 코드

from processing import extract_parts, draw # 함수 2개 사용하는데, 이미지에서 파츠 찾는거 extract, 그리는건 draw

from model.cmu_model import get_testing_model # 모델 가져오는 것

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

currentDT = time.localtime()
start_datetime = time.strftime("-%m-%d-%H-%M-%S", currentDT)


def crop(image, w, f): # 이미지 사이즈 줄이는 함수 // 전체를 가지고 하면 속도가 느려지기 때문에
    return image[:, int(w * f): int(w * (1 - f))]


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', type=int, default=0, help='ID of the device to open') #parser에서 받는거
    parser.add_argument('--model', type=str, default='model/keras/model.h5', help='path to the weights file') #모델경로
    parser.add_argument('--frame_ratio', type=int, default=7, help='analyze every [n] frames')
    # --process_speed changes at how many times the model analyzes each frame at a different scale
    parser.add_argument('--process_speed', type=int, default=1,
                        help='Int 1 (fastest, lowest quality) to 4 (slowest, highest quality)')
    parser.add_argument('--out_name', type=str, default=None, help='name of the output file to write')
    parser.add_argument('--mirror', type=bool, default=True, help='whether to mirror the camera')

    # 받은 값들 저장하는것
    args = parser.parse_args()
    device = args.device
    keras_weights_file = args.model
    frame_rate_ratio = args.frame_ratio
    process_speed = args.process_speed
    out_name = args.out_name
    mirror = args.mirror

    print('start processing...')

    # load model
    # authors of original model don't use
    # vgg normalization (subtracting mean) on input images
    model = get_testing_model()
    model.load_weights(keras_weights_file)

    # load config
    params, model_params = config_reader()

    # Video reader
    cam = cv2.VideoCapture(device) # 디바이스=0은 카메라, 파일넣고싶으면 파일 경로 넣으면 됨
    # CV_CAP_PROP_FPS
    input_fps = cam.get(cv2.CAP_PROP_FPS) # 해당카메라의 프레임으로 추측
    print("Running at {} fps.".format(input_fps))

    ret_val, orig_image = cam.read() #ret = 제대로 read됐는지확인하는 부울타입, orig = 실질적인 프레임단위의 이미지

    width = orig_image.shape[1]
    height = orig_image.shape[0]
    factor = 0.3

    out = None
    # Output location
    if out_name is not None and ret_val is not None: # out_name이 parser 40번째줄/ out_name이 잇으면 파일생성/
        output_path = 'videos/outputs/'
        output_format = '.mp4'
        video_output = output_path + out_name + output_format

        # Video writer
        output_fps = input_fps / frame_rate_ratio

        tmp = crop(orig_image, width, factor)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_output, fourcc, output_fps, (tmp.shape[1], tmp.shape[0]))

        del tmp

    scale_search = [0.22, 0.25, .5, 1, 1.5, 2]  # [.5, 1, 1.5, 2]
    scale_search = scale_search[0:process_speed]

    params['scale_search'] = scale_search

    i = 0  # default is 0
    resize_fac = 8
    # while(cam.isOpened()) and ret_val is True:
    while True:

        cv2.waitKey(10)

        if cam.isOpened() is False or ret_val is False:
            break

        if mirror:
            orig_image = cv2.flip(orig_image, 1)

        tic = time.time()

        cropped = crop(orig_image, width, factor) # 파일 자름
        #opencv함수로 사이즈 조절하는 것
        input_image = cv2.resize(cropped, (0, 0), fx=1/resize_fac, fy=1/resize_fac, interpolation=cv2.INTER_CUBIC)

        input_image = cv2.cvtColor(input_image, cv2.COLOR_RGB2BGR)

        # generate image with body parts
        # extract_part
        all_peaks, subset, candidate = extract_parts(input_image, params, model, model_params)
        canvas = draw(cropped, all_peaks, subset, candidate, resize_fac=resize_fac)

        print('Processing frame: ', i)
        toc = time.time()
        print('processing time is %.5f' % (toc - tic))

        if out is not None: # 이게 있으면 계속 출력하는 것
            out.write(canvas) # 이미지 위에 만들어진 스켈레톤!

        # canvas = cv2.resize(canvas, (0, 0), fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

        cv2.imshow('frame', canvas)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        ret_val, orig_image = cam.read()

        i += 1