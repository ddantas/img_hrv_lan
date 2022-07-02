report_pdc <- function(res, title, confidence=0.95) {

  significance = 1 - confidence
  print(res)
  writeLines(paste("Testing columns ", title))
  writeLines("")

  writeLines("Regarding Granger causality from Subject 1 to Subject 2:\n")
  writeLines(paste("PDC value = ", res[1]$pdc))
  writeLines(paste("P-value = ", res[1]$p.value))

  writeLines("")

  if (!is.nan(res[1]$p.value))
  {
    if (res[1]$p.value < significance){
      writeLines(paste("P-value smaller than ", significance, ": THERE IS NOT statistical evidence of causality\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than ", significance, ": THERE IS statistical evidence of causality\n"), sep="")
    }
  }

  writeLines("Regarding Granger causality from Subject 2 to Subject 1:\n")
  writeLines(paste("PDC value = ", res[2]$pdc))
  writeLines(paste("P-value = ", res[2]$p.value))
  writeLines("")

  if (!is.nan(res[2]$p.value))
  {
    if (res[2]$p.value < significance){
      writeLines(paste("P-value smaller than ", significance, ": THERE IS NOT statistical evidence of causality\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than ", significance, ": THERE IS statistical evidence of causality\n"), sep="")
    }
  }
}