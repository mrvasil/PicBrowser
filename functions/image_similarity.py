import os
import imgcompare

def groups_of_similar_images(user_code, similarity_threshold=17.0):
    directory = os.path.join('uploads', user_code)
    files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    n = len(files)
    groups = [[files[0]]]

    for file in files[1:]:
        added = False
        for group in groups:
            diff_percent = imgcompare.image_diff_percent(os.path.join(directory, file), os.path.join(directory, group[-1]))

            print(diff_percent, file, group[-1])
            if diff_percent <= similarity_threshold:
                group.append(file)
                added = True
                break
        if not added:
            groups.append([file])
    
    return groups
    # for index, group in enumerate(groups):
    #     print(f"Группа {index + 1}:")
    #     for image in group:
    #         print(image)
    

# __init__(os.path.join('uploads', 'd33be525-da6b-4842-aa52-a95b828dfa3d'))








# import imgcompare

# image1 = ''
# image2 = ''

# difference = imgcompare.image_diff_percent(image1, image2)
# if difference == 0:
#     print("The images are identical.")
# else:
#     print(f"The images are {difference}% different.")