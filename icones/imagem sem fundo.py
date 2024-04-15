from PIL import Image 
import numpy as np

 


Image.MAX_IMAGE_PIXELS = None  # desativa o limite de tamanho máximo de imagem

# Abre a imagem TIFF
img_tiff = Image.open('seta esquerda.jpg')

# Converte a imagem em uma matriz numpy com 4 canais (R, G, B, A)
img_array = np.array(img_tiff.convert('RGBA'))

# Define o valor inicial do canal alfa para 255 (totalmente opaco) para todos os pixels
img_array[:, :, 3] = 255

# Encontra os pixels brancos e os transforma em transparentes
white_pixels = (img_array[:,:,0] > 120) & (img_array[:,:,1] > 120) & (img_array[:,:,2] > 120)
img_array[white_pixels, 3] = 0


# Converte a matriz numpy de volta para uma imagem PIL
img_pil=Image.fromarray(img_array)


#img_tiff=img_tiff.resize((64,64))
img_pil.save("seta esquerda n.png")
print("foi")
