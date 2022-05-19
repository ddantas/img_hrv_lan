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

EXT_TSV = ".tsv"
EXT_LIN = "_linear.tsv"
EXT_NN  = "_nearest.tsv"
EXT_INFERRED  = "_inferred_rr.tsv"

## Used mostly by Polar.py, Data.py and Plot.py
TYPE_RR  = "R"
TYPE_ECG = "E"

## Used mostly by WinOp.py
FOLDER_DATA = "data"
FOLDER_DEBUG = os.path.join(FOLDER_DATA, "DEBUG")

FILENAME_ROUTINE  = "routine.txt"
FILENAME_LOG      = "log.txt"

FILENAME_ECG      = "subj%d_ecg.tsv"
FILENAME_ECG_S1   = "subj1_ecg.tsv"
FILENAME_ECG_S2   = "subj2_ecg.tsv"

FILENAME_RR       = "subj%d_rr.tsv"
FILENAME_RR_S1    = "subj1_rr.tsv"
FILENAME_RR_S2    = "subj2_rr.tsv"

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
FILENAME_DATASET = ["dataset_jf.tsv", "dataset_dd.tsv"]
# FILENAME_DATASET = "dataset_dd.tsv"
FILENAME_ANNOTATION = ["annotation_jf.eaf", "annotation_dd.eaf"]
# FILENAME_ANNOTATION = "annotation_dd.eaf"
DATASET_HEADERS = ['folder', 'annotator', 'block', 'label', 'time', 'IsImit', 'IsSync', 'Imitator',\
					'Model', 'hr_subj1_linear', 'hr_subj2_linear', 'hr_subj1_nearest', 'hr_subj2_nearest', \
					'hr_subj1_ecg_linear', 'hr_subj2_ecg_linear', 'hr_subj1_ecg_nearest', 'hr_subj2_ecg_nearest', \
					'msg1', 'msg2']

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
