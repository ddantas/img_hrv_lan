report_pdc_new <- function(res, pos, subj, title, confidence=0.95) {

  significance = 1 - confidence

  writeLines(paste("Testing columns ", title))

  pval = res$p.value[pos[1], pos[2]]
  pdc  = res$pdc[pos[1], pos[2]]
  lag  = res$lag
  
  writeLines("")
  writeLines(paste("Regarding Granger causality from Subject ", subj[1], " to Subject ", subj[2], ":\n", sep = ""))
  writeLines(paste("Lag = ", lag))
  writeLines(paste("PDC value = ", pdc))
  writeLines(paste("P-value = ", pval))
  writeLines("")

  if (!is.nan(pval))
  {
    if (pval < significance){
      writeLines(paste("P-value smaller than ", significance, ": THERE IS statistical evidence of causality\n", sep=""))
    }
    else{
      writeLines(paste("P-value greater than ", significance, ": THERE IS NOT statistical evidence of causality\n", sep=""))
    }
  }
}
