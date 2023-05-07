import matplotlib.pyplot as plt

#width, height, dpi, size, image_name


old_dpis = []
new_dpis = []
image_names = []
with open("properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        image_names.append(data[4])
        old_dpis.append(int(data[2]))

with open("new_properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        new_dpis.append(int(data[2]))

#old_dpis = old_dpis[:20]
#image_names = image_names[:20]
#new_dpis = new_dpis[:20]

plt.plot(image_names, old_dpis, "r-", label = "Old DPI")
plt.plot(image_names, new_dpis, "b-", label = "New DPI")
plt.xlabel("Image")
plt.ylabel("DPI")
plt.title("DPI vs Image")
plt.legend()
plt.xticks(range(0, len(image_names)+1, 3))
plt.yticks(range(0, max(max(new_dpis), max(old_dpis)), 20))
plt.show()