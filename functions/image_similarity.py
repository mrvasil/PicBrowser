import os
import imgcompare

def __init__(self, directory, similarity_threshold=10.0):
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    n = len(files)
    groups = [[files[0]]]

    for i in range(n-1):
        added = False
        for group in groups:
            diff_percent = imgcompare.image_diff_percent(os.path.join(directory, files[i+1]), os.path.join(directory, group[0]))
            print(diff_percent)
            print(files[i+1], group[0])
            if diff_percent <= similarity_threshold:
                group.append(files[i+1])
                added = True
                break
        if not added:
            groups.append([files[i+1]])

    print(groups)


# compare_all_images('uploads\--')








# import imgcompare

# image1 = ''
# image2 = ''

# difference = imgcompare.image_diff_percent(image1, image2)
# if difference == 0:
#     print("The images are identical.")
# else:
#     print(f"The images are {difference}% different.")