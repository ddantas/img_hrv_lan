source("utils.R")
source("analysis.R")

filename = "output.tsv"

folders = commandArgs(trailingOnly=TRUE)
print("Getting datasets from folders")
print(folders)
concatenate_datasets(folders)

imit = TRUE
sync = NA

df = load_data(filename)
folder_names = get_folder_names(df)
stats_df = create_SI_dataframe(df, folder_names)
df = get_stats(stats_df)

print(df)
