import matplotlib.pyplot as plt

#width, height, dpi, size, image_name


#Code for height vs Image Name
old_width = []
new_width = []
image_names = []
with open("properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        image_names.append(data[4])
        old_width.append(int(data[0]))

with open("new_properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        new_width.append(int(data[0]))

#old_width = old_width[5:20]
#image_names = image_names[5:20]
#new_width = new_width[5:20]

plt.plot(image_names, old_width, "r-", label = "Old Height")
plt.plot(image_names, new_width, "b-", label = "New Height")
plt.xlabel("Image")
plt.ylabel("width")
plt.title("width vs Image")
plt.legend()
plt.xticks(range(0, len(image_names)+1, 3))
plt.yticks(range(0, max(max(new_width), max(old_width)), 350))
plt.show()
