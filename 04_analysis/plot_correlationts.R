plot_correlationts <- function(data1, data2, labels, exp, str_title, outputDir="") {

  outputFullname = ""
  outputFile     = ""
  outputSubdir   = "plot_correlationts"
  
  if (outputDir != "")
  {
    writeLines(paste("<table><tr>", sep=""))
  }

  df_corr = data.frame(matrix(nrow=0, ncol=3))

  for (l in labels) {

    data1_label = data1[data1["label"] == l, 1]
    data2_label = data2[data2["label"] == l, 1]
    # df_label = df_data[df_data["label"] == l, ]
    # data1 = df_label[, cols[1]]
    # data2 = df_label[, cols[2]]

    df_res = data.frame(data1_label, data2_label)
    names(df_res) = c("subj1", "subj2")

    if (nrow(df_res) > 0) {
      corr = get_correlationts(df_res)
      df_corr = rbind(df_corr, c(corr, l, exp))
    }
  }

  names(df_corr) = c("corr", "label", "experiment")
    
  if (outputDir != "")
  {
    outputFile     = paste("hist_bar_corr_", str_title, ".png", sep="")
    outputFullname = paste(outputDir, "/", outputSubdir, "/", outputFile, sep="")
    png(outputFullname, width=640);
  }

  x = ggplot(df_corr, aes(.data$label, .data$corr, fill=label)) +
    geom_bar(stat='identity')
  grid::grid.draw(x)

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
}