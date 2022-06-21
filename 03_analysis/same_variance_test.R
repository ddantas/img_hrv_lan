same_variance_test <- function(x, y, str_title, confidence=0.95)
{
  significance = 1 - confidence

  writeLines(paste("Testing if ", str_title, " have the same variance...", sep=""))

  result <- list(estimate=NaN, conf.int=c(NaN, NaN), p.value=NaN)
  tryCatch(
    expr = {
      result <- var.test(x, y)
    },
    error = function(e){
      writeLines(paste("All values are identical"))
    }
  )

  writeLines(paste("Ratio = ", result$estimate))
  writeLines(paste("Interval = [", result$conf.int[[1]], ", ", result$conf.int[[2]], "]"))

  writeLines("Fisher f-test")
  writeLines(paste("P-value = ", result$p.value))
  if (!is.nan(result$p.value))
  {
    if (result$p.value < significance){
      writeLines(paste("P-value smaller than", significance, ": Sample variances are DIFFERENT.\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than", significance, ": Sample variances are EQUAL.\n"), sep="")
    }
  }
}


