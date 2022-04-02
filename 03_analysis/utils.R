load_data <- function(filename){

	data = read.table(filename, header=TRUE, sep='	')

	return(data)
}
