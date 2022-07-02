plot_pdc <- function(data1, data2, str_title, outputDir="") {

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

  df = cbind(data1, data2)
  res = get_pdc(df)

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

  return(res)
}