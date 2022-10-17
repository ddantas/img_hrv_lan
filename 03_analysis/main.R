#sudo apt install r-base r-base-core r-recommended

#ad.test
library(nortest)

#str_pad
library(stringr)

#ggplot, stat_cor
library(ggplot2)
library(ggpubr)

GENERATE = FALSE
REPORT   = TRUE

source("utils.R")
source("analysis.R")
source("group_roles.R")
source('report.R')
source('dataset_stack.R')

folders = commandArgs(trailingOnly=TRUE)
print("Getting datasets from folders")
print(folders)

if (length(folders) == 0)
{
  folders = c("../data/001",
              "../data/002",
              "../data/003",
              "../data/004",
              "../data/005")
  #folders = c("../data/001")
}

#ds_files = c("02_preprocess/dataset_dd.tsv", "02_preprocess/dataset_jf.tsv")
ds_files = c("02_preprocess/dataset.tsv")

filename_dataset = "dataset.tsv"
if (GENERATE)
{
  concatenate_datasets(folders, filename_dataset, ds_files)
}

###########################################################
df = load_data(filename_dataset)

confidence = 0.95
prompt     = 0
inputFile     = filename_dataset
outputDir      = "saida"
outputFile     = "report.html"

if (REPORT)
{
  report(inputFile, outputFile, outputDir, df, df_stack, confidence, prompt)
}

###########################################################

#group_roles(filename)
