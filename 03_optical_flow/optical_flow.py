#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Preprocess Polar H10 and annotation data.            ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Fev 2022                                ###
############################################################
#########################################################"""

import os
import xml.etree.ElementTree as et
from queue import Queue
import sys
import pandas as pd
import numpy as np
import cv2

#import rr_interpolation
#import rr_inference

# Import module from parent folder
filepath = os.path.dirname(__file__)
modpathrel = os.path.join(filepath, "..")
modpathabs = os.path.abspath(modpathrel)
sys.path.append(modpathabs)

import Data
import const as k
import utils


def create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_annot, filename_dataset):
  
  dfs = []
  for key in tiers_dict.keys():
    content[key] = ["" if val is None else val.strip() for val in content[key]]

  for h in k.DATASET_HEADERS:
    print(h)
    if (h == "msg1" or h == "msg2"):
      for i in range(len(content[h])):
        content[h][i] = content[h][i].replace('"', '')
    dfs.append(pd.Series(content[h], name=h))

  df = pd.concat(dfs, axis=1)
  
  df.to_csv(filename_dataset, sep = '\t', index=False, mode = "w", header = True)

def write_to_dataset0(filename_input, filename_output):

  cap = cv2.VideoCapture(filename_input)
  f = 0
  while(cap.isOpened()):
    ret, frame = cap.read()
    print(f, ret, cap.isOpened())
    if (ret):
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      gray[0:24, :] = 0
      cv2.imshow('frame', gray)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    f += 1
    if (f > 20000):
      break

  cap.release()
  cv2.destroyAllWindows()

  return

def find_maximum(img):
  y_max, x_max = np.unravel_index(np.argmax(img), img.shape)
  return x_max, y_max, img[y_max, x_max]

def find_centroid(img):
  aux = img.astype(int)
  if (len(aux.shape) > 2):
    print("Error: find_centroid: image must be grayscale.")
    return
  tot = sum(sum(aux))
  h, w = aux.shape[0:2]

  x_sum = sum(aux)
  x_coord = range(len(x_sum))
  cx = np.dot(x_sum, x_coord) / tot

  y_sum = sum(aux.transpose())
  y_coord = range(len(y_sum))
  cy = np.dot(y_sum, y_coord) / tot  

  return cx, cy

def apply_mask(img, mask):
  # Grayscale
  if (len(img.shape) <= 2):
    result = np.minimum(img, mask)
  else:
    result = np.zeros(img.shape)
    n_ch = img.shape[2]
    for c in range(n_ch):
      result[:, :, c] = np.minimum(img[:, :, c], mask)
  return result

def find_flow(flow, th=3, magnitude=None):
  x_flow = flow[:, :, 0]
  y_flow = flow[:, :, 1]

  if (magnitude is None):
    magnitude, angle = cv2.cartToPolar(x_flow, y_flow)
  ret, mask = cv2.threshold(magnitude, th, 255, cv2.THRESH_BINARY)
  n_pix = sum(sum(mask)) // 255
  print("n_pix " + str(n_pix))

  import my
  my.imshow(mask)

  flow_masked = apply_mask(flow, mask)
  x_flow_masked = flow_masked[:, :, 0]
  y_flow_masked = flow_masked[:, :, 1]

  #return flow_masked

  x_tot = sum(sum(abs(x_flow_masked)))
  y_tot = sum(sum(abs(y_flow_masked)))
  #h, w = aux.shape[0:2]

  x_sum_abs = sum(abs(x_flow_masked))
  x_sum = sum(x_flow_masked)
  x_coord = range(len(x_sum))
  print("x_sum_abs " + str(x_sum_abs))
  print("x_coord " + str(x_coord))
  print("x_tot " + str(x_tot))
  cx = np.dot(x_sum_abs, x_coord) / x_tot
  vx = sum(x_sum) / n_pix

  y_sum_abs = sum(abs(y_flow_masked.transpose()))
  y_sum = sum(y_flow_masked.transpose())
  y_coord = range(len(y_sum))
  cy = np.dot(y_sum_abs, y_coord) / y_tot
  vy = sum(y_sum) / n_pix

  return cx, cy, vx, vy

def clamp(c, inf, sup):
  c = max(inf, c)
  c = min(sup, c)
  return c
                        
def split(img):
  w = img.shape[1]
  img_left = img[:, 0:w // 2]
  img_right = img[:, w // 2:]
  return (img_left, img_right)

def draw_cross(img, x, y, r=2):
  x = round(x)
  y = round(y)
  h, w = img.shape[0:2]
  y_min = clamp(y - r, 0, h - 1)
  y_max = clamp(y + r, 0, h - 1)
  x_min = clamp(x - r, 0, w - 1)
  x_max = clamp(x + r, 0, w - 1)
  for y_i in range(y_min, y_max + 1):
    img[round(y_i), round(x)] = 255
  for x_i in range(x_min, x_max + 1):
    img[round(y), round(x_i)] = 255

def write_to_dataset_diff(filename_input, filename_output):

  import numpy as np
  import cv2
  #import my
  
  cap = cv2.VideoCapture(filename_input)
  f = 0
  w_half = -1
  while(cap.isOpened()):
    ret, frame = cap.read()
    frame[0:24, :] = 0
    frame_left, frame_right = split(frame)
    if (f % 2 == 0):
      gray0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #gray0[0:24, :] = 0
      if (f == 0):
        print(f)
        w_half = frame.shape[1] // 2
        f += 1
        continue
    else:
      gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #gray1[0:24, :] = 0
      
    diff = np.uint8(abs(np.int32(gray1) - np.int32(gray0)))
    diff_blur = cv2.blur(diff, (31, 31))

    # save start
    #filename = "f%05d.tiff" % f
    #my.imwrite(filename, diff)
    # save end
    
    l, r = split(diff_blur)
    lx, ly = find_centroid(l)
    rx, ry = find_centroid(r)
    lxm, lym, lvm = find_maximum(l)
    rxm, rym, rvm = find_maximum(r)
    print("%d: L = (%f, %f)  R = (%f, %f)  L[%d, %d] = %d  R[%d, %d] = %d" % (f, lx, ly, rx, ry, lxm, lym, lvm, rxm, rym, rvm))

    draw_cross(diff, lx, ly)
    draw_cross(diff, w_half + rx, ry)
    draw_cross(diff, lxm, lym, lvm // 10)
    draw_cross(diff, w_half + rxm, rym, rvm // 10)
    
    cv2.imshow('frame', diff)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    f += 1
    input("Press Enter...")

  cap.release()
  cv2.destroyAllWindows()
  return

def write_to_dataset_dense(filename_input, filename_output):

  import numpy as np
  import cv2
  import my
  
  cap = cv2.VideoCapture(filename_input)
  f = 0
  w_half = -1
  while(cap.isOpened()):
    ret, frame = cap.read()
    frame[0:24, :] = 0
    frame_left, frame_right = split(frame)
    if (f == 0):
      print(f)
      gray0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      w_half = frame.shape[1] // 2
      mask = np.zeros_like(frame)
      mask[..., 1] = 255
      f += 1
    #elif (f < 3000):
    #  f += 1
    #  continue
    if (f % 2 == 0):
      gray0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #gray0[0:24, :] = 0
      frame_new = gray0
      frame_old = gray1
    else:
      gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      frame_new = gray1
      frame_old = gray0
      #gray1[0:24, :] = 0
      

    flow = cv2.calcOpticalFlowFarneback(frame_old, frame_new, None, pyr_scale = 0.5, levels = 5, winsize = 11, iterations = 5, poly_n = 5, poly_sigma = 1.1, flags = 0)
    # Compute the magnitude and angle of the 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Set image hue according to the optical flow direction
    mask[..., 0] = angle * 180 / np.pi / 2
    # Set image value according to the optical flow magnitude (normalized)
    #mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    mask[..., 2] = 10 * magnitude
    # Convert HSV to RGB (BGR) color representation
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

    th = 0
    #flow_masked = find_flow(flow, th, magnitude)
    #ret, mask2 = cv2.threshold(magnitude, th, 255, cv2.THRESH_BINARY)

    #magnitude[magnitude > 255] = 0
    l_flow, r_flow = split(flow)
    l_mag, r_mag = split(magnitude)
    print("l_flow.shape " + str(l_flow.shape))
    print("r_flow.shape " + str(r_flow.shape))
    print("l_mag.shape " + str(l_mag.shape))
    print("r_mag.shape " + str(r_mag.shape))

    l_cx, l_cy, l_vx, l_vy = find_flow(l_flow, th, l_mag)
    r_cx, r_cy, r_vx, r_vy = find_flow(r_flow, th, r_mag)
    #if (lvm > 255):
    #  lvm = 255
    #if (rvm > 255):
    #  rvm = 255
    #lvm = round(lvm)
    #rvm = round(rvm)
    print("%d: L[%d, %d] + (%f, %f)  R[%d, %d] + (%f, %f)" % (f, l_cx, l_cy, l_vx, l_vy, r_cx, r_cy, r_vx, r_vy))

    #mask = mask.astype(np.uint8)
    draw_cross(rgb,          round(l_cx), round(l_cy), round(l_vx + l_vy) // 1)
    draw_cross(rgb, w_half + round(r_cx), round(r_cy), round(r_vx + r_vy) // 1)
    
    # save start
    #filename = "f%05d.tiff" % f
    #my.imwrite(filename, diff)
    # save end

    dense_flow = cv2.addWeighted(frame, 1, rgb, 2, 0)

    print("np.amax(flow) = " + str(np.amax(flow)))
    print("np.amin(flow) = " + str(np.amin(flow)))
    #print(flow[:, 0, :])
    print("flow.shape = " + str(flow.shape))
    print("magnitude.shape = " + str(magnitude.shape))

    flow2 = np.zeros(frame.shape, dtype=np.uint8)
    print(flow2.dtype)
    flow2[:, :, 2] = 10*flow[:,:,0] + 128
    flow2[:, :, 1] = 10*flow[:,:,1] + 128
    #flow2[:, :, 0] = 128
    
    cv2.imshow('frame', flow2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    f += 1
    if (f > 0):
      input()

  cap.release()
  cv2.destroyAllWindows()
  return


  ## Generate dataset.tsv
  print("Generating complete dataset...")
  create_data_file(input_path,
       filename_rr_linear1, filename_rr_linear2,
       filename_rr_nearest1, filename_rr_nearest2,
       filename_ecg_rr_linear1, filename_ecg_rr_linear2,
       filename_ecg_rr_nearest1, filename_ecg_rr_nearest2,
       filename_annot, filename_dataset)
  print("Done.")

"""#########################################################
############################################################
### Main function                                        ###
############################################################
#########################################################"""

def main(path_input, path_output):

  #for d in dir_list:
    #path_input = d

    path_opti = os.path.join(path_output, k.FOLDER_OPTI)
    if not os.path.exists(path_opti):
      os.mkdir(path_opti)

    files = os.listdir(path_input)
    for filename_video in files:
      
      filename_dataset = filename_video[0:k.LEN_PREF_VIDEO] + k.EXT_FLOW
      filename_input = os.path.join(path_input, filename_video)
      filename_output = os.path.join(path_output, filename_dataset)

      print("path_input: " + path_input)
      print("path_output: " + path_output)
      print("filename_video: " + filename_video)
      print("filename_dataset: " + filename_dataset)      
      print("filename_input: " + filename_input)
      print("filename_output: " + filename_output)
      write_to_dataset_dense(filename_input, filename_output)
      input("Press Enter...")

      
      if filename_video in files:
        pass
        #filename_video = os.path.join(path_input, k.FOLDER_OPTI, filename_ds)
        #filename_dataset = os.path.join(path_input, k.FOLDER_OPTI, filename_ds)
        #print(filename_dataset)
        #write_to_dataset(path_input, path_output, filename_video, filename_dataset)

      else:
        if filename_annot not in files:
          print(f"Could not find {filename_annot}... Skipping")


if __name__ == "__main__":

  # data/output
  print(sys.argv)
  if len(sys.argv) < 2:
    print(f"Usage: python3 optical_flow.py <dir_input> <dir_output>") 
    exit(1)

  dir_input = sys.argv[1]
  dir_output = sys.argv[2]

  print(dir_input)
  print(dir_output)

  #path_dataset = os.path.join(k.FOLDER_DATA, k.FOLDER_OUTPUT)
  #if not os.path.exists(path_dataset):
  #  os.mkdir(path_dataset)
  #print("path_dataset = %s" % path_dataset)

  main(dir_input, dir_output)
