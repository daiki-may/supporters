import cv2
import numpy as np
# from IPython import display
from matplotlib import pyplot as plt
import datetime
import os
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage

if __name__ == '__main__':
    cred = credentials.Certificate(
        "/Users/daiki.m/Desktop/supporters/gikucamp-firebase-adminsdk-bw43u-2fb954e096.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'gikucamp.appspot.com'})
    db = firestore.client()
    doc_ref = db.collection(u'data').document(u'90TwVL13wTuPpmCgw24C')
    ref = db.collection(u'data')
    docs = ref.stream()

    bucket = storage.bucket()
    # filename = 'outline.png'
    # blob = bucket.blob(filename)
    content_type = 'outline/png'

    # filename2 = 'img_gomi.png'
    filename2 = 'img_gomi.png'
    blob = bucket.blob(filename2)

    # 現在画像を取り込む
    camera = cv2.VideoCapture(1)
    ret, frame = camera.read()
    if ret:
        print('Success')
        cv2.imwrite('final.png', frame)

    else:
        print('Failed')
    start_name = ''
    #start_name = 'start.png'
    final_name = 'final.png'
    # start_name = 'outline0.png'
    # final_name = 'outline40.png'
    # 画像の読み込み
    img_src1 = cv2.imread(start_name, 0)
    img_src2 = cv2.imread(final_name, 0)

    fgbg = cv2.createBackgroundSubtractorMOG2()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    # 検出画像
    bg_diff_path = 'result.png'
    cv2.imwrite(bg_diff_path, fgmask)
    print('Success2')

    # 画像読み込み
    img = cv2.imread('result.png')
    img2 = cv2.imread('final.png')

    # グレースケール化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2値化
    ret, bin_img = cv2.threshold(gray, 86, 100, cv2.THRESH_BINARY_INV)
    threshold = 120
    bin_img = gray.copy()
    bin_img[bin_img < threshold] = 0
    bin_img[bin_img >= threshold] = 255

    # 輪郭抽出
    contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 小さい輪郭を削除
    contours = list(filter(lambda x: cv2.contourArea(x) > 100000, contours))

    # 外形のマスク画像を生成
    mask = np.zeros_like(img[:, :, 0])
    cv2.drawContours(mask, [contours[0]], -1, color=255, thickness=-1)
    ch_b, ch_g, ch_r = cv2.split(img2[:, :, :3])
    img_alpha = cv2.merge((ch_b, ch_g, ch_r, mask))

    # 外枠の矩形を計算
    x, y, w, h = cv2.boundingRect(contours[0])
    img_gomi = img_alpha[y:y + h, x:x + w]
    cv2.imwrite("img_gomi.png", img_gomi)

    # 輪郭を描写
    cv2.drawContours(img2, contours, -1, color=(0, 255, 0), thickness=5)

    final_area = 0

    for a in range(len(contours)):
        area = cv2.contourArea(contours[a])
        print(a, area)
        final_area = final_area + area

    cv2.imwrite('outline.png', img2)
    print(final_area)

    # firebaseにトータルの面積を送信
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    ###################################################################################

    input_cvdata = final_area
    ####################################################################################

    doc_ref.set({
        u'amount': f"{input_cvdata}",
    })

    # 現在取ったものの画像をfirebaseに送信
    cv2.imwrite('img_gomi.png', img_gomi)
    with open(filename2, 'rb') as f:
        blob.upload_from_file(f, content_type=content_type)

    final_name = start_name

    '''
    img_gomiは現在取った物のだけの輪郭を取った画像
    start_name = start.png
    final_name = final.png
    img = final.png
    img2 = result.png
    result.pngはグレースケール画像
    img2に輪郭を描写したのがoutline.png
    '''