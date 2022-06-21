report_tc_test <- function(df_test, df_control, str_title, confidence=0.95)
{
  source('normality_test.R')
  source('same_variance_test.R')
  source('same_mean_test_unpaired.R')

  list_test    = df_test[[1]]
  list_control = df_control[[1]]
  
  writeLines(paste("Testing column", str_title)) 
  writeLines("")

  #print(list_test)
  #print(class(list_test))
  
  aux_title = paste(str_title, " - Group Test", sep="")
  normality_test(list_test, aux_title, confidence)
  writeLines("")
  aux_title = paste(str_title, " - Group Control", sep="")
  normality_test(list_control, aux_title, confidence)
  writeLines("")

  aux_title = paste(str_title, " - Groups Test and Control", sep="")
  same_variance_test(list_test, list_control, aux_title, confidence)
  writeLines("")

  aux_title = paste(str_title, " - Groups Test and Control", sep="")
  same_mean_test_unpaired(list_test, list_control, aux_title, confidence)
  writeLines("")
  writeLines("")
}
