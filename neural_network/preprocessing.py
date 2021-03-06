import os
import cv2
import numpy as np
from tqdm import tqdm
from pathlib import Path
import matplotlib.pyplot as plt

class Preprocessing():

    trainig_data = []
    cwd = str(Path(__file__).resolve().parent.parent)
    points_dir = cwd + "/images/images1"
    paths_dir = cwd + "/images/images2"
    directories = [points_dir, paths_dir]

    def make_trainig_data(self, img_size=64):
        self.img_size = img_size
        self.image_nr = 0

        '''
        :return: saves training data as *.npy file (list created with 2 images: points and path
        '''
        try:
            for pic in tqdm(os.listdir(self.points_dir)):
                path_points = os.path.join(self.points_dir, pic)
                path_paths = os.path.join(self.paths_dir, pic)
                img_points = cv2.imread(path_points, 0)
                img_paths = cv2.imread(path_paths, 0)
                img_points = img_points/255.0
                img_paths = img_paths/255.0
                # img_points = cv2.resize(img_points, (self.img_size, self.img_size))
                # img_paths = cv2.resize(img_paths, (self.img_size, self.img_size))
                self.trainig_data.append([np.array(img_points), np.array(img_paths)])
                self.image_nr += 1

                # if self.image_nr >= 4000:
                #     break

            np.save("training_data.npy", self.trainig_data)
        except Exception as E:
            print("Exception" + str(E))


    def classify_pix(self, classes_nr, print_info):

        '''
        :param classes_nr: number of classes
        :param print_info: print information about pixel category
        :return: returns list with pixels classified to categories
        '''

        if 256 % classes_nr == 0:
            max_num = 256
            shift = round(max_num/classes_nr)
            classes = np.zeros(classes_nr, dtype=int)
            try:
                for pic in tqdm(os.listdir(self.paths_dir)):
                    path_paths = os.path.join(self.paths_dir, pic)
                    img_paths = cv2.imread(path_paths, 0)
                    for i in range(img_paths.shape[0]):
                        for j in range(img_paths.shape[1]):
                            pix_range = 0
                            for k in range(classes_nr):
                                if pix_range <= img_paths[i][j] <= (shift - 1) + pix_range:
                                    classes[k] = classes[k] + 1
                                    if print_info:
                                        print(f"IMAGE: {pic}")
                                        print(f"PIXEL: {[i], [j]}")
                                        print(f"PIXEL RANGE: {pix_range} <= pix <= {pix_range + shift - 1}")
                                        print(f"CLASS NUMBER: {k}")
                                    break
                                else:
                                    pix_range += shift

            except Exception as E:
                print("Exception" + str(E))

            return(classes)

        else:
            print("Invalid class number! 256 % numer_of_classes != 0")




training_data = Preprocessing()
print(training_data.points_dir)
print(training_data.paths_dir)
training_data.make_trainig_data()
# classes = training_data.classify_pix(2, print_info=False)
# print(classes)

training_data = np.load("training_data.npy")
print("Liczba probek: ", len(training_data))
print("Rozmiar: ", training_data.shape)

plt.figure()
plt.subplot(121)
plt.imshow(training_data[0][0], cmap='gray')

plt.subplot(122)
plt.imshow(training_data[0][1], cmap='gray')
# plt.savefig('nn_output.png')
show = plt.show()
