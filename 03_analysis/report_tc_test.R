report_tc_test <- function(df_test, df_control, str_title, confidence=0.95, label1="Test", label2="Control")
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
  
  aux_title = paste(str_title, ' - Group "', label1, '"', sep="")
  normality_test(list_test, aux_title, confidence)
  writeLines("")
  aux_title = paste(str_title, ' - Group "', label2, '"', sep="")
  normality_test(list_control, aux_title, confidence)
  writeLines("")

  aux_title = paste(str_title, ' - Groups "', label1, '" and "', label2, '"', sep="")
  same_variance_test(list_test, list_control, aux_title, confidence)
  writeLines("")

  aux_title = paste(str_title, ' - Groups "', label1, '" and "', label2, '"', sep="")
  same_mean_test_unpaired(list_test, list_control, aux_title, confidence, label1, label2)
  writeLines("")
  writeLines("")
}
