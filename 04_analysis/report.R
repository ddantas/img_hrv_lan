report <- function(inputFile, outputFile, outputDir, df, df_stack, confidence=0.95, prompt=1)
{
  source('print_separator.R')
  source('generate_summary.R')
  source('plot_tc_distribution.R')
  #source('plot_tc_dispersion.R')
  source('report_tc_test.R')
  source('plot_correlationts.R')
  source('report_pdc.R')
  source('plot_pdc.R')
  source('script.R')
  #source('plot_power.R')
  
  outputFullname = paste(outputDir, "/", outputFile, sep="")
  sink(file=NULL)
  sink(file=outputFullname, append=FALSE, split=TRUE)
  #outputDir = ""

  ##########
  writeLines("<tt><pre>");
  print_separator()

  writeLines(paste("input file:  ", inputFile));
  writeLines(paste("output file: ", outputFile));
  writeLines(paste("output dir:  ", outputDir));
  writeLines("...")
  writeLines("")

  ##########
  print_separator()
  writeLines(paste("<h2>Descriptive statistics</h2>", sep=""))

  cols = c(seq(10, 17), seq(21, 28))
  #cols_disparsion = c(32, 36, 43, seq(44, 46), seq(57, 68))
  #cols_dispersion = c(37, 43, 46, 68)
  #min_num_col = 4
  #max_num_col = 68

  options(width = 200)

  ##########
  writeLines("...")
  writeLines("Descriptive statistics from each column")
  writeLines("")

  print(generate_summary(df[cols]))
  writeLines("")

  ##########
  #writeLines("...")
  #writeLines("Descriptive statistics from each column: Test - anisometropia")
  #writeLines("")

  #print(generate_summary(test[cols]))
  #writeLines("")

  ##########
  #writeLines("...")
  #writeLines("Descriptive statistics from each column: Control")
  #writeLines("")

  #print(generate_summary(control[cols]))
  #writeLines("")

  ##########
  #print_separator()
  #writeLines(paste("<h2>Sample size calculation</h2>", sep=""))

  #arr_diff = c(0.15, 0.30)
  #col_name = "estereop.log"
  #sd1 = sd(test   [, col_name])
  #sd2 = sd(control[, col_name])
  #arr_pow = c(0.8, 0.85, 0.9, 0.95)
  #sig = 0.05
  #type = "two.sample"
  #arr_alternative = c("two.sided", "greater")

  #writeLines(paste("Column considered: ", col_name, sep=""))
  #writeLines(paste("SD(Test)    = ", sd1, sep=""))
  #writeLines(paste("SD(Control) = ", sd2, sep=""))
  #writeLines("")
  
  #for (diff in arr_diff)
  #{
  #  for (alternative in arr_alternative)
  #  {
  #    str_title = paste("power_", diff, "_", type, "_", alternative, sep="")
  #    writeLines("...")
  #    writeLines(paste("Sample size calculation: diff = ", diff, sep=""))
  #    writeLines("")
  #    plot_power(outputFile, outputDir, str_title, diff, sd1, sd2, arr_pow, sig, type, alternative)
  #  }
  #}
  
  ##########
  print_separator()
  writeLines(paste("<h2>Distributions of Test and Control groups in original dataset</h2>", sep=""))

  #rows
  conditions = rbind(
    c("df$folder != ''",                                  "all",  "Subject 1", "Subject 2"),
    c("df$folder %in% c('b001', 'b002', 'b003', 'b004')", "ex01", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b009', 'b010', 'b011', 'b012')", "ex03", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b013', 'b014', 'b015', 'b016')", "ex04", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b017', 'b018', 'b019', 'b020')", "ex05", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b021', 'b022', 'b023', 'b024')", "ex06", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b025', 'b026', 'b027', 'b028')", "ex07", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b029', 'b030', 'b031', 'b032')", "ex08", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b033', 'b034', 'b035', 'b036')", "ex09", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b037', 'b038', 'b039', 'b040')", "ex10", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b041', 'b042', 'b043', 'b044')", "ex11", "Subject 1", "Subject 2") )
  
  prompt = 0
  #for (c in seq(1, dim(conditions)[1]))
  for (c in seq(1))
  {
    rows = eval(parse(text=conditions[c, 1]))
    exp_label = conditions[c, 2]
    str1 = conditions[c, 3]
    str2 = conditions[c, 4]
    
    for (i in seq(1, length(cols), by = 2))
    {
      col1 = names(df)[cols[i]]
      col2 = names(df)[cols[i + 1]]
      data1 = df[rows, col1, drop=FALSE]
      data2 = df[rows, col2, drop=FALSE]
      str_title = paste("exp_", exp_label, "__", col1, "_vs_", col2, sep="")
      writeLines("...")
      writeLines(paste("<h3>", str_title, "</h3>", sep=""))

      report_tc_test(data1, data2, str_title, confidence=0.95, str1, str2)
      #writeLines(paste("plot_test_control: ", names(df)[i]))
      plot_tc_distribution(data1, data2, str_title, prompt, outputDir, "Heart rate", str1, str2)
    }
  }
  ##########
  print_separator()
  writeLines(paste("<h2>Distributions of Test and Control groups in stacked dataset</h2>", sep=""))

  #rows
  conditions = rbind(
    c("df_stack$Gender == 'M'", "df_stack$Gender == 'F'", "gender", "Male", "Female", "male", "female") )

  #cols
  cols_stack = c(seq(10, 13), seq(16, 19))

  prompt = 0
  #cols = c(60, 61)
  for (c in seq(1, dim(conditions)[1]))
  {
    rows1 = eval(parse(text=conditions[c, 1]))
    rows2 = eval(parse(text=conditions[c, 2]))
    exp_label = conditions[c, 3]
    str1 = conditions[c, 4]
    str2 = conditions[c, 5]
    label1 = conditions[c, 6]
    label2 = conditions[c, 7]
    
    for (i in seq(1, length(cols_stack)))
    {
      col_name = names(df_stack)[cols_stack[i]]
      data1 = df_stack[rows1, col_name, drop=FALSE]
      data2 = df_stack[rows2, col_name, drop=FALSE]
      str_title = paste("exp_", exp_label, "__", col_name, "__", label1, "_vs_", label2, sep="")
      writeLines("...")
      writeLines(paste("<h3>", str_title, "</h3>", sep=""))

      report_tc_test(data1, data2, str_title, confidence=0.95, str1, str2)
      plot_tc_distribution(data1, data2, str_title, prompt, outputDir, "Heart rate", str1, str2)
    }
  }

  ##########
  print_separator()

  conditions = rbind(
    c("df$folder != ''"                                 , "all"),
    c("df$folder %in% c('b001', 'b002', 'b003', 'b004')", "ex01"),
    c("df$folder %in% c('b009', 'b010', 'b011', 'b012')", "ex03"),
    c("df$folder %in% c('b013', 'b014', 'b015', 'b016')", "ex04"),
    c("df$folder %in% c('b017', 'b018', 'b019', 'b020')", "ex05"),
    c("df$folder %in% c('b021', 'b022', 'b023', 'b024')", "ex06"),
    c("df$folder %in% c('b025', 'b026', 'b027', 'b028')", "ex07"),
    c("df$folder %in% c('b029', 'b030', 'b031', 'b032')", "ex08"),
    c("df$folder %in% c('b033', 'b034', 'b035', 'b036')", "ex09"),
    c("df$folder %in% c('b037', 'b038', 'b039', 'b040')", "ex10"),
    c("df$folder %in% c('b041', 'b042', 'b043', 'b044')", "ex11") )

  writeLines(paste("<h2>Correlation between time series on different phases of the experiment</h2>", sep=""))

  cols = c(seq(10, 17, 2))
  labels = unique(df$label)

  for (j in cols) {

    str_title = names(df)[j]
    str_title = gsub("hr_subj1_", "", str_title)

    writeLines(paste("<h3>Correlation for ", str_title, " data</h3>", sep=""))
    writeLines("...")

    for (c in seq(1, dim(conditions)[1])) {

      rows = eval(parse(text=conditions[c, 1]))
      exp = conditions[c, 2]
      df_data = df[rows, ]
      col1 = names(df)[j]
      col2 = names(df)[j+1]
      data1 = df_data[, c(col1, "label")]
      data2 = df_data[, c(col2, "label")]
      str_title = paste(str_title, exp)
      plot_correlationts(data1, data2, labels, exp, str_title, outputDir)

    }
  }

  ##########
  print_separator()

  cols = c(seq(10, 17), seq(21, 28))
  conditions = rbind(
    c("df$folder != ''",                                  "all",  "Subject 1", "Subject 2"),
    c("df$folder %in% c('b001', 'b002', 'b003', 'b004')", "ex01", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b009', 'b010', 'b011', 'b012')", "ex03", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b013', 'b014', 'b015', 'b016')", "ex04", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b017', 'b018', 'b019', 'b020')", "ex05", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b021', 'b022', 'b023', 'b024')", "ex06", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b025', 'b026', 'b027', 'b028')", "ex07", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b029', 'b030', 'b031', 'b032')", "ex08", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b033', 'b034', 'b035', 'b036')", "ex09", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b037', 'b038', 'b039', 'b040')", "ex10", "Subject 1", "Subject 2"),
    c("df$folder %in% c('b041', 'b042', 'b043', 'b044')", "ex11", "Subject 1", "Subject 2") )
  
  # for (c in seq(1, dim(conditions)[1]))
  for (c in seq(1))
  {
    rows = eval(parse(text=conditions[c, 1]))
    exp_label = conditions[c, 2]
    str1 = conditions[c, 3]
    str2 = conditions[c, 4]
    
    for (i in seq(1, length(cols), by = 2))
    {
      col1 = names(df)[cols[i]]
      col2 = names(df)[cols[i + 1]]
      data1 = df[rows, col1, drop=FALSE]
      data2 = df[rows, col2, drop=FALSE]
      str_title = paste("exp_", exp_label, "__", col1, "_vs_", col2, sep="")
      writeLines("...")
      writeLines(paste("<h3>", str_title, "</h3>", sep=""))

      res = plot_pdc(data1, data2, str_title, outputDir)

      report_pdc(res, str_title)
    }
  }

  ##########

  ###plot_tc_dispersion(test, control, cols_dispersion, prompt, outputDir)
  #plot_tc_dispersion(test, control, cols, prompt, outputDir)


  

  sink(file=NULL)
}
