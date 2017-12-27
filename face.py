#coding: utf8 
from aip import AipFace
import cv2
import pdb
# baidu api APP_ID
APP_ID = ''
# baidu api API_KEY
API_KEY = ''
#baidu api SECRET_KEY
SECRET_KEY = ''

client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def santa(filePath, hatPath):
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    hat_img = cv2.imread(hatPath, cv2.IMREAD_UNCHANGED)
    face_img = cv2.imread(filePath)
    r,g,b,a = cv2.split(hat_img)
    rgb_hat = cv2.merge((r,g,b))
    image = get_file_content(filePath)

    options = {}
    options["max_face_num"] = 1
    options["face_fields"] = "age"
    options["face_fields"] = "landmark"

    res = client.detect(image, options)
    if res['result_num'] == 0:
        return face_img
    lm = res['result'][0]['landmark']
    lc = res['result'][0]['location']
    x, y, face_w, face_h = lc['left'], lc['top'], lc['width'], lc['height']
    l_eye = lm[0]
    r_eye = lm[1]
    l_c_eyes, r_c_eyes = (l_eye['x'] + r_eye['x']) // 2, (l_eye['y'] + r_eye['y']) // 2
    factor = 1.5
    resized_hat_h = int(round(rgb_hat.shape[0]*face_w/rgb_hat.shape[1]*factor))
    resized_hat_w = int(round(rgb_hat.shape[1]*face_w/rgb_hat.shape[1]*factor))
    if resized_hat_h > y:
        resized_hat_h = y-1
    resized_hat = cv2.resize(rgb_hat,(resized_hat_w,resized_hat_h))
    mask = cv2.resize(a,(resized_hat_w,resized_hat_h))
    mask_inv =  cv2.bitwise_not(mask)
    dh = -20
    dw = -20
    bg_roi = face_img[y+dh-resized_hat_h:y+dh, x+dw:x+dw+resized_hat_w]
    bg_roi = bg_roi.astype(float)
    mask_inv = cv2.merge((mask_inv,mask_inv,mask_inv))
    alpha = mask_inv.astype(float)/255
    alpha = cv2.resize(alpha,(bg_roi.shape[1],bg_roi.shape[0]))
    bg = cv2.multiply(alpha, bg_roi)
    bg = bg.astype('uint8')
    hat = cv2.bitwise_and(resized_hat,resized_hat,mask = mask)
    hat = cv2.resize(hat,(bg_roi.shape[1],bg_roi.shape[0]))
    add_hat = cv2.add(bg,hat)
    face_img[y+dh-resized_hat_h:y+dh, x+dw:x+dw+resized_hat_w] = add_hat
    return face_img

if __name__ == "__main__":
    filePath = 'Ei.jpg'
    hatPath = 'Santa-hat-icon.png'
    santa(filePath, hatPath) 
