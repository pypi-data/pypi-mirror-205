import torch
import cv2
import numpy as np
 
class HazeGen:
    def __init__(self, depth_quality,level):
        self.depth_quality = depth_quality
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.midas, self.midas_transform = self.initialize_midas()
        self.density = level

    def initialize_midas(self):
        model_type = self.get_model_type(self.depth_quality)
        midas = torch.hub.load("intel-isl/MiDaS", model_type)
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        midas.to(self.device)
        midas.eval()

        if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
            midas_transform_ = midas_transforms.dpt_transform
        else: 
            midas_transform_ = midas_transforms.small_transform

        return midas, midas_transform_
    
    def predict_depth(self, image):
        img_input = self.midas_transform(image).to(self.device)
        with torch.no_grad():
          prediction = self.midas(img_input)

          prediction = torch.nn.functional.interpolate(
              prediction.unsqueeze(1),
              size=image.shape[:2],
              mode="bicubic",
              align_corners=False,
          ).squeeze()
        invert_depth_map =  torch.max(prediction) - prediction
        output = invert_depth_map.cpu().numpy()        
        return output

    def get_model_type(self,quality_level):
        if quality_level == "low":
            return "MiDaS_small"
        elif quality_level == "high":
            return "DPT_Large"
        elif quality_level == "medium":
            return "DPT_Hybrid"
        else:
            print("Invalid quality level. Setting default to 'DPT_Hybrid'")
            return "DPT_Hybrid"
        
    def generate_haze(self, clean_image, beta):
        KERNAL_SIZE = 15
        if clean_image.shape[0] == 1:
            clean_image = np.concatenate(
                (clean_image, clean_image, clean_image), axis=0)

        dark_channel, _ = self.get_dark_channel(clean_image,KERNAL_SIZE)

        atm_light,_,_ = self.estimate_atmospheric_light_rf(dark_channel, clean_image)
        normalize_depthmap = self.normalize_image(depth_map)
        trans = np.exp(-normalize_depthmap * beta) 
        atm_light = atm_light.reshape(3)
        clean_image = self.normalize_image(clean_image)
        atm_light = atm_light/255
        hazy_tensor = clean_image * trans + atm_light * (1 - trans)
        img_pil = Image.fromarray(np.uint8(hazy_tensor*255))

        return img_pil

    def normalize_image(self,img):
        return (img - img.min()) / (img.max() - img.min())

    def erosion(x, m=1):
        b, c, h, w = x.shape
        x_pad = F.pad(x, pad=[m, m, m, m], mode='constant', value=1e9)
        channel = F.unfold(x_pad, 2 * m + 1, padding=0,
                        stride=1).view(b, c, -1, h, w)
        result = torch.min(channel, dim=2)[0]
        return result


    def get_dark_channel(self,I, neighborhood_size):
        # Define a square structuring element
        se = cv2.getStructuringElement(
            cv2.MORPH_RECT, (neighborhood_size, neighborhood_size))

        # Perform erosion operation
        I_eroded = cv2.erode(I, se)

        # Compute the minimum intensity value over the third dimension (color channels)
        I_dark = I_eroded.min(axis=2)

        return I_dark, I_eroded


    def estimate_atmospheric_light_rf(self,I_dark, I):
        # Determine the number of brightest pixels in the dark channel to be used for estimating atmospheric light
        brightest_pixels_fraction = 1 / 1000
        number_of_pixels = I_dark.size
        brightest_pixels_count = int(
            np.round(number_of_pixels * brightest_pixels_fraction))
        brightest_pixels_count = brightest_pixels_count + \
            1 if brightest_pixels_count % 2 == 0 else brightest_pixels_count

        # Find indices of the brightest pixels in the dark channel
        I_dark_vector = I_dark.flatten()
        indices = np.argsort(I_dark_vector)[::-1]
        brightest_pixels_indices = indices[:brightest_pixels_count]

        # Find the graylevel intensities of the brightest pixels in the original image
        I_gray_vector = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY).flatten()
        I_gray_vector_brightest_pixels = I_gray_vector[brightest_pixels_indices]

        # Determine the atmospheric light as the pixel with median graylevel intensity among the brightest pixels
        median_intensity = np.median(I_gray_vector_brightest_pixels)
        index_median_intensity = np.where(
            I_gray_vector_brightest_pixels == median_intensity)[0][0]
        index_L = brightest_pixels_indices[index_median_intensity]

        row_L, column_L = np.unravel_index(index_L, I_dark.shape)

        L = I[row_L, column_L, :]
        atm_light = np.mean(L)
        atm_light = np.array([atm_light, atm_light, atm_light])
        return atm_light
      
    def add_haze(self, clean_image, level=None, kernel_size=15):
        if level is None:
            level = self.density
        if clean_image.shape[0] == 1:
            clean_image = torch.cat((clean_image, clean_image, clean_image), dim=0)
      
        dark_channel, _ = self.get_dark_channel(clean_image,15)
        atm_light = self.estimate_atmospheric_light_rf(dark_channel, clean_image)
        depth_map = self.predict_depth(clean_image)
        depth_img_3c = np.zeros_like(clean_image).astype(np.float32)
        depth_img_3c[:,:,0] = depth_map
        depth_img_3c[:,:,1] = depth_map
        depth_img_3c[:,:,2] = depth_map

        norm_depth_img = self.normalize_image(depth_img_3c)

        trans = np.exp(-norm_depth_img * level) 

        clean_image = self.normalize_image(clean_image)
        atm_light = atm_light/255
        hazy = clean_image * trans + atm_light * (1 - trans)

        return hazy



