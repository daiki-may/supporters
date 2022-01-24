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
import subprocess

from PIL import Image, ImageFilter

def find_cont(img_before, img_after):
    fgbg = cv2.createBackgroundSubtractorMOG2()

    fgmask = fgbg.apply(img_before)
    fgmask = fgbg.apply(img_after)
    #im_diff = img_before - img_after
    # print(im_diff)
    #fgmask = np.abs(im_diff)
    # cv2.imshow("bin_img", fgmask)
    # cv2.waitKey(0)
    # fgmask = np.abs(im_diff)
    # cv2.imwrite("fgmask.png",fgmask)
    # fgmask = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)

    # グレースケール化
    #gray = cv2.cvtColor(fgmask, cv2.COLOR_BGR2GRAY)

    _, img_bin = cv2.threshold(fgmask, 0, 255, cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    img_bin = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("bin_img",bin_img)
    # cv2.waitKey(0)
    cv2.imwrite("img_bin.png",img_bin)


    # 輪郭抽出
    tmp_contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return tmp_contours

def result_img(count_gomi):
    img_list = [Image.open('gomi_{}.png'.format(i+1)) for i in range(count_gomi)]
    # print(img_list)
    img_width = [i.size[0] for i in img_list]
    img_height = [i.size[1] for i in img_list]

    img_height_result = max(img_height)+200
    img_width_result = sum(img_width)+100*count_gomi+100


    bg = Image.new("RGBA", (img_width_result, img_height_result), (255, 255, 255, 0))

    tmp_width = 0
    for i, im in enumerate(img_list):
        bg.paste(im, (int(100+tmp_width), int((img_height_result-im.size[1])/2)))
        tmp_width = tmp_width + im.size[0] + 100

    bg.save("result_img.png")

if __name__ == '__main__':
    cred = credentials.Certificate(
        "gikucamp-firebase-adminsdk-bw43u-3c588aa9ee.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'gikucamp.appspot.com'})
    db = firestore.client()
    doc_ref = db.collection(u'data').document(u'90TwVL13wTuPpmCgw24C')
    ref = db.collection(u'data')
    docs = ref.stream()
    bucket = storage.bucket()
    #filename = 'outline.png'
    #blob = bucket.blob(filename)
    content_type = 'outline/png'

    #filename2 = 'img_gomi.png'
    filename2 = 'img_gomi.png'
    blob = bucket.blob(filename2)


    area_total_previous = 0
    area_total = 0
    count_gomi = 0
    hp_max = 0
    count_gomi = 0

    camera = cv2.VideoCapture(0)
    for i in range(1, 600):
        # if area_total > hp_max:
        #     hp_max = area_total
        ret, frame = camera.read()
        if ret:
            print('Success')
            cv2.imwrite('final{}.png'.format(i), frame)

        else:
            print('Failed')

        # start_name = 'final{}.png'.format(i-1)
        # final_name = 'final{}.png'.format(i)
        img_before = cv2.imread('final{}.png'.format(i-1))
        img_after = cv2.imread('final{}.png'.format(i))

        cont_n = find_cont(img_before, img_after)
        #print("contours", contours)

        # 輪郭を描写
        img_outline = img_after.copy()
        cv2.drawContours(img_outline, cont_n, -1, color=(0, 255, 0), thickness=5)
        cv2.imwrite('outline.png', img_outline)

        # for i in cont_n:
        #     print(cv2.contourArea(i))

        # 小さい輪郭を削除
        cont_A = list(filter(lambda x: cv2.contourArea(x) > 20000, cont_n))
        # print("contours-", cont_n)

        # 輪郭を描写
        # img_outline = img2.copy()
        cv2.drawContours(img_outline, cont_A, -1, color=(0, 255, 0), thickness=5)
        cv2.imwrite('outline_.png', img_outline)
        final_area = 0
        # cv2.imshow("img_outline",img_after)
        # cv2.waitKey()

        # トータルエリアを計算

        img_0 = cv2.imread('final0.png')
        cont_0 = find_cont(img_0, img_after)
        cont_0A = list(filter(lambda x: cv2.contourArea(x) > 10000, cont_0))

        area_total_previous = area_total
        area_total = sum([cv2.contourArea(i) for i in cont_0A])

        for a in range(len(cont_A)):
            area = cv2.contourArea(cont_A[a])
            print(a, area)
            final_area = final_area + area


        print("final_area", final_area)
        print("area_total", area_total)
        print("area_total_previous", area_total_previous)

        final_area = area_total



        try:
            if area_total < area_total_previous:
                count_gomi = count_gomi+1
                # 外形のマスク画像を生成
                mask = np.zeros_like(img_before[:, :, 0])
                cv2.drawContours(mask, [cont_A[0]], -1, color=255, thickness=-1)
                #if(area_diff>0):
                ch_b, ch_g, ch_r = cv2.split(img_before[:, :, :3])
                img_alpha = cv2.merge((ch_b, ch_g, ch_r, mask))
                cv2.imwrite("img_alpha.png", img_alpha)

                # 外枠の矩形を計算
                x, y, w, h = cv2.boundingRect(cont_A[0])
                img_gomi = img_alpha[y:y + h, x:x + w]
                cv2.imwrite("img_gomi.png", img_gomi)

                # 現在取ったものの画像をfirebaseに送信

                with open(filename2, 'rb') as f:
                    blob.upload_from_file(f, content_type=content_type)

                gomi_path ='gomi_{}.png'.format(count_gomi)
                cv2.imwrite(gomi_path, img_gomi)

                blob_gomi_path = bucket.blob(gomi_path)
                with open(gomi_path, 'rb') as f:
                    blob_gomi_path.upload_from_file(f, content_type=content_type)



        except IndexError:
            print('Not found: gomi')

        # firebaseにトータルの面積を送信
        for doc in docs:
            print(u'{} => {}'.format(doc.id, doc.to_dict()))

        if final_area > hp_max:
            hp_max = area_total

        doc_ref.set({
            u'amount': f"{final_area}",
            u'count_gomi': f"{count_gomi}",
            u'hp_max': f"{hp_max}",
            u'hp_diff': f"{area_total - area_total_previous}",

        })
        if area_total == 0:
            result_path = "result_img.png"
            result_img(count_gomi)
            blob_result_path = bucket.blob(result_path)
            with open(result_path, 'rb') as f:
                blob_result_path.upload_from_file(f, content_type=content_type)

            hp_max = 0
            count_gomi = 0


        print("今置け！")
        #cv2.waitKey(0)
        #input()
        #subprocess.call('PAUSE', shell=True)
        var = input("Please input variable : ")
        print("Input variable is : {}".format(var))


    ''' 
    img_gomiは現在取った物のだけの輪郭を取った画像
    start_name = start.png
    final_name = final.png
    img = final.png
    img2 = result.png
    result.pngはグレースケール画像
    img2に輪郭を描写したのがoutline.png
    '''
