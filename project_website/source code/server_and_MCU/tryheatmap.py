import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from PIL import Image
height = 2250#x
width = 1050#y
size = (height,width)

def gaussian(sigma, d):
    y = np.exp(-d ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))
    return y
def myheatmapleft(left_data):
    left_data[8] = min(left_data[8]-300,4095)
    left_data[9] = min(left_data[9]-300,4095)
    left_data[10] = min(left_data[10]-300,4095)
    left_data[11] = min(left_data[11]-300,4095)
    left_data[12] = min(left_data[12]+2200,4095)
    left_data[13] = min(left_data[13]+3000,4095)
    left_data[14] = min(left_data[14]+1100,4095)
    left_data[15] = min(left_data[15]+1100,4095)
    left_data = [4095 - i for i in left_data]
    
    left_center_x_prim = np.array([(300,544),(240,544),(250,544),(300,544),(577,1000),(577,1000),(577,1000),(577,851),(877,1138),(1029,1442),(1029,1442),(1160,1442),(1463,1707),(1463,1707),(1730,2000),(1730,2000)])##x is column
    left_center_x = np.zeros(16,dtype = int)
    left_center_y_prim=np.array([(800, 713), (689, 608), (585, 504), (478, 316), (770, 663), (637, 524), (504, 391), (361, 265), (363, 243), (650, 508), (486, 391), (363, 255), (597, 442), (414, 259), (597, 442), (414, 259)])
    left_center_y = np.zeros(16,dtype = int)

    left_center = np.zeros((16,2),dtype = int)
    for i in range(left_center_x_prim.shape[0]):
        left_center_x[i] =(left_center_x_prim[i,0]+left_center_x_prim[i][1])//2
        left_center_y[i] = (left_center_y_prim[i,0]+left_center_y_prim[i][1])//2
        left_center[i,0]=left_center_x[i]
        left_center[i,1] = left_center_y[i]
    left_radius = np.zeros(16, dtype = int )
    for i in range(16):
        left_radius[i] =math.sqrt((left_center[i,0]-left_center_x_prim[i,0])**2+(left_center[i,1]-left_center_y_prim[i,0])**2) 
    Y = np.arange(0,width, 4)
    X = np.arange(0,height, 4)
    Y,X = np.meshgrid(Y, X)
    Rl = np.zeros((height//4+1,width//4+1))
    for i in range(16):
        tmpl= np.sqrt((X-left_center[i,0])**2 + (Y-left_center[i,1])**2)
        yl = gaussian(left_radius[i],tmpl)
        yl = left_data[i]* yl
        Rl +=yl
    Rlmin,Rlmax= Rl.min(),Rl.max()
    Rl= (Rl - Rlmin) * (1/(Rlmax - Rlmin))
    plt.imsave('testl.png',Rl,format="png",cmap='magma')

def myheatmapright(right_data):
#bottom image
#compute center of right foot 
    right_data = [4095 - i for i in right_data]
    right_center_x_prim = np.array([(300,544),(240,544),(250,544),(300,544),(577,1000),(577,1000),(577,1000),(577,851),(877,1138),(1029,1442),(1029,1442),(1160,1442),(1463,1707),(1463,1707),(1730,2000),(1730,2000)])##x is column
    right_center_x = np.zeros(16,dtype = int)
    right_center_y_prim=np.array([(250,337),(361,442),(465,546),(572,734),(280,387),(413,526),(546,659),(689,785),(687,807),(400,542),(564,659),(687,795),(453,608),(636,791),(453,608),(636,791)])
    right_center_y = np.zeros(16,dtype = int)

    right_center = np.zeros((16,2),dtype = int)
    for i in range(right_center_x_prim.shape[0]):
        right_center_x[i] =(right_center_x_prim[i,0]+right_center_x_prim[i][1])//2
        right_center_y[i] = (right_center_y_prim[i,0]+right_center_y_prim[i][1])//2
        right_center[i,0] = right_center_x[i]
        right_center[i,1] = right_center_y[i]

#compute radius
    right_radius = np.zeros(16, dtype = int )
    for i in range(16):
        right_radius[i] =math.sqrt((right_center[i,0]-right_center_x_prim[i,0])**2+(right_center[i,1]-right_center_y_prim[i,0])**2) 

    Y = np.arange(0,width, 4)
    X = np.arange(0,height, 4)
    Y,X = np.meshgrid(Y, X)
    Rr = np.zeros((height//4+1,width//4+1))
    for i in range(16):
        tmpr= np.sqrt((X-right_center[i,0])**2 + (Y-right_center[i,1])**2)
        yr = gaussian(right_radius[i],tmpr)
        yr =right_data[i]* yr
        Rr += yr
        
    Rrmin,Rrmax= Rr.min(),Rr.max()
    Rr= (Rr - Rrmin) * (1/(Rrmax - Rrmin))
    plt.imsave('testr.png',Rr,format="png",cmap='magma')




