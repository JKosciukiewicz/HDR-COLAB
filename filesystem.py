import nibabel 
import dicom2nifti
import os
import numpy as np
import matplotlib.pyplot as plt
import pydicom



def dicom_to_nifti(path):
    try:
        #dicom2nifti.dicom_series_to_nifti('./scans','./output',reorient_nifti=True)
        dicom2nifti.convert_directory(path,"./output",compression=True, reorient=True)
    except Exception as ex:
        print(ex)


def open_scan(path):
    image=nibabel.load(path)
    image_data=image.get_fdata()
    #header contains metadata
    header=image.header.extensions
    print(header)
    #print(image_data)
    image_shape=image_data.shape
    num_of_slices=image_shape[0]
    voxels_x=image_shape[1]
    voxels_y=image_shape[2]

    # x_slice = image_data[9, :, :]
    # y_slice = image_data[:, 19, :]
    # z_slice = image_data[:, :, 2]
    # slices = [x_slice, y_slice, z_slice]

    slices=[]

    for i in range(10, 22):
        slices.append(image_data[:,:,i])

    rows=4
    cols=int(len(slices)/rows)
    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    index=0
    for i in range(0,rows):
        for j in range(0,cols):
            item=slices[index]
            axes[i][j].imshow(item.T, cmap="gray", origin="lower")
            index+=1
    
    #for i, slice in enumerate(slices):
    #    axes[i].imshow(slice.T, cmap="gray", origin="lower")
    plt.tight_layout()
    plt.show()

