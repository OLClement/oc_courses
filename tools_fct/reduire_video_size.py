import imageio
import PIL
from PIL import Image
import numpy as np
import pandas as pd

# Parametres de compression
width, height = 128,72
img_freq = 90

# Import de la video
filename = 'ACP.mp4'
images_per_seconds = 30 # La video : 30 images par secondes
url = "https://youtu.be/uV5hmpzmWsU"
vid = imageio.get_reader(filename,  'ffmpeg')
sample = np.arange(0, vid.get_length(), img_freq)

# Extraction des informations
first_frame = vid.get_data(0)
image_height, image_width, colors = first_frame.shape
print(image_height,image_width,vid.get_length(),colors)
print(image_height * image_width * vid.get_length() * colors)

# Extraction des images
video = np.zeros((0, width*height*3), dtype=np.int8)
for j,i in enumerate(sample):
    if j%5 == 0:
        print("image ",i, max(sample))
    image = vid.get_data(i)

    # Reduction de la taille des images
    img = Image.fromarray(image.astype('uint8'), 'RGB')
    img = img.resize((width,height), PIL.Image.ANTIALIAS)
    image = np.array(img)
    
    image = image.reshape(height*width*3)
    image = image / 4 #Reduction de l'echelle des couleurs (0 Ã  256 vers du 0 Ã  64)
    image = np.array(image, dtype=np.int8) # Conversion des niveaux de couleurs en int
    #display_image(image,height,width,3)
    video = np.concatenate([video,[image]])

print(video.shape)

# conversion en dataframe
video = pd.DataFrame(video)

# ajout de la position de l'image, en secondes :
video["position"] = [int(frame/images_per_seconds) for frame in sample]
# ajout de l'url qui fait demarrer la video au bon endroit
video.index = ["{}?t={}s".format(url, p) for p in video["position"]]
# inversion de l'ordre des colonnes dans le dataframe
cols = list(video.columns)
cols.pop(cols.index('position'))
video = video[['position'] + cols]

# Export CSV
video.to_csv("video.csv")