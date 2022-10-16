plot_pdc_df <- function(df_pdc, str_title, outputDir="") {

  source("script.R")

  outputFullname = ""
  outputFile     = ""
  outputSubdir   = "plot_pdc"
  
  if (outputDir != "")
  {
    writeLines(paste("<table><tr>", sep=""))
  }
    
  if (outputDir != "")
  {
    outputFile     = paste("pdc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }

  #df_pdc = cbind(data1, data2, hand_pos_data1, hand_pos_data1)
  res_pdc = get_pdc_new(df_pdc)

  if (outputDir != "")
  {
    writeLines(paste("<td><img src='", outputSubdir, "/", outputFile, "'></td>", sep=""))
    writeLines("")
    writeLines("")
    dev.off()
  }

  if (outputDir != "")
  {
    writeLines(paste("</tr></table>", sep=""))
  }
  
  #writeLines("")
  #writeLines(paste("size = (", nrow(data1), ", ", nrow(data2), ", ", nrow(hand_pos_data1), ", ", nrow(hand_pos_data2), ")", sep=""))
        
  return(res_pdc)
}
