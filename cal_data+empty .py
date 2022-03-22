# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 11:27:45 2022

@author: Jason

分別畫出有細胞的玻片 以及，空白玻片的光譜圖像並且疊加
"""
import os
from spectral.io import envi
import spectral 
# os.chdir(r'C:\Users\Jason\Documents\HinaLea\SDKtest\bin\processed\20200521_101240')

spectral.settings.envi_support_nonlowercase_params ='TRUE'

#光譜將具有CxB形狀，其中C是庫中的光譜數，B是每個光譜的譜帶數。

os.chdir(r"H:\臺大醫院測試\第9次拍攝\700\sample 700")

img = envi.open("sample 700.hdr", "sample 700.dat")

print(img.__class__)
print(img)
print('===================================')

arr = img.load()
arr.__class__
print (arr.info())
print(arr.shape)  #608 x968 x299

#%%

sample700 =[]

for i in range(0,608):
    for j in range(0,968):
        sample700.append(arr[i,j,:].reshape(299))
        

data = np.zeros(299)
for i in range(len(sample700)):
    data = data +sample700[i]

data700 = data/299
plt.plot(data700,label='data')

    
z = 70
#%%

os.chdir(r"H:\臺大醫院測試\第9次拍攝\700\empty 700")

img1 = envi.open("empty 700.hdr", "empty 700.dat")

arr1 = img1.load()

empty700 =[]

for i in range(0,608):
    for j in range(0,968):
        empty700.append(arr1[i,j,:].reshape(299))
        

data1 = np.zeros(299)
for i in range(len(empty700)):
    data1 = data1 +empty700[i]

empty700 = data1/299

plt.plot(empty700,label='empty')
plt.legend()

plt.xlabel('Number of bands')
plt.ylabel('Intensity')
plt.title('500ms')

vlines(z, 0,data700.max(),'r')

#%%

plt.figure()

index = data700/empty700

plt.plot(index)
plt.xlabel('Number of bands')
plt.ylabel('Intensity')
plt.title('500ms')

vlines(z, index.min(),index.max(),'r')

