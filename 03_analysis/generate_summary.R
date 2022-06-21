generate_summary <- function(tab)
{

    result = NULL
    for (i in seq(1, length(tab)))
    {
        one_row = summary(tab[[i]])
        one_sd  = sd(tab[[i]])
        names(one_sd) = "SD"
        one_len  = length(tab[[i]])
        names(one_len) = "Length"
        one_row = c(one_len, one_row, one_sd)

        result = cbind(result, one_row)
    }

    result = as.data.frame(t(result), row.names=names(tab))

    return(result)

}