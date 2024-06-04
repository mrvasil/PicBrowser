import imgcompare

image1 = ''
image2 = ''

difference = imgcompare.image_diff_percent(image1, image2)
if difference == 0:
    print("The images are identical.")
else:
    print(f"The images are {difference}% different.")