source("utils.R")
source("analysis.R")

folders = commandArgs(trailingOnly=TRUE)
print("Getting datasets from folders")
print(folders)

if (length(folders) == 0)
{
  folders = c("../data/a001",
              "../data/a003",
              "../data/a004",
              "../data/a005",
              "../data/a006")
}

filename = "output.tsv"
concatenate_datasets(folders, filename)

imit = TRUE
sync = NA

df = load_data(filename)
folder_names = get_folder_names(df)

stats_df = create_SI_dataframe(df, folder_names)
result = get_stats(stats_df)
print(result)
