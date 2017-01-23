# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 21:02:47 2017

@author: hugh
"""
import scipy
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import random
import time
from scipy.misc import imread
from scipy.misc import imsave
from scipy.misc import imresize
import matplotlib.image as mpimg
from scipy.ndimage import filters
import json
import os

def prepare_data():
    fp = open("face_locations.json", "r")
    d = json.load(fp)
    fp.close()
    crop_and_save_all(d)
    process_non_outliers()
    "print done"
def process_non_outliers():
    out = get_rgb_outliers_in_folder()
    process(".\cropped\\", ".\processed\\", out)
def process(source_dir, dest_dir, exclude_list):
    print "excluding"
    print exclude_list
    for filename in os.listdir(source_dir):
        if filename not in exclude_list:
            im = process_image(filename, source_dir)
            try:
                imsave(dest_dir+filename, im)
            except ValueError:
                print "attempt to save produced value error"
def get_num_images(dir_path):
    return len(os.listdir(dir_path))

def get_rgb_outliers_in_folder(dir_path=".\cropped\\"):    
    means = np.zeros(shape=(get_num_images(dir_path), 3))
    i= 0
    sample = {}
    for filename in os.listdir(dir_path):
        try:
            sample[i]=filename
            vals = get_rgb_mean_for_picture(filename, dir_path)
            means[i] = vals
        except ValueError:
            means[i] = vals[0:3]
        i+=1        
    print means
    mu = np.mean(means, axis=(0))
    sigma = np.std(means, axis=(0))
    outliers = [sample[j] for j in range(0, i-1) if (abs(mu-means[j])[0]/sigma[0]+abs(mu-means[j])[1]/sigma[1]+abs(mu-means[j])[2]/sigma[2])>6 ]
    return  outliers

def get_rgb_mean_for_picture(filename, dir_path):
    return np.mean(imread(dir_path+filename), axis=(0,1))
def crop_and_save_all(im_dictionary, dest_dir=".\cropped\\", source_dir=".\uncropped\\"):
    done = [] #file names of successfully saved images    
    for (filename, size) in im_dictionary.items():
        if os.path.exists(source_dir+filename) and not(os.path.exists(dest_dir+filename)):
            try:
               im = imread(source_dir+filename)
               im = crop_image(im, size[0], size[1], size[2], size[3])
            except IOError:
                print "failed to read " + filename
            except ValueError:
                continue
            except IndexError:
                continue
            try:
                imsave(dest_dir+filename, im)
                done.append(filename)
            except ValueError:
                print "processing file " + filename + " failed. File may be corrupt."
    #fp = open(dest_dir+"contents.json", 'w')
    #json.dump(done, fp)

def process_and_save_all(im_dictionary, dest_dir=".\processed\\", source_dir=".\uncropped\\"):
    for (filename, size) in im_dictionary.items():
        print size
        if os.path.exists(source_dir+filename):
            try:
                im = read_image(filename, dir_path=source_dir)
            except IOError:
                print "failed to read " + filename
            except ValueError:
                continue
            try:
                if not (os.path.exists(dest_dir+filename)):
                    imsave(dest_dir+filename, im)
            except ValueError:
                print "processing file " + filename + " failed. File may be corrupt."

def crop_image(im, x1, y1, x2, y2):
    print x1, x2, y1, y2, type(x1), type(im)
    return im[int(x1) : int(x2), int(y1) : int(y2)]
    
def process_image(image_title, dir_path=".\\uncropped\\"):
    im = imread(dir_path+image_title)
    #im = crop_image(im, size[0], size[1], size[2], size[3])
    im = resize_as_32x32(im)
    im = rgb2gray(im)
    return im
    
def open_image(file_name, dir_path):
    return imread(dir_path+image_title)
def resize_as_32x32(image_vector):
    resized_im_vec = scipy.misc.imresize(image_vector, size=(32, 32))
    return resized_im_vec
    
def rgb2gray(rgb, r_weight=0.2989, g_weight=0.5870, b_weight=0.1140):
    '''Return the grayscale version of the RGB image rgb as a 2D numpy array
    whose range is 0..1
    Arguments:
    rgb -- an RGB image, represented as a numpy array of size n x m x 3. The
    range of the values is 0..255
    '''
    if( rgb.ndim != 3 ):
        return "rgb gray called on non 3d-array"
    
    
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        
    gray = r_weight * r + g_weight * g + b_weight * b

    return gray/255.