normality_test <- function(x, title, confidence=0.95)
{
  significance = 1 - confidence
  
  writeLines(paste("Testing if column ", title, " has normal distribution...", sep="")) 

  result <- list(statistic=NaN, p.value=NaN)
  tryCatch(
    expr = {
      result <- ad.test(x)
    },
    error = function(e){
      writeLines(paste(e))
    }
  )

  writeLines(paste("W-statistic = ", result$statistic))
  writeLines(paste("P-value = ", result$p.value))
  if (!is.nan(result$p.value))
  {
    if (result$p.value < significance){
      writeLines(paste("P-value smaller than ", significance, ": Distribution IS NOT NORMAL\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than ", significance, ": Distribution IS NORMAL\n"), sep="")
    }
  }
}
