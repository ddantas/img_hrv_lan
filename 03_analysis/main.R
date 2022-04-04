

source("utils.R")
source("analysis.R")

filename = "../data/a003/02_preprocess/dataset.tsv"

df = load_data(filename)


imit = TRUE
sync = NA

df = load_data(filename)
#result = get_SI_stats(filename, imit, sync)
stats_df = create_SI_dataframe(df)
