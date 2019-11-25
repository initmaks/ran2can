# Credits for the Psycodelice background generator 
# https://github.com/j2kun/random-art
import random, math
import cv2
from PIL import Image
import numpy as np
from skimage.draw import random_shapes

class X:
    def eval(self, x, y):
        return x
   
    def __str__(self):
        return "x"

class Y:
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"

class SinPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x,y))

class CosPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
          return math.cos(math.pi * self.arg.eval(x,y))

class Times:
    def __init__(self, prob):
        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def __str__(self):
        return str(self.lhs) + "*" + str(self.rhs)

    def eval(self, x, y):
        return self.lhs.eval(x,y) * self.rhs.eval(x,y)

def buildExpr(prob = 0.99):
    if random.random() < prob:
        return random.choice([SinPi, CosPi, Times])(prob)
    else:
        return random.choice([X, Y])()

def plotIntensity(exp, pixelsPerUnit = 150):
    canvasWidth = 2 * pixelsPerUnit
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsPerUnit) / pixelsPerUnit 
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            z = exp.eval(x,y)

            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            canvas.putpixel((px,py), intensity)

    return canvas

def plotColor(redExp, greenExp, blueExp, pixelsPerUnit = 150):
    redPlane   = plotIntensity(redExp, pixelsPerUnit)
    greenPlane = plotIntensity(greenExp, pixelsPerUnit)
    bluePlane  = plotIntensity(blueExp, pixelsPerUnit)
    return Image.merge("RGB", (redPlane, greenPlane, bluePlane))

def makeImage(image_half_width = 150):
    redExp = buildExpr()
    greenExp = buildExpr()
    blueExp = buildExpr()

    image = plotColor(redExp, greenExp, blueExp, image_half_width)
    return image

### DATASET_V1

def get_random_image(image_dim = 256, color_channels = 3, max_shapes=16, min_shapes = 1):
    assert image_dim % 2 == 0 # should be even
    image_size = (image_dim, image_dim)
    # generate image with random shapes
    clean_bg_image, _ = random_shapes(image_shape = image_size, 
                                  max_shapes=max_shapes,
                                  min_shapes=min_shapes,
                                  min_size = image_size[0]/10,
                                  max_size=image_size[0]/2,
                                  num_channels=color_channels,
                                  shape=None, #  {rectangle, circle, triangle, None}
                                  intensity_range=None, 
                                  allow_overlap=False, # TODO 
                                  num_trials=100, 
                                  random_seed=None # TODO
                                 )

    random_bg_image = np.array(makeImage(image_dim//2)) # create a random background
    random_bg_image[clean_bg_image!=255] = clean_bg_image[clean_bg_image!=255] # merge background and random shapes
    return random_bg_image, clean_bg_image

### DATASET_V2

def draw_rect(im, x, y, w, h, angle, color):
    rect = ((x - (np.sin(np.deg2rad(angle)) * h)/2,
             y + (np.cos(np.deg2rad(angle)) * h)/2
            )
            , (w, h), angle)
    box = cv2.boxPoints(rect)
    cv2.drawContours(im,[np.int0(box)],0,color,-1)
    return im

def generate_arm(img_dim = 512): # ROBOTIC ARM SILHOUETTE GENERATION SCRIP
    im = np.zeros((img_dim,img_dim,3))
    # base
    base_x = np.random.randint(50,450)
    base_y = np.random.randint(200,400)
    im = draw_rect(im, x = base_x, y = base_y, w = 140, h = 60, angle = 0, color = (255,0,0))

    # j1
    j1_angle = np.random.randint(150,210)
    j1_len = 140
    j1_x = base_x 
    j1_y = base_y + 10
    im = draw_rect(im, x = j1_x, y = j1_y, w = 30, h = j1_len, angle = j1_angle, color = (0,255,0))
    im = cv2.circle(im, (j1_x, j1_y), radius = 30, color = (255,255,0), thickness = - 1)

    # j2
    j2_angle = np.random.randint(45,315)
    j2_len = 100
    j2_x = int(j1_x - np.sin(np.deg2rad(j1_angle)) * j1_len)
    j2_y = int(j1_y + np.cos(np.deg2rad(j1_angle)) * j1_len)
    im = draw_rect(im, x = j2_x, y = j2_y, w = 25, h = j2_len, angle = j2_angle, color = (0,0,255))
    im = cv2.circle(im, (j2_x, j2_y), radius = 25, color = (0,255,255), thickness = - 1)

    # j3
    j3_angle = np.random.randint(0,360)
    j3_len = 100
    j3_x = int(j2_x - np.sin(np.deg2rad(j2_angle)) * j2_len) 
    j3_y = int(j2_y + np.cos(np.deg2rad(j2_angle)) * j2_len)
    im = draw_rect(im, x = j3_x, y = j3_y, w = 23, h = j3_len, angle = j3_angle, color = (255,0,255))
    im = cv2.circle(im, (j3_x, j3_y), radius = 23, color = (128,25,128), thickness = - 1)
    im = np.uint16(im)
    return im


def get_random_image_v2(image_dim = 256, color_channels = 3, max_shapes=16, min_shapes = 1):
    image_in, image_out = get_random_image(image_dim, color_channels, max_shapes, min_shapes)
    canonical_arm = generate_arm(image_dim)
    im = np.copy(canonical_arm)
    if np.random.rand() < 0.5:
        # apply texture to whole arm
        ### trim the 2d edges ###
        gray = im.sum(axis=-1)
        y_idx = np.where(np.sum(gray,axis=0) != 0)[0]
        y_min, y_max = y_idx.min(), y_idx.max()
        x_idx = np.where(np.sum(gray,axis=1) != 0)[0]
        x_min, x_max = x_idx.min(), x_idx.max()
        arm = im[x_min:x_max,y_min:y_max,:]
        ### END : trim ###
        texture_dim = max((x_max - x_min),(y_max - y_min)) + 1
        arm_mask_cropped = np.any(arm != [0,0,0], axis=2)

        texture = np.array(makeImage(texture_dim//2))
        texture = texture[:arm.shape[0],:arm.shape[1],:]
        arm[arm_mask_cropped] = texture[arm_mask_cropped]
        im[x_min:x_max,y_min:y_max,:][np.any(arm!=[0,0,0],axis=2)] = arm[np.any(arm!=[0,0,0],axis=2)]
    else:
        # apply texture to each part separately
        for color in np.unique(im.reshape(-1, im.shape[2]), axis=0):
            if np.all(color == [0,0,0]): continue #skip background
            masked_im = np.copy(im)
            masked_im[np.any(im != color, axis=2)] = 0 # select only the part of interest 
            ### trim the 2d edges ###
            gray = masked_im.sum(axis=-1) 
            y_idx = np.where(np.sum(gray,axis=0) != 0)[0]
            y_min, y_max = y_idx.min(), y_idx.max()
            x_idx = np.where(np.sum(gray,axis=1) != 0)[0]
            x_min, x_max = x_idx.min(), x_idx.max()
            part = masked_im[x_min:x_max,y_min:y_max,:]
            ### END : trim ###
            texture_dim = max((x_max - x_min),(y_max - y_min)) + 1 # the image size for new texture

            part_mask_cropped = np.any(part != [0,0,0], axis=2) # binaty mask of the cropped part

            texture = np.array(makeImage(texture_dim//2)) # texture generation
            texture = texture[:part.shape[0],:part.shape[1],:] # adjusting the dimension for masking
            part[part_mask_cropped] = texture[part_mask_cropped] # replace the part with the texture
            # apply the texture inpace on the whole image
            im[x_min:x_max,y_min:y_max,:][np.any(part!=[0,0,0],axis=2)] = part[np.any(part!=[0,0,0],axis=2)] 

    # attach canonical arm over the clear background image
    image_out[np.any(canonical_arm != [0,0,0],axis=2)] = canonical_arm[np.any(canonical_arm != [0,0,0],axis=2)]
    # attach texturized arm over the textured background image
    image_in[np.any(im != [0,0,0],axis=2)] = im[np.any(im != [0,0,0],axis=2)]
    
    return image_in, image_out