load_data <- function(filename){

  data = read.table(filename, header=TRUE, sep='	')

  return(data)
}

concatenate_datasets <- function(folders, filename_output, ds_files) {

  columns = c("folder", "annotator", "block", "label", "time",
              "IsImit", "IsSync", "Imitator", "Model",
              "hr_subj1_linear", "hr_subj2_linear", "hr_subj1_nearest", "hr_subj2_nearest",
              "hr_subj1_ecg_linear", "hr_subj2_ecg_linear", "hr_subj1_ecg_nearest",
              "hr_subj2_ecg_nearest", "msg1", "msg2")

  for (default_ds_subpath in ds_files)

  final_df = data.frame(matrix(nrow=0, ncol=length(columns)))
  colnames(final_df) = columns

  print(folders)
  for (f in folders){
    writeLines(paste("Folder: ", f))
    ds_path = file.path(f, default_ds_subpath)
    df = load_data(ds_path)
    # If IsImit is FALSE, IsSync must be NA
    n = length(df[(df$IsImit == FALSE & !is.na(df$IsSync)), "IsSync"])
    if (n > 0)
    {
      writeLines(paste("Found", n, "lines with IsImit = FALSE and IsSync != NA. Correcting..."))
      writeLines("")
      df[(df$IsImit == FALSE & !is.na(df$IsSync)), "IsSync"] = NA
    }
    # Fill Model column
    df$Model = 3 - df$Imitator
    # Fill derivative  columns
    df$d_hr_subj1_linear      = derivate(df$hr_subj1_linear)
    df$d_hr_subj2_linear      = derivate(df$hr_subj2_linear)
    df$d_hr_subj1_nearest     = derivate(df$hr_subj1_nearest)
    df$d_hr_subj2_nearest     = derivate(df$hr_subj2_nearest)
    df$d_hr_subj1_ecg_linear  = derivate(df$hr_subj1_ecg_linear)
    df$d_hr_subj2_ecg_linear  = derivate(df$hr_subj2_ecg_linear)
    df$d_hr_subj1_ecg_nearest = derivate(df$hr_subj1_ecg_nearest)
    df$d_hr_subj2_ecg_nearest = derivate(df$hr_subj2_ecg_nearest)

    print(colnames(df))
    final_df = rbind(final_df, df)
  }

  write.table(final_df, file=filename_output, sep="\t", col.names=NA)
}

get_folder_names <- function(df) {
  return(unique(df$folder))
}


# Return derivative or input array
derivate <- function(arr)
{
  arr2 = c(arr[-1], tail(arr, n=1))
  result = arr2 - arr
  return(result)
}
