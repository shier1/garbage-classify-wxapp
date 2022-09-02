import paddle
import cv2
import numpy as np
import math


label_lists = {
    0:"可回收物",
    1:"厨余垃圾",
    2:"其他垃圾",
    3:"有害垃圾"
}

def softmax(x):
    y = np.exp(x - np.max(x))
    f_x = y / np.sum(np.exp(x))
    return f_x

def normalize(img):
    mean = [0.515, 0.549, 0.575]
    std=[0.247, 0.237, 0.231]
    mean = np.float32(np.array(mean).reshape(-1, 1, 1))
    std = np.float32(np.array(std).reshape(-1, 1, 1))
    img = (img - mean) / std
    return img

def center_crop(image, size=(224,224)):
    h, w = image.shape[0:2]
    th, tw = size
    i = int(round((h - th) / 2.))
    j = int(round((w - tw) / 2.))
    return image[i:i + th, j:j + tw, :]

def predict_one_image(model_dir,image, image_size=224, scale=0.875):
    model = paddle.jit.load(model_dir)
    model.eval()
    scale_size = int(math.floor(image_size/scale))
    image_data = cv2.resize(image, dsize=(scale_size, scale_size))
    image_data = center_crop(image_data, size=(224,224))
    input_data = image_data/255
    input_data = input_data.transpose(2,0,1)
    input_data = normalize(input_data)
    input_data = np.expand_dims(input_data, axis=0).dtype('float32')
    input_tensor = paddle.to_tensor(input_data)
    output_data = model(input_tensor).numpy()
    label = output_data.argmax()
    prob = output_data[label]
    return label_lists[label]

def predict_video(model_dir, video_path, image_size=224, scale=0.875):
    config = lite.MobileConfig()
    config.set_model_from_file(model_dir)
    predictor = lite.create_paddle_predictor(config)
    scale_size = int(math.floor(image_size/scale))

    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        print('the Video path is not exist')
        return
    print('start predict the images')
    while(True):
        ret, frame = capture.read()
        if ret is None:
            break
        image_data = cv2.resize(frame, dsize=(scale_size, scale_size))
        image_data = center_crop(image_data, size=(224,224))
        
        input_data = image_data/255
        input_data = input_data.transpose(2,0,1)
        input_data = normalize(input_data)
        input_data = np.expand_dims(input_data, axis=0)
        input_tensor = predictor.get_input(0)
        input_tensor.from_numpy(input_data.astype("float32"))

        predictor.run()

        output_tensor = predictor.get_output(0)
        output_data = output_tensor.numpy()
        label = output_data.argmax()
        prob = output_data[label]
        cv2.putText(frame, label_lists[label], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        yield frame

if __name__ == "__main__":
    image_path = 'cdb12.jpg'
    image = cv2.imread(image_path)
    model_dir = 'static_model'
    print(predict_one_image(model_dir=model_dir, image=image))