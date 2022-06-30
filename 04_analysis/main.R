#sudo apt install r-base r-base-core r-recommended

#ad.test
library(nortest)

#str_pad
library(stringr)

library(ggplot2)


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
  folders = c("../data/b001",
              "../data/b002",
              "../data/b003",
              "../data/b004",
              "../data/b009",
              "../data/b010",
              "../data/b011",
              "../data/b012",
              "../data/b013",
              "../data/b014",
              "../data/b015",
              "../data/b016",
              "../data/b017",
              "../data/b018",
              "../data/b019",
              "../data/b020",
              "../data/b021",
              "../data/b022",
              "../data/b023",
              "../data/b024",
              "../data/b025",
              "../data/b026",
              "../data/b027",
              "../data/b028",
              "../data/b029",
              "../data/b030",
              "../data/b031",
              "../data/b032",
              "../data/b033",
              "../data/b034",
              "../data/b035",
              "../data/b036",
              "../data/b037",
              "../data/b038",
              "../data/b039",
              "../data/b040",
              "../data/b041",
              "../data/b042",
              "../data/b043",
              "../data/b044")
  #folders = c("../data/b044")
}

ds_files = c("02_preprocess/dataset_dd.tsv", "02_preprocess/dataset_jf.tsv")
#ds_files = c("02_preprocess/dataset_dd.tsv")
#ds_files = c("02_preprocess/dataset_jf.tsv")

filename_dataset = "dataset.tsv"
#concatenate_datasets(folders, filename_dataset, ds_files)

filename_dataset_stack = "dataset_stack.tsv"
dataset_stack(filename_dataset, filename_dataset_stack)

###############################################################3
#folder_names = get_folder_names(df)
#stats_df = create_SI_dataframe(df, folder_names)
#result = get_stats(stats_df)
#print(result)

df = load_data(filename_dataset)
df_stack = load_data(filename_dataset_stack)

confidence = 0.95
prompt     = 0
inputFile     = filename_dataset
outputDir      = "saida"
outputFile     = "report.html"

report(inputFile, outputFile, outputDir, df, df_stack, confidence, prompt)


###############################################################3

#group_roles(filename)
