from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import cv2


config = Cfg.load_config_from_name('vgg_transformer')

# load pretrained weight
config['weights'] = './transformerocr.pth'

# set device to use cpu
config['device'] = 'cpu'
config['cnn']['pretrained'] = False
config['predictor']['beamsearch'] = False

detector = Predictor(config)
img = cv2.imread('img_check.png')
result = detector.predict(img)
print(result)
