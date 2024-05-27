import imgcompare

image1 = 'WIN_20240527_13_57_15_Pro.jpg'
image2 = 'WIN_20240527_14_02_55_Pro.jpg'

# Compare the two images
if imgcompare.is_equal(image1, image2):
    print("The images are identical.")
else:
    difference = imgcompare.image_diff_percent(image1, image2)
    print(f"The images are {difference}% different.")
