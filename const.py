#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Define constants used by multiple source files.      ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Mar 2022                                ###
############################################################
#########################################################"""

import os

## Used mostly by Polar.py, Data.py and Plot.py
TYPE_RR  = "R"
TYPE_ECG = "E"

## Used mostly by WinOp.py
FOLDER_DATA = "data"
FOLDER_DEBUG = os.path.join(FOLDER_DATA, "DEBUG")

FILENAME_ROUTINE  = "log.txt"
FILENAME_LOG      = "routine.txt"

FILENAME_ECG      = "subj%d_ecg.tsv"
FILENAME_ECG_S1   = "subj1_ecg.tsv"
FILENAME_ECG_S2   = "subj2_ecg.tsv"

FILENAME_RR       = "subj%d_rr.tsv"
FILENAME_RR_S1    = "subj1_rr.tsv"
FILENAME_RR_S2    = "subj2_rr.tsv"

FILENAME_VIDEO    = "subj%d.mp4"
FILENAME_VIDEO_S1 = "subj1.mp4"
FILENAME_VIDEO_S2 = "subj2.mp4"


## Used mostly by 01_sync/sync.py
FOLDER_SYNC = "01_sync"
FILENAME_VIDEO_SYNC    = "subj%d_sync.mp4"
FILENAME_VIDEO_SYNC_S1 = "subj1_sync.mp4"
FILENAME_VIDEO_SYNC_S2 = "subj2_sync.mp4"

## Used mostly by 02_preprocess/preprocess.py
FOLDER_PREP = "02_preprocess"
FILENAME_DATASET = "dataset.tsv"

