import matplotlib.pyplot as plt
import numpy as np
import time
import os
import cv2

from PIL import Image

path = os.path.abspath(__file__)
dir = os.path.dirname(path)

image = "zebra.jpeg" 
image_path = os.path.join(dir, image)
img = Image.open(image_path)
imggray = img.convert('L')

imgmat = np.array(list(imggray.getdata(band=0)), float)
imgmat.shape = (imggray.size[1], imggray.size[0])
imgmat = np.matrix(imgmat)


U, sigma, Vt = np.linalg.svd(imgmat) 
val1 = 1
val2 = 10
val3 = 50
val4 = 400

reconstimg1 = np.matrix(U[:, :val1]) * np.diag(sigma[:val1]) * np.matrix(Vt[:val1, :])
reconstimg10 = np.matrix(U[:, :val2]) * np.diag(sigma[:val2]) * np.matrix(Vt[:val2, :])
reconstimg50 = np.matrix(U[:, :val3]) * np.diag(sigma[:val3]) * np.matrix(Vt[:val3, :])
reconstimg200 = np.matrix(U[:, :val4]) * np.diag(sigma[:val4]) * np.matrix(Vt[:val4, :])

size1 = round(((img.width + val1 + img.height) / (img.width * img.height)) * 100, 2)
size2 = round((((img.width * val2) + val2 + (img.height * val2)) / (img.width * img.height)) * 100, 2)
size3 = round((((img.width * val3) + val3 + (img.height * val3)) / (img.width * img.height)) * 100, 2)
size4 = round((((img.width * val4) + val4 + (img.height * val4)) / (img.width * img.height)) * 100, 2)

res = cv2.absdiff(imgmat, reconstimg200)
res = res.astype(np.uint8)
percentage = (np.count_nonzero(res) * 100)/ res.size
print(percentage) #percent loss


plt.figure(figsize=(9, 6))

plt.subplot(1, 5, 1)
plt.imshow(imgmat, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 5, 2)  
plt.imshow(reconstimg1, cmap='gray')
plt.title("1 SV: {}% size".format(size1))
plt.axis('off')

plt.subplot(1, 5, 3) 
plt.imshow(reconstimg10, cmap='gray')
plt.title("10 SV: {}% size".format(size2))
plt.axis('off')

plt.subplot(1, 5, 4) 
plt.imshow(reconstimg50, cmap='gray')
plt.title("50 SV: {}% size".format(size3))
plt.axis('off')

plt.subplot(1, 5, 5)  
plt.imshow(reconstimg200, cmap='gray')
plt.title("400 SV: {}% size".format(size4))
plt.axis('off')

plt.tight_layout() 
plt.show()
