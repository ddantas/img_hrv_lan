
load_data <- function(filename){
	data = read.table(filename, header=TRUE, sep='	')

	return(data)
}

get_synchrony_stats <- function(filename) {

	df = load_data(filename)

	isimit_si = df['IsImit'][df['label'] == 'SI']
	issync_si = df['IsSync'][df['label'] == 'SI']

	df_si = data.frame(IsImit=isimit_si, IsSync=issync_si)

	# change T to 1, F and NA to 0 in 'IsImit'

	df_si['IsSync' == 'T' & 'IsImit' == 'T'] = 1
	df_si[!('IsSync' == 'T' & 'IsImit' == 'T')] = 0
	
	imit_sync = df_si['IsImit'][df_si['IsSync' == 'T']]
	imit_notsync = df_si['IsImit'][df_si['IsSync' == 'F']]	

	# change T and NA to 0, F to 1 in 'IsImit'
	notimit_sync = df_si['IsImit'][df_si['IsSync' == 'T']]	
	notimit_notsync = df_si['IsImit'][df_si['IsSync' == 'F']]

	# df_sd_si = sd(isimit_si)
	# df_mean_si = mean(isimit_si)

	# return(c(df_sd_si, df_mean_si, df_sd_ii, df_mean_ii))
}
