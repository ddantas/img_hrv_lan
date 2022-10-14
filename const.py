#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""#########################################################
############################################################
### Define constants used by multiple source files.      ###
###                                                      ###
### Author: Daniel Dantas                                ###
### Last edited: Sep 2022                                ###
############################################################
#########################################################"""

import os

## Canvas sizes
SUBJ_W = 720
SUBJ_H = 540
OP_W   = 640
OP_H   = 480
PAD_X  = 10
PAD_Y  = 10

## Filenames
EXT_TSV = ".tsv"
EXT_LIN = "_linear.tsv"
EXT_NN  = "_nearest.tsv"
EXT_INFERRED  = "_inferred_rr.tsv"
EXT_FLOW  = "_flow.tsv"

## Used mostly by Polar.py, Data.py and Plot.py
TYPE_RR    = "R"
TYPE_ECG   = "E"
TYPE_AUDIO = "A"

## Used mostly by WinOp.py
FOLDER_DATA = "data"
FOLDER_DEBUG = os.path.join(FOLDER_DATA, "DEBUG")

FILENAME_RANDOM       = "random.txt"
FILENAME_ROUTINE      = "routine.txt"
FILENAME_START_TIME   = "start_time.txt"
FILENAME_LOG          = "log.txt"

FILENAME_ECG      = "subj%d_ecg.tsv"
FILENAME_ECG_S1   = "subj1_ecg.tsv"
FILENAME_ECG_S2   = "subj2_ecg.tsv"

FILENAME_RR       = "subj%d_rr.tsv"
FILENAME_RR_S1    = "subj1_rr.tsv"
FILENAME_RR_S2    = "subj2_rr.tsv"

FILENAME_AUDIO    = "audio.wav"

# "subj%d_ecg_inferred_rr.tsv"
FILENAME_ECG_RR       = FILENAME_ECG.replace(EXT_TSV, EXT_INFERRED)
FILENAME_ECG_RR_S1    = FILENAME_ECG_S1.replace(EXT_TSV, EXT_INFERRED)
FILENAME_ECG_RR_S2    = FILENAME_ECG_S2.replace(EXT_TSV, EXT_INFERRED)

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
FOLDER_OUTPUT = "output"
#FILENAME_DATASET = ["dataset_jf.tsv", "dataset_dd.tsv"]
FILENAME_DATASET = "dataset.tsv"
FILENAME_SLIDE = "slides_time.tsv"
#FILENAME_ANNOTATION = ["annotation_jf.eaf", "annotation_dd.eaf"]
# FILENAME_ANNOTATION = "annotation_dd.eaf"
DATASET_HEADERS = ['folder', 'time', 'block', 'slide',
                   'hr_subj1_linear',     'hr_subj2_linear',     'hr_subj1_nearest',     'hr_subj2_nearest', \
                   'hr_subj1_ecg_linear', 'hr_subj2_ecg_linear', 'hr_subj1_ecg_nearest', 'hr_subj2_ecg_nearest', \
                   'rr_subj1_linear',     'rr_subj2_linear',     'rr_subj1_nearest',     'rr_subj2_nearest', \
                   'rr_subj1_ecg_linear', 'rr_subj2_ecg_linear', 'rr_subj1_ecg_nearest', 'rr_subj2_ecg_nearest']

# "subj%d_rr_linear.tsv"
FILENAME_RR_LIN          = FILENAME_RR.replace(EXT_TSV, EXT_LIN)
FILENAME_RR_LIN_S1       = FILENAME_RR_S1.replace(EXT_TSV, EXT_LIN)
FILENAME_RR_LIN_S2       = FILENAME_RR_S2.replace(EXT_TSV, EXT_LIN)

# "subj%d_rr_nearest.tsv"
FILENAME_RR_NN           = FILENAME_RR.replace(EXT_TSV, EXT_NN)
FILENAME_RR_NN_S1        = FILENAME_RR_S1.replace(EXT_TSV, EXT_NN)
FILENAME_RR_NN_S2        = FILENAME_RR_S2.replace(EXT_TSV, EXT_NN)

# "subj%d_ecg_inferred_rr_linear.tsv"
FILENAME_ECG_RR_LIN      = FILENAME_ECG_RR.replace(EXT_TSV, EXT_LIN)
FILENAME_ECG_RR_LIN_S1   = FILENAME_ECG_RR_S1.replace(EXT_TSV, EXT_LIN)
FILENAME_ECG_RR_LIN_S2   = FILENAME_ECG_RR_S2.replace(EXT_TSV, EXT_LIN)

# "subj%d_ecg_inferred_rr_nearest.tsv"
FILENAME_ECG_RR_NN       = FILENAME_ECG_RR.replace(EXT_TSV, EXT_NN)
FILENAME_ECG_RR_NN_S1    = FILENAME_ECG_RR_S1.replace(EXT_TSV, EXT_NN)
FILENAME_ECG_RR_NN_S2    = FILENAME_ECG_RR_S2.replace(EXT_TSV, EXT_NN)

## Used mostly by 03_optical_flow/optical_flow.py
FOLDER_OPTI = "03_optical_flow"
LEN_PREF_VIDEO = 5
