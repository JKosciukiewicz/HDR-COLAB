from ctypes import sizeof

from requests import ReadTimeout
from exposures import get_exposure_time, calculate_exposure
from pydoc import doc
from tempfile_name_generator import get_tempfilename
from image_data import ImageData

import pydicom
import numpy as np
import PIL

def process_dicom(path):
    dicom=pydicom.dcmread(path)
    dicom_average_exposure=get_dicom_exposure(dicom)
    #generate image name
    tempfilename=get_tempfilename('./temp','.jpg')
    #print_echo_times(dicom)
    dicom_to_image(dicom,tempfilename)
    converted_dicom_data=ImageData(tempfilename,dicom_average_exposure)
    return converted_dicom_data


def print_echo_times(dicom):
    Te=dicom[0x18,0x81].value
    Tr=dicom[0x18,0x80].value
    T1_relaxivity=dicom[0x18,0x13].value
    T2_preparation=dicom[0x18,9021].value
    print(f"Te={Te}\nTr={Tr}")
    print(f"T1={T1_relaxivity}\nT2={T2_preparation}")
    #print(T2_preparation)


def get_dicom_exposure(dicom):
    #read Te and Tr from meta
    Te=dicom[0x18,0x81].value
    Tr=dicom[0x18,0x80].value
    #get array dimensions
    dataArray=dicom.pixel_array
    rows=dataArray.shape[0]
    cols=dataArray.shape[1]

    #exposure times will be saved here
    timeArray=np.empty(dataArray.shape)
    exposure_times=[]
    for row in range (0,rows):
        for col in range (0, cols):
            exposure_time=calculate_exposure(1,Te,Tr,dataArray[row,col],dataArray[row,col],4)
            timeArray[row,col]=exposure_time
            exposure_times.append(round(exposure_time,5))

    average_exposure=get_average_exposure(exposure_times)
    return average_exposure
    #print(timeArray)


#might use it later
def get_double_dicom(T1_dicom,T2_dicom):
    Te_1=T1_dicom[0x18,0x81].value
    Tr_1=T1_dicom[0x18,0x80].value
    Te_2=T2_dicom[0x18,0x81].value
    Tr_2=T2_dicom[0x18,0x80].value

    #check if Te's and Tr's are equal
    if Te_1==Te_2 and Tr_1==Tr_2:
        t1_array=T1_dicom.pixel_array
        t2_array=T2_dicom.pixel_array

        t1_shape=t1_array.shape
        t2_shape=t2_array.shape

        #check if scan sizes are equal
        if t1_shape[0]==t2_shape[0] and t1_shape[1]==t2_shape[1]:
            #get dimensions of array
            rows=t1_array.shape[0]
            cols=t1_array.shape[1]

            #exposure times will be saved here
            time_array=np.empty(t1_array.shape)
            exposure_times=[]
            for row in range (0,rows):
                for col in range (0, cols):
                    exposure_time=calculate_exposure(1,Te_1,Tr_1,t1_array[row,col],t2_array[row,col],4)
                    time_array[row,col]=exposure_time
                    exposure_times.append(round(exposure_time,5))

            average_exposure=get_average_exposure(exposure_times)

        else:
            print('Error, scans are of different resolution')
    else:
        print('Te or Tr times are different')


#mathematically average
def get_average_exposure(exposure_times):
    exposure_average=0
    for value in exposure_times:
        if value !=0:
            exposure_average=exposure_average+value

    average=exposure_average/len(exposure_times)
    #print('average (s)',average)
    return average


#save image to jpeg/png
def dicom_to_image(dicom,filename):
    image_as_float=dicom.pixel_array.astype(float)
    scaled_image = (np.maximum(image_as_float, 0) / image_as_float.max()) * 255.0 
    scaled_image = np.uint8(scaled_image)
    final_image = PIL.Image.fromarray(scaled_image)
    final_image.save(f"{filename}")
    #final_image.save('image.png')