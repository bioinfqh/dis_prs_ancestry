import matplotlib.pyplot as plt
import math 
import sys
from math import pi

perc = float(str(sys.argv[1]))
score = float(str(sys.argv[2]))
if(len(sys.argv) <3):
    img = plt.imread("scale_empty.png")
elif(sys.argv[3] == "true"):
    img = plt.imread("scale_with_scores.png")
else:
    img = plt.imread("scale_empty.png")
fig, ax = plt.subplots()
ax.imshow(img)
#tangens = math.tan(pi * perc)
#print(tangens)
angle=float(180*(1.0-(score/100.0)))
#print(angle)
x2 = 925 + (500 * math.cos(math.pi * angle / 180.0))
y2 = 735 - (500 * math.sin(math.pi * angle / 180.0))
#print(x2)
#print(y2)
x_values = [925, x2]
y_values = [735, y2]
plt.plot(x_values, y_values,color='black',linewidth=4)
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.0)
plt.axis('off')
fig = plt.gcf()
fig.set_size_inches(18.0, 10.0)
fig.savefig('out_temp_2.png', dpi=500)
#plt.show()
#plt.savefig("test.png")
#plt.axline((0, 0), (1, 1))
#plt.show()
#plt.clf()
#img2 = plt.imread("test.png")
#print(img2.shape)
#img_cropped = img2[700:1200, 700:1200, :]
#ax.imshow(img2)
#plt.show()
#plt.show()
