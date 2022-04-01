
load_data <- function(filename){

	data = read.table(filename, header=TRUE, sep='	')

	return(data)
}

get_synchrony_stats <- function(filename, imit, sync) {

	# select what values you want based on the truth values of 'imit' and 'sync'

	df = load_data(filename)

	isimit_si = df$IsImit[df['label'] == 'SI']
	issync_si = df$IsSync[df['label'] == 'SI']

	df_si = data.frame(IsImit=isimit_si, IsSync=issync_si)
	
	# SANITY CHECKING CODE
	# l = c(42, 43, 44)
	# df_si['IsSync'][l,] = TRUE
	# nrows = 1:nrow(df_si)
	# aux = nrows[!(nrows %in% l)]	
	# df_si['IsSync'][aux, ] = FALSE
	# print(df_si)

	# get a list of indexes where values are 'IsImit' == imit and 'IsSync' == sync
	indexes_true = intersect(which(df_si['IsImit'] == imit), which(df_si['IsSync'] == sync))

	# create a vector with 1's only on indexes that match our conditions
	res = rep(0, nrow(df_si))
	res[indexes_true] = 1

	return(c(mean(res), sd(res)))
}
