
'''

	This code does inference of trained Rooftop segmentation model (download from G.Drive) 
	to test a region of interest specified by user.
	Steps:
			* User Specifies latitude and logitude in GUI
			* Google Maps displaying specified Lat,Long is displayed on browser
			* User performs zooming if needed on map and inputs "yes"
			* Screenshot of map will be taken so that user selects ROI bounding box (crop image by dragging mouse)
			* The cropped image is used for inference and saved   

'''		

from fastai.vision import *
from fastai.callbacks import *

from fastai.utils.collect_env import *

import skimage 
import time
from skimage import io
from selenium import webdriver
import cv2
import tkinter as tk
import numpy as np
import pyscreenshot as ImageGrab
import sys

show_install(True)

# TODO: look into better way of loading export.pkl w/o needing to redefine these custom classes

class SegLabelListCustom(SegmentationLabelList):
    def open(self, fn): return open_mask(fn, div=True, convert_mode='RGB')
    
class SegItemListCustom(SegmentationItemList):
    _label_cls = SegLabelListCustom

def dice_loss(input, target):
#     pdb.set_trace()
    smooth = 1.
    input = torch.sigmoid(input)
    iflat = input.contiguous().view(-1).float()
    tflat = target.contiguous().view(-1).float()
    intersection = (iflat * tflat).sum()
    return 1 - ((2. * intersection + smooth) / ((iflat + tflat).sum() +smooth))

# adapted from https://www.kaggle.com/c/tgs-salt-identification-challenge/discussion/65938
class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets.float(), reduction='none')
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1-pt)**self.gamma * BCE_loss

        if self.reduction == 'mean': return F_loss.mean()
        elif self.reduction == 'sum': return F_loss.sum()
        else: return F_loss

class DiceLoss(nn.Module):
    def __init__(self, reduction='mean'):
        super().__init__()
        self.reduction = reduction
        
    def forward(self, input, target):
        loss = dice_loss(input, target)
        if self.reduction == 'mean': return loss.mean()
        elif self.reduction == 'sum': return loss.sum()
        else: return loss

class MultiChComboLoss(nn.Module):
    def __init__(self, reduction='mean', loss_funcs=[FocalLoss(),DiceLoss()], loss_wts = [1,1], ch_wts=[1,1,1]):
        super().__init__()
        self.reduction = reduction
        self.ch_wts = ch_wts
        self.loss_wts = loss_wts
        self.loss_funcs = loss_funcs 
        
    def forward(self, output, target):
#         pdb.set_trace()
        for loss_func in self.loss_funcs: loss_func.reduction = self.reduction # need to change reduction on fwd pass for loss calc in learn.get_preds(with_loss=True)
        loss = 0
        channels = output.shape[1]
        assert len(self.ch_wts) == channels
        assert len(self.loss_wts) == len(self.loss_funcs)
        for ch_wt,c in zip(self.ch_wts,range(channels)):
            ch_loss=0
            for loss_wt, loss_func in zip(self.loss_wts,self.loss_funcs): 
                ch_loss+=loss_wt*loss_func(output[:,c,None], target[:,c,None])
            loss+=ch_wt*(ch_loss)
        return loss/sum(self.ch_wts)

def acc_thresh_multich(input:Tensor, target:Tensor, thresh:float=0.5, sigmoid:bool=True, one_ch:int=None)->Rank0Tensor:
    "Compute accuracy when `y_pred` and `y_true` are the same size."
    
#     pdb.set_trace()
    if sigmoid: input = input.sigmoid()
    n = input.shape[0]
    
    if one_ch is not None:
        input = input[:,one_ch,None]
        target = target[:,one_ch,None]
    
    input = input.view(n,-1)
    target = target.view(n,-1)
    return ((input>thresh)==target.byte()).float().mean()

def dice_multich(input:Tensor, targs:Tensor, iou:bool=False, one_ch:int=None)->Rank0Tensor:
    "Dice coefficient metric for binary target. If iou=True, returns iou metric, classic for segmentation problems."
#     pdb.set_trace()
    n = targs.shape[0]
    input = input.sigmoid()
    
    if one_ch is not None:
        input = input[:,one_ch,None]
        targs = targs[:,one_ch,None]
    
    input = (input>0.5).view(n,-1).float()
    targs = targs.view(n,-1).float()

    intersect = (input * targs).sum().float()
    union = (input+targs).sum().float()
    if not iou: return (2. * intersect / union if union > 0 else union.new([1.]).squeeze())
    else: return intersect / (union-intersect+1.0)


def get_pred(learner, tile):
#     pdb.set_trace()
    t_img = Image(pil2tensor(tile[:,:,:3],np.float32).div_(255))
    outputs = learner.predict(t_img)
    im = image2np(outputs[2].sigmoid())
    im = (im*255).astype('uint8')
    return im

# Download model file and store in ./models folder
# https://drive.google.com/drive/folders/19YfoHvlN8cixYKzLUveToPBh3m9rGUkq?usp=sharing

# load model file
inference_learner = load_learner(path='models/', file='model.pkl')


# GUI to input latitude and longitude
master = tk.Tk()
master.title("Specify place")
tk.Label(master, 
         text="Latitude", width=15,fg='blue',font = "Verdana 10 bold").grid(row=0)
tk.Label(master, 
         text="Longitude",width=15,fg='blue',font = "Verdana 10 bold").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)


tk.Button(master, 
          text='Go', 
          command=master.quit).grid(row=3, 
                                    column=2, 
                                    sticky=tk.W, 
                                    pady=5)

tk.mainloop()

# Open Google Maps on webbrowser
print("Opening Google Maps")
options = webdriver.ChromeOptions() 
options.add_argument('--no-sandbox')

# get chrome driver for os and update path
extension_path = "/home/user/Desktop/omdena/segmentattion/chromedriver_linux64/chromedriver" 

driver = webdriver.Chrome(extension_path)
#driver = webdriver.Chrome(chrome_options=options)
driver.maximize_window()
# https://www.google.com/maps/@6.5750887,3.3602643,385m/data=!3m1!1e3
url = 'https://www.google.com/maps/@' + str(e1.get())+ ',' +str(e2.get()) + ','+ '180m/data=!3m1!1e3'
print("URL:",url)
driver.get(url)

# Function to select region of interest from GMaps by user and inference on cropped image
def roiSelection_inference():
	
	user_input = input("Enter 'yes' to continue: ")
	if user_input == 'yes':
		im = ImageGrab.grab()

		# save image file
		im.save('picture.png')
		#im.show()


		 
		# Read image
		im = cv2.imread("picture.png")
		     
		# Select ROI
		fromCenter = False
		showCrosshair= False
		rois = cv2.selectROI("Select Image", im, fromCenter, showCrosshair)     
		# Crop image
		cropped_image = im[int(rois[1]):int(rois[1]+rois[3]), int(rois[0]):int(rois[0]+rois[2])]
		 
		# Display cropped image
		#cv2.imshow("Image", imCrop)
		cv2.imwrite("crop.png",cropped_image)
		#cv2.waitKey(0)


		t1 = time.time()
		test_tile = skimage.io.imread('/home/user/Desktop/omdena/segmentattion/crop.png')
		result = get_pred(inference_learner, test_tile)
		t2 = time.time()
		  
		print(f'CPU inference took {t2-t1:.2f}secs')
		fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))
		ax1.imshow(test_tile)
		ax2.imshow(result)
		ax1.axis('off')
		ax2.axis('off')
		plt.imsave('result.png',result)
		plt.show()

		return 0


if __name__== "__main__":
  
	roiSelection_inference()
	sys.exit()




	





  