plot_tc_correlation <- function(df_test, df_control, str_title, prompt=1, outputDir="", xlabel="", label1="Test", label2="Control")
{
  ## Reference:
  ## http://www.sthda.com/english/wiki/ggplot2-scatter-plots-quick-start-guide-r-software-and-data-visualization
  
  outputFullname = ""
  outputFile     = ""
  outputSubdir   = "plot_tc_correlation"

  time = seq(nrow(df_test))
  df_data <- cbind(time, df_test, df_control)
  col1 = colnames(df_data[2])
  col2 = colnames(df_data[3])

  if (outputDir != "")
  {
    writeLines(paste("<table><tr>", sep=""))
  }
  ##########
  if (outputDir != "")
  {
    outputFile     = paste("corr_scatter_tc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }
  x = ggplot(df_data, aes_string(x=col1, y=col2)) + geom_point()
  grid::grid.draw(x)
  if (outputDir != "")
  {
    writeLines(paste("<td><img src='", outputSubdir, "/", outputFile, "'></td>", sep=""))
    writeLines("")
    writeLines("")
    dev.off()
  }
  ##########
  if (outputDir != "")
  {
    outputFile     = paste("corr_series_tc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }
  df_data_long = reshape(df_data, timevar="Subject", varying=c(col1, col2), v.name="value", direction="long")
  df_data_long[df_data_long$Subject==1,]$Subject = "Subject 1"
  df_data_long[df_data_long$Subject==2,]$Subject = "Subject 2"
  x = ggplot(df_data_long, aes(x=time, color=Subject, group=Subject)) +
      geom_line(aes_string(y="value"))
  grid::grid.draw(x)
  if (outputDir != "")
  {
    writeLines(paste("<td><img src='", outputSubdir, "/", outputFile, "'></td>", sep=""))
    writeLines("")
    writeLines("")
    dev.off()
  }
  ##########
  if (outputDir != "")
  {
    writeLines(paste("</tr></table>", sep=""))
  }

  if (prompt)
  {
    readline(prompt=paste("Showing plots of",  str_title))
    writeLines("\n...")
    writeLines("")
  }
}
