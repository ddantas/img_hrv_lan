load_data <- function(filename){

  data = read.table(filename, header=TRUE, sep='	')

  return(data)
}

concatenate_datasets <- function(folders) {

  columns = c("folder", "block", "label", "time", "IsImit", "IsSync", "Imitator", "Model", 
            "hr_subj1_linear", "hr_subj2_linear", "hr_subj1_nearest", "hr_subj2_nearest", 
            "hr_subj1_ecg_linear", "hr_subj2_ecg_linear", "hr_subj1_ecg_nearest", 
            "hr_subj2_ecg_nearest", "msg1", "msg2")

  default_ds_subpath = "02_preprocess/dataset.tsv"

  final_df = data.frame(matrix(nrow=0, ncol=length(columns)))
  colnames(final_df) = columns

  for (f in folders){
    ds_path = file.path(f, default_ds_subpath)
    df = load_data(ds_path)
    final_df = rbind(final_df, df)
  }

  write.table(final_df, file="output.tsv", sep="\t", col.names=NA)
}

get_folder_names <- function(df) {
  return(unique(df$folder))
}