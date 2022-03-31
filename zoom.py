# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 14:29:14 2022

@author: Jason

選取特定的波段，並且將特定波段放大，再將前後波段做疊加平均，並展現出影像

"""
import os
from spectral.io import envi
import spectral 
import cv2
from PIL import Image 
# os.chdir(r'C:\Users\Jason\Documents\HinaLea\SDKtest\bin\processed\20200521_101240')

spectral.settings.envi_support_nonlowercase_params ='TRUE'

#光譜將具有CxB形狀，其中C是庫中的光譜數，B是每個光譜的譜帶數。

os.chdir(r"H:\臺大醫院測試\第14次量測\20220331\540標準")

img = envi.open("540標準.hdr", "540標準.dat")

print(img.__class__)
print(img)
print('===================================')

arr = img.load()
arr.__class__
print (arr.info())
print(arr.shape)  #608 x968 x299



#%%

#所取波段設定
a = 94
b = 95

#畫出580的圖像
arr1 = arr.copy()


plt.figure()
plt.imshow(arr1[:,:,70])

plt.figure()
plt.imshow(arr1[:,:,90])

arr1[:,:,90].mean()
arr1[:,:,90].max()

#%% 小於mean的都等於0
zzz= np.where(arr1[:,:,90] <= arr1[:,:,90].mean())

for i in range(len(zzz[0])):
    arr1[zzz[0][i],zzz[1][i],90] = 0

#%% 數據處理
zzz1 = np.where(arr1[:,:,95] >= 0.1)

for i in range(len(zzz1[0])):
    arr1[zzz1[0][i],zzz1[1][i],95]*1

# zzz1 = np.where(arr1[:,:,95] <= 0.1)
# for i in range(len(zzz1[0])):
#     arr1[zzz1[0][i],zzz1[1][i],95] =0

arr1[:,:,95] = (arr1[:,:,95]/arr1[:,:,95].max())*200

#%%
plt.imshow(arr1[:,:,90],cmap ="gray")

image = Image.fromarray(np.uint8(cm.plasma(arr1[:,:,94])*255))
image.show()

plt.figure()
plt.imshow(arr1[:,:,95])
np.where(arr1[:,:,95] == arr1[:,:,95].max())

#畫出570~595的圖像
data = arr1[:,:,a:b]
data_sum = data.sum(axis = 2)
plt.figure()
plt.imshow(data_sum)

image = Image.fromarray(np.uint8(cm.plasma(data_sum)*255))
image.show()

#%%

plt.figure()
a540 = arr1[:,:,70]
subplot(1,2,1)
plt.imshow(a540,cmap ="gray")

a580 = arr1[:,:,90]
subplot(1,2,2)
plt.imshow(a580)


plt.figure()
img1 = np.zeros([608,968, 3], np.uint8)
a580 = (a580/a580.max())*255
# img1[:,:,0] = a580.astype('uint8')
img1[:,:,1] = a580.astype('uint8')
# img1[:,:,2] = a580.astype('uint8')
subplot(2,2,1)
plt.imshow(img1)

img = np.zeros([608,968, 3], np.uint8)
a540 = (a540/a540.max())*255
img[:,:,0] = a540.astype('uint8')
img[:,:,1] = a540.astype('uint8')
img[:,:,2] = a540.astype('uint8')
subplot(2,2,2)
plt.imshow(img)


plt.figure()
plt.imshow(img+ img1)

#%%
z = np.where(a580 == a580.max())



