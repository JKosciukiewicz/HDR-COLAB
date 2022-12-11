import cv2
from matplotlib import image
import numpy 


# Sample HDR image generated following these tutorials:
# https://docs.opencv.org/3.4/d2/df0/tutorial_py_hdr.html
# https://docs.opencv.org/4.x/d3/db7/tutorial_hdr_imaging.html


def create_hdr(img_samples,img_exposure_times_data):
    # image exposure times in seconds of each image (from metadata)
    # !MIGHT CAUSE ISSUES FOR MRI IMAGING
    img_exposure_times=numpy.array(img_exposure_times_data, dtype=numpy.float32)
    img_list_nosize=[cv2.imread(img) for img in img_samples]
    img_list=[cv2.resize(img, (256,256)) for img in img_list_nosize]
    #Create HDR images using different methods
    get_debeveck(img_list,img_exposure_times)
    get_robertson(img_list,img_exposure_times)
    get_mertens(img_list)


#Create HDR image using Debeveck method 
def get_debeveck(images,image_exposures):
    merge_debevec = cv2.createMergeDebevec()    
    cal_debevec = cv2.createCalibrateDebevec()
    crf_debevec = cal_debevec.process(images, times=image_exposures)
    hdr_debevec = merge_debevec.process(images, times=image_exposures.copy(), response=crf_debevec.copy())

    # Tonemap HDR image (convert hdr data to avoid overflow after float32->uint8 conversion)
    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_debevec = tonemap1.process(hdr_debevec.copy())

    # Convert datatype to 8-bit and save
    res_debevec_8bit = numpy.clip(res_debevec*255, 0, 255).astype('uint8')
    cv2.imwrite("./output/ldr_debevec.jpg", res_debevec_8bit)


#Create HDR image using Robertson method
def get_robertson(images,image_exposures):
    merge_robertson = cv2.createMergeRobertson()
    cal_robertson = cv2.createCalibrateRobertson()
    crf_robertson = cal_robertson.process(images, times=image_exposures)
    hdr_robertson = merge_robertson.process(images, times=image_exposures.copy(), response=crf_robertson.copy())

    # Tonemap HDR image (convert hdr data to avoid overflow after float32->uint8 conversion)
    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_robertson= tonemap1.process(hdr_robertson.copy())

    # Convert datatype to 8-bit and save
    res_robertson_8bit = numpy.clip(res_robertson*255, 0, 255).astype('uint8')
    cv2.imwrite("./output/ldr_robertson.jpg", res_robertson_8bit)


#Create HDR image using Mertens fusion (DOESN'T REQUIRE EXPOSURE TIMES AND TONEMAPPING !!!)
def get_mertens(images):
    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(images)

    # Convert datatype to 8-bit and save
    res_mertens_8bit = numpy.clip(res_mertens*255, 0, 255).astype('uint8')
    cv2.imwrite("./output/fusion_mertens.jpg", res_mertens_8bit)

