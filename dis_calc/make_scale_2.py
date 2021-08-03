import matplotlib.pyplot as plt
import sys

is_abs_risk = "f"

abs_perc = float(str(sys.argv[1]))
perc_str = str("{:.2f}".format(abs_perc))
if(is_abs_risk == "t"):
    perc_str = perc_str + "%"
else:
    perc_str = " " + perc_str
if(len(perc_str) < 5):
    perc_str = " " + perc_str
#img = plt.imread("scale_empty.png")
fig, ax = plt.subplots()
img = plt.imread("out_temp_2.png")
plt.axis('off')
#print(img.shape)
#img_cropped = img[200:800, 440:1400, :]
#img_cropped = img[100:800, 300:1500, :]
img_cropped = img[500:4050, 1500:7500, :]
#img_cropped = img[200:800, 440:1300, :]

ax.imshow(img_cropped)
#plt.text(565, 650, perc_str, size=12, color='white')
plt.text(2820, 3250, perc_str, size=12, color='white')
#plt.show()
#plt.show()
#plt.savefig("output.png")
plt.margins(0,0)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

fig = plt.gcf()
fig.set_size_inches(12.0,7.0)
fig.savefig(str(sys.argv[2]), dpi=500,bbox_inches = 'tight',pad_inches = 0)
