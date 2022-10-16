# Print table in html format.
# Input:
#   tab: Table to print
#   cs: color specifier function
print_table_html <- function(tab, cs=NULL)
{
  col_titles = names(tab)
  w = length(tab)
  h = length(tab[[1]])

  writeLines("<table border=1>")

  if (h > 0)
  {
    writeLines("  <tr>")
    for (j in seq(1, w))
    {
      writeLines(paste0("    <td>", col_titles[j], "</td>"))
    }
    writeLines("  </tr>")

    for (i in seq(1, h))
    {
      writeLines("  <tr>")
      for (j in seq(1, w))
      {
        d = tab[[j]][[i]]
        s = paste(d)
        if (!is.null(cs) & is.numeric(d))
        {
          writeLines(paste0("    <td><div style='color:", cs(d), "'>", s, "</div></td>"))
        }
        else
        {
          writeLines(paste0("    <td>", s, "</td>"))
        }
      }
      writeLines("  </tr>")
    }
  }
  writeLines("</table>")

}
