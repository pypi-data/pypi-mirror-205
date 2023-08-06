'''
Author: Yorai Shaoul
Date: 2023-02-05

Example script for creating a Pytorch dataset using the TartanAir dataset toolbox.
'''

# General imports.
import sys
import cv2
import numpy as np
import torch
from torchvision.transforms import ToTensor, Compose
from scipy.spatial.transform import Rotation

from tartanair.image_resampling.image_sampler.six_images import SixPlanarTorch
from tartanair.image_resampling.mvs_utils.shape_struct import ShapeStruct


# Local imports.
sys.path.append('..')
import tartanair as ta

# Image sampling imports.
from tartanair.image_resampling.mvs_utils.camera_models import LinearSphere
from tartanair.image_resampling.image_sampler.six_images_py_numba import SixPlanarNumba

# Create a TartanAir object.
tartanair_data_root = '/media/yoraish/overflow/data/tartanair-v2'
ta.init(tartanair_data_root)

#####################
# Using a dataloader #
#####################

# Set up the dataset.
transform = Compose([
    ToTensor(),
])
dataset = ta.create_image_dataset(env = ['OldScandinaviaExposure'], difficulty = ['easy'], trajectory_id = ['P003'], modality = ['image', 'depth'], camera_name = ['lcam_front', 'lcam_back', 'lcam_right', 'lcam_left', 'lcam_top', 'lcam_bottom'], transform = transform, num_workers=10)





def render_batch_to_fov(sample_batched, fov, R_raw_fisheye = np.eye(3)):

    # Show the batch side by side.
    import cv2
    import numpy as np
    imgs1 = sample_batched['lcam_front']['image_0'].numpy()
    imgs2 = sample_batched['lcam_front']['image_1'].numpy()

    # Create a camera model.
    camera_model = LinearSphere(fov_degree = fov, shape_struct=ShapeStruct(512, 512))

    # Create a sampler.

    # Create the image dict.
    image_dict = {}
    image_dict['front'] = imgs1[0, 0, :, :]
    image_dict['back'] = imgs1[0, 1, :, :]



    fisheye_sampler = SixPlanarTorch( 180,
                                        camera_model,
                                        R_raw_fisheye = torch.tensor(R_raw_fisheye).float() ,
                                        convert_output = False)  
      
    fisheye_sampler.device = 'cuda'
    image_dicts = [{
                        'front': sample_batched["lcam_front"]['image_0'][b],
                        'left': sample_batched["lcam_left"]['image_0'][b],
                        'right': sample_batched["lcam_right"]['image_0'][b],
                        'back': sample_batched["lcam_back"]['image_0'][b],
                        'top': sample_batched["lcam_top"]['image_0'][b],
                        'bottom': sample_batched["lcam_bottom"]['image_0'][b]
                    } for b in range (sample_batched["lcam_front"]['image_0'].shape[0])]
    
    fish0, valid_mask_fish0 = fisheye_sampler(image_dicts, invalid_pixel_value=0, interpolation='linear')
    return fish0
    

# Create a torch dataloader.
import torch
from torch.utils.data import Dataset, DataLoader

dataloader = DataLoader(dataset, batch_size = 1, shuffle = False, num_workers = 0)

raw_iamges = []
trip_images = []

# Show a few images.
fov = 90
roll = 0
pitch = 0
yaw = 0
for i_batch, sample_batched in enumerate(dataloader):
    print(i_batch)
    if i_batch > 160:
        break

    # Widen field of view.
    if i_batch == 30:
        for f in range(25):
            fov += 4
            fish0 = render_batch_to_fov(sample_batched, fov)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )
        
        for f in range(25):
            fov -= 4
            fish0 = render_batch_to_fov(sample_batched, fov)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )

        for f in range(25):
            fov += 4
            fish0 = render_batch_to_fov(sample_batched, fov)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )


    # Rotate camera.
    if i_batch == 60:
        for _ in range(10):
            roll += 5
            R_fish_in_cube = Rotation.from_euler('xyz', [pitch, 0, roll], degrees=True).as_matrix()
            fish0 = render_batch_to_fov(sample_batched, fov, R_fish_in_cube)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )

        for _ in range(10):
            roll -= 5
            R_fish_in_cube = Rotation.from_euler('xyz', [pitch, 0, roll], degrees=True).as_matrix()
            fish0 = render_batch_to_fov(sample_batched, fov, R_fish_in_cube)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )

        for _ in range(10):
            roll += 5
            R_fish_in_cube = Rotation.from_euler('xyz', [pitch, 0, roll], degrees=True).as_matrix()
            fish0 = render_batch_to_fov(sample_batched, fov, R_fish_in_cube)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )

        for _ in range(5):
            roll -= 5
            R_fish_in_cube = Rotation.from_euler('xyz', [pitch, 0, roll], degrees=True).as_matrix()
            fish0 = render_batch_to_fov(sample_batched, fov, R_fish_in_cube)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )



    if i_batch > 60 <= 160:
            pitch -= 5
            roll += 5

            if i_batch//20 % 2 == 0:
                fov -= 5
            else:
                fov += 5

            R_fish_in_cube = Rotation.from_euler('xyz', [pitch, 0, roll], degrees=True).as_matrix()
            fish0 = render_batch_to_fov(sample_batched, fov, R_fish_in_cube)

            B = sample_batched['lcam_front']['image_0'].shape[0]
            for b in range(B):
                img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
                trip_images.append(img_np)
                raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )



    else:
        fish0 = render_batch_to_fov(sample_batched, fov, Rotation.from_euler('xyz', [0, 0, roll], degrees=True).as_matrix())

        B = sample_batched['lcam_front']['image_0'].shape[0]
        for b in range(B):
            img_np = (fish0[b].permute(1,2,0) * 255).to(dtype=torch.uint8).cpu().numpy()
            trip_images.append(img_np)
            raw_iamges.append((sample_batched['lcam_front']['image_0'][b] * 255).to(dtype=torch.uint8).permute(1,2,0).cpu().numpy() )


# Show the images side by side.
concat_images = []
for i in range(len(trip_images)):
    img1 = trip_images[i]
    img2 = raw_iamges[i]
    
    # Resize both to the same size.
    img1 = cv2.resize(img1, (512, 512))
    img_buffer = cv2.resize(img1, (512, 512))[:, :100, :] * 0
    img2 = cv2.resize(img2, (512, 512))

    img = np.concatenate((img2, img_buffer, img1), axis=1)
    concat_images.append(img)

# Create a gif.
import imageio
imageio.mimsave('trip.gif', concat_images, fps=10)
