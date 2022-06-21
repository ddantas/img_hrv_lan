plot_tc_distribution <- function(df_test, df_control, str_title, prompt=1, outputDir="")
{
  ## Reference:
  ## https://stackoverflow.com/questions/3541713/how-to-plot-two-histograms-together-in-r
  
  outputFullname = ""
  outputFile     = ""
  outputSubdir   = "plot_tc_distribution"

  colnames(df_test) = "x"
  colnames(df_control) = "x"

  if (outputDir != "")
  {
    writeLines(paste("<table><tr>", sep=""))
  }
  ##########
  if (outputDir != "")
  {
    outputFile     = paste("hist_smooth_tc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }
  df_test$Group = "Test"
  df_control$Group = "Control"
  #df_test$Group = "Anisometropia"
  #df_control$Group = "Controle"
  df_data <- rbind(df_test, df_control)
  x = ggplot(df_data, aes(.data$x, fill=Group)) +
    geom_density(alpha = 0.2)
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
    outputFile     = paste("hist_bar_tc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }
  df_test$Group = "Test"
  df_control$Group = "Control"
  #df_test$Group = "Anisometropia"
  #df_control$Group = "Controle"
  df_data <- rbind(df_test, df_control)
  x = ggplot(df_data, aes(.data$x, fill=Group)) +
    geom_histogram(alpha = 0.5, position = 'identity')
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
    outputFile     = paste("boxplot_tc_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }
  df_test$Group = "Test"
  df_control$Group = "Control"
  #df_test$Group = "Anisometropia"
  #df_control$Group = "Controle"
  df_data <- rbind(df_test, df_control)
  x = ggplot(df_data, aes(x=Group, y=.data$x, color=Group)) + 
    geom_boxplot()
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
