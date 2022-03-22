
Created on Fri Nov 12 141352 2021

@author Jason



import os
from spectral.io import envi
import spectral 
import cv2
import numpy as np

os.chdir(r'H20211112_111115_ref')

# img = envi.open(20211112_111115_ref.hdr,20211112_111115_ref.dat)


def Sobel1(matrix)
    matrix = np.array(matrix)
    x = cv2.Sobel(matrix,cv2.CV_16S,1,0)
    y = cv2.Sobel(matrix,cv2.CV_16S,0,1)
    absX = cv2.convertScaleAbs(x)   # 转回uint8
    absY = cv2.convertScaleAbs(y)      
    dst = cv2.addWeighted(absX,0.5,absY,0.5,0)
    return dst

def Hyper_spectral(hdr,dat)
    
    hdr_name = str(hdr)
    dat_name = str(dat)
    
    img = envi.open(hdr_name, dat_name)
    
    print(img.__class__)
    print(img)
    
    arr = img.load()
    arr.__class__
    # print (arr.info())
    print(arr.shape)  #608 x968 x299
    
    B  = arr[,,44] #blue 488
    G  = arr[,,75] #green 550
    R  = arr[,,123] #red 646
    
    B1 =cv2.normalize(B,None,0,255,cv2.NORM_MINMAX)
    G1 =cv2.normalize(G,None,0,255,cv2.NORM_MINMAX)
    R1 =cv2.normalize(R,None,0,255,cv2.NORM_MINMAX) #float32

    #灰度 g = pR+qG+tB
    p =0.2898; q=0.5870; t =0.1140
    g = pR1 + qG1 + tB1
    g = B1 + G1 + R1
    
    BB = (g-(pR1 + qG1))t 
    GG = (g-(pR1 + tB1))q 
    RR = (g-(qG1 + tB1))p
    
    return B1,G1,R1

#%%

B,G,R = Hyper_spectral(20211112_111115_ref.hdr,20211112_111115_ref.dat)

s1 = Sobel1(B) #-uint8
s2 = Sobel1(G)
s3 = Sobel1(R)

cv2.imshow('B',B.astype(uint8))
cv2.imshow('G',G.astype(uint8))
cv2.imshow('R',R.astype(uint8))


cv2.imshow('s1',s1)
cv2.imshow('s2',s2)
cv2.imshow('s3',s3)
    
    # plt.imshow(dst,cmap = 'gray')

zero = np.zeros([608, 968])
z255 =np.zeros([608, 968])
z255.fill(255)

ss1 = s1.reshape(608, 968,1)
ss2 = s1.reshape(608, 968,1)
ss3 = s1.reshape(608, 968,1)

ss1[,,0] = z255
ss2[,,0] = zero
ss3[,,0] = zero

RGB_img = np.zeros([608, 968, 3], np.uint8)
RGB_img[, , 0] = ss1
RGB_img[, , 1] = ss2
RGB_img[, , 2] = ss3



#要先做二值化 效果比較差
ret, thresh = cv2.threshold(B.astype(uint8), 127, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(B.astype(uint8),contours,-1,(1,0,0),3)
cv2.imshow(B,B.astype(uint8))



#還原成RGB影像
RGB_img = np.zeros([608, 968, 3], np.uint8)
RGB_img[, , 0] = B
RGB_img[, , 1] = G
RGB_img[, , 2] = R
cv2.imshow('RGB_img',RGB_img)


data6 = np.zeros((608, 968, 3)).astype(uint8)
data6 = cv2.merge([B,G,R]).astype(uint8)
cv2.imshow('',data6)
