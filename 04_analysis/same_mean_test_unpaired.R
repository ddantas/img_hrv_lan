same_mean_test_unpaired <- function(x, y, str_title, confidence=0.95, label1="Test", label2="Control")
{
  significance = 1 - confidence

  pad = max(nchar(label1), nchar(label2))
  label1_pad = str_pad(label1, pad, side="right")
  label2_pad = str_pad(label2, pad, side="right")
  writeLines(paste("Testing if column", str_title, "have the same mean..."))
  writeLines(paste(label1_pad, " (Mean &plusmn; SD) = (", mean(x), " &plusmn; ", sd(x), ")", sep=""))
  writeLines(paste(label2_pad, " (Mean &plusmn; SD) = (", mean(y), " &plusmn; ", sd(y), ")", sep=""))

  result <- list(p.value=NaN)
  tryCatch(
    expr = {
      result = t.test(x, y, conf.level=confidence, var.equal=TRUE, paired=FALSE)
    },
    error = function(e){
      writeLines(paste("All values are identical"))
    }
  )
  writeLines("Student unpaired equal variances t-test (parametric)")
  writeLines(paste("P-value = ", result$p.value))
  if (!is.nan(result$p.value))
  {
    if (result$p.value < significance){
      writeLines(paste("P-value smaller than", significance, ": Sample means are DIFFERENT.\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than", significance, ": Sample means are EQUAL.\n"), sep="")
    }
  }
  ##########
  result2 <- list(p.value=NaN)
  tryCatch(
    expr = {
      result2 = t.test(x, y, conf.level=confidence, var.equal=FALSE, paired=FALSE)
    },
    error = function(e){
      writeLines(paste("All values are identical"))
    }
  )
  writeLines("Welch unpaired unequal variances t-test (parametric)")
  writeLines(paste("P-value = ", result2$p.value))
  if (!is.nan(result2$p.value))
  {
    if (result2$p.value < significance){
      writeLines(paste("P-value smaller than", significance, ": Sample means are DIFFERENT.\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than", significance, ": Sample means are EQUAL.\n"), sep="")
    }
  }
  ##########
  writeLines("Mann-Whitney U-test (nonparametric)")
  result3 = wilcox.test(x, y, paired=FALSE)
  writeLines(paste("P-value = ", result3$p.value))
  if (!is.nan(result3$p.value))
  {
    if (result3$p.value < significance){
      writeLines(paste("P-value smaller than", significance, ": Sample means are DIFFERENT.\n"), sep="")
    }
    else{
      writeLines(paste("P-value greater than", significance, ": Sample means are EQUAL.\n"), sep="")
    }
  }
}


