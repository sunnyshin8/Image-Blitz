import matplotlib.pyplot as plt

#width, height, dpi, size, image_name


#Code for height vs Image Name
old_heights = []
new_heights = []
image_names = []
with open("properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        image_names.append(data[4])
        old_heights.append(int(data[1]))

with open("new_properties.txt", "r") as f:
    for line in f:
        data = line.strip().split(",")
        new_heights.append(int(data[1]))

#old_heights = old_heights[5:20]
#image_names = image_names[5:20]
#new_heights = new_heights[5:20]

plt.plot(image_names, old_heights, "r-", label = "Old Height")
plt.plot(image_names, new_heights, "b-", label = "New Height")
plt.xlabel("Image")
plt.ylabel("Heights")
plt.title("Heights vs Image")
plt.legend()
plt.xticks(range(0, len(image_names)+1, 3))
plt.yticks(range(0, max(max(new_heights), max(old_heights)), 350))
plt.show()
