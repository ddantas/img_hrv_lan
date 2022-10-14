source('./utils.R')

get_SI_imitation_pcent <- function(df_si, imit, sync) {
	
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

  return(mean(res))
}

get_SI_pcents <- function(df_si) {

  # "Synchrony/Imitation"
  imit_sync = get_SI_imitation_pcent(df_si, TRUE, TRUE)
  # "Synchrony/Non-Imitation"
  imit_notsync = get_SI_imitation_pcent(df_si, TRUE, FALSE)

  # "Non-Synchrony/Imitation"
  notimit_sync = get_SI_imitation_pcent(df_si, FALSE, TRUE)
  # "Non-Synchrony/Non-Imitation"
  notimit_notsync = get_SI_imitation_pcent(df_si, FALSE, FALSE)

  return(c(imit_sync, imit_notsync, notimit_sync, notimit_notsync))
}

create_SI_dataframe <- function(df, folder_names) {


  # "Synchrony/Imitation", "Synchrony/Non-Imitation", "Non-Synchrony/Imitation", 
  #       "Non-Synchrony/Non-Imitation"
  columns = c("S_I", "S_NI", "NS_I", "NS_NI")

  stats_df = data.frame(matrix(nrow=0, ncol=length(columns)))
  colnames(stats_df) <- columns

  for (f in folder_names) {

    isimit_si = df$IsImit[df['label'] == 'SI' & df['folder'] == f]
    issync_si = df$IsSync[df['label'] == 'SI' & df['folder'] == f]

    df_si = data.frame(IsImit=isimit_si, IsSync=issync_si)
    df_si[is.na(df_si)] <- FALSE

    stats = get_SI_pcents(df_si)

    stats_df[nrow(stats_df) + 1,] = stats

  }

  return(stats_df)
}

get_stats <- function(stats_df) {

  mean_si = mean(stats_df$S_I)
  sd_si = sd(stats_df$S_I)

  mean_sni = mean(stats_df$S_NI)
  sd_sni = sd(stats_df$S_NI)

  mean_nsi = mean(stats_df$NS_I)
  sd_nsi = sd(stats_df$NS_I)

  mean_nsni = mean(stats_df$NS_NI)
  sd_nsni = sd(stats_df$NS_NI)

  behaviour = c("S_I", "S_NI", "NS_I", "NS_NI")

  df = data.frame(Mean=c(mean_si, mean_sni, mean_nsi, mean_nsni),
                  SD=c(sd_si, sd_sni, sd_nsi, sd_nsni),
                  Behaviour=behaviour)

  return(df)
}
