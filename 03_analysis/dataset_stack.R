dataset_stack <- function(filename_input, filename_output)
{
  df = load_data(filename_input)


  df1 = df[c("folder", "annotator", "block", "label", "time", "IsImit", "IsSync", "Imitator", "Model",
             "hr_subj1_linear", "hr_subj1_nearest", "hr_subj1_ecg_linear", "hr_subj1_ecg_nearest", "msg1", "Gender",
             "d_hr_subj1_linear", "d_hr_subj1_nearest", "d_hr_subj1_ecg_linear", "d_hr_subj1_ecg_nearest")]
  df2 = df[c("folder", "annotator", "block", "label", "time", "IsImit", "IsSync", "Imitator", "Model",
             "hr_subj2_linear", "hr_subj2_nearest", "hr_subj2_ecg_linear", "hr_subj2_ecg_nearest", "msg2", "Gender",
             "d_hr_subj2_linear", "d_hr_subj2_nearest", "d_hr_subj2_ecg_linear", "d_hr_subj2_ecg_nearest")]

  colnames_new = c("folder", "annotator", "block", "label", "time", "IsImit", "IsSync", "Imitator", "Model",
             "hr_linear", "hr_nearest", "hr_ecg_linear", "hr_ecg_nearest", "msg", "Gender",
             "d_hr_linear", "d_hr_nearest", "d_hr_ecg_linear", "d_hr_ecg_nearest")

  colnames(df1) = colnames_new
  colnames(df2) = colnames_new
  df_new = rbind(df1, df2)

  write.table(df_new, file=filename_output, sep="\t", row.names=FALSE)
}


