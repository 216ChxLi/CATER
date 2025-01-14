import cv2
print(cv2.__version__)
import numpy as np
import matplotlib.pyplot as plt

# replace opencv waitKey() to avoid error due to pyqt5 
def disp_img(str,img, kill_window=True):
    plt.figure()
    plt.imshow(img)
    plt.title(str)
    plt.show(block=False)
    plt.waitforbuttonpress(0)
    if kill_window:
        plt.close()
    # cv2.imshow(str,img)
    # cv2.waitKey()

class prepare_data:
    def __init__(self) -> None:
        pass
    
    def save_image(self):
        vidcap = cv2.VideoCapture("./raw_data/all_action_camera_move/videos/CATER_new_005748.avi")
        success, image = vidcap.read()
        count = 0
        while success:
            if count % 50 == 0:
                cv2.imwrite(f'frame{count}.png', image) # save as PNG file
            success,image = vidcap.read()
            print('Read a new frame ', success)
            count += 1
            chr = cv2.waitKey(10)
            if chr == 'q':
                break

    def preprocess_img(self, img):
        
        
        return img

    def process_img(self, img,type='BGR', method = 'kmeans'):    
        disp_img("origin", img, kill_window=False )
        res_img = []
        # method 0: convert to HSV then applying different threshold
        if method == 'threshold':
            if type == 'HSV':
                imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                disp_img("HSV",imgHSV)
                lower_HSV = np.array([110,50,50],dtype=np.uint8)
                upper_HSV = np.array([130,255,255],dtype=np.uint8)
                mask = cv2.inRange(imgHSV,lower_HSV,upper_HSV)
                res_img = cv2.bitwise_and(imgHSV, imgHSV, mask=mask)
            else:
                lower_RGB = np.array([80,30,0],dtype=np.uint8)
                upper_RGB = np.array([160,50,100],dtype=np.uint8)
                mask = cv2.inRange(img,lower_RGB,upper_RGB)
                res_img = cv2.bitwise_and(img,img,mask=mask)
            
            disp_img("after_masking",res_img)


        # methed 1: using watershed 
        # makers = cv2.watershed(imgHLS, markers)
        
        # method 2: using kmeans
        if method == 'kmeans':
            channels = 3 if len(img.shape) > 2 else 1
            # assert channels == 1 , "number of channels"
            if type == 'HSV':
                img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            twoDimg = img.reshape((-1, channels))
            twoDimg = np.float32(twoDimg)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,1000, 1.0)
            K = 7  # num of clusters
            attempts = 100
            ret, label, center = cv2.kmeans(twoDimg,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
            center = np.uint8(center)
            label = label.flatten()
            res_img = center[label]
            res_img = res_img.reshape((img.shape))
            disp_img("res_img",res_img,kill_window=False)

            # display each cluster
            for i in range(K):
                masked_img = np.copy(img)
                masked_img = masked_img.reshape((-1,channels))
                masked_img[label != i] = np.zeros(channels)
                masked_img = masked_img.reshape((img.shape))
                disp_img(f'cluster{i}',masked_img, kill_window=False)
        
        # method 3: GrabCut
        if method == 'grabcut':
            # mask = cv2.Canny(img,100,200)
            mask = np.zeros(img.shape[:2], np.uint8)
            bgd = np.zeros((1,65),np.float64)
            fgd = np.zeros((1,65),np.float64)
            rect = (40,40,240,150)
            cv2.grabCut(img,mask,rect,bgd,fgd,5,cv2.GC_INIT_WITH_RECT)
            cv2.grabCut(img,mask,rect,bgd,fgd,20,cv2.GC_INIT_WITH_MASK)
            mask2 = np.where((mask==2) | (mask==0),0,1).astype('uint8') # mask to set all bgd and possible bgd to 0.
            res_img = img * mask2[:,:,np.newaxis]
            disp_img("res0", res_img,kill_window=False)
            # cv2.destroyAllWindows()
            # img = cv2.GaussianBlur(img,(5,5),0)
            # first erosion then dilation to remove some bright holes after segmentation
            tmp_img = np.copy(res_img)
            kernel = np.ones((2,2),np.uint8)
            # res_img = cv2.erode(res_img,kernel,iterations=3)
            # res_img = cv2.dilate(res_img,kernel,iterations=1)
            res_img = cv2.morphologyEx(res_img,cv2.MORPH_OPEN,kernel)
            mask_tmp_img = np.where(tmp_img != 0, 255, 0).astype('uint8')
            mask_res_img = np.where(res_img != 0, 255, 0).astype('uint8')
            res_eval = cv2.bitwise_xor(mask_res_img, mask_tmp_img)
            disp_img("difference after opening", res_eval, kill_window=False)

        return res_img




if __name__ == "__main__":
    # if input("save image from videos?\n") == 'y' :
    #     save_image()
    img = cv2.imread("frame150.png")
    edge_ = cv2.Canny(img,100,200)
    disp_img("edge",edge_,False)
    pd = prepare_data()
    img = pd.process_img(img, method='grabcut')
    img = pd.process_img(img,method='threshold')
    # img = process_img(img,type='HSV')