source('./utils.R')

get_SI_stats <- function(df_si, imit, sync) {
	
  # SANITY CHECKING CODE
  # l = c(42, 43, 44)
  # df_si['IsSync'][l,] = TRUE
  # nrows = 1:nrow(df_si)
  # aux = nrows[!(nrows %in% l)]
  # df_si['IsSync'][aux, ] = FALSE

  # get a list of indexes where values of 'IsImit' == imit and 'IsSync' == sync
  indexes_true = intersect(which(df_si['IsImit'] == imit), which(df_si['IsSync'] == sync))

  # create a vector with 1's only on indexes that match our conditions
  res = rep(0, nrow(df_si))
  res[indexes_true] = 1

  return(c(mean(res), sd(res)))
}

create_SI_dataframe <- function(df) {

  isimit_si = df$IsImit[df['label'] == 'SI']
  issync_si = df$IsSync[df['label'] == 'SI']

  df_si = data.frame(IsImit=isimit_si, IsSync=issync_si)
  df_si[is.na(df_si)]  <- FALSE

  imit_sync = get_SI_stats(df_si, TRUE, TRUE)
  imit_notsync = get_SI_stats(df_si, TRUE, FALSE)

  notimit_sync = get_SI_stats(df_si, FALSE, TRUE)
  notimit_notsync = get_SI_stats(df_si, FALSE, FALSE)

  names = c("Synchrony/Imitation", "Synchrony/Non-Imitation", "Non-Synchrony/Imitation", 
        "Non-Synchrony/Non-Imitation")

  stats_df = data.frame(Mean=c(imit_sync[1], imit_notsync[1], notimit_sync[1], notimit_notsync[1]),
        SD=c(imit_sync[2], imit_notsync[2], notimit_sync[2], notimit_notsync[2]), Behaviour=names)

  return(stats_df)
}
