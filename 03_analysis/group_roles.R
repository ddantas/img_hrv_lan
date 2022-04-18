source('./utils.R')

normalize_dataset <- function(filename) {

	df = load_data(filename)

	subj1_cols = c("folder", "block", "Subject", "label", "time", "IsImit", "IsSync", "Role", 
            "hr_subj1_linear", "hr_subj1_nearest", "hr_subj1_ecg_linear", "hr_subj1_ecg_nearest", 
            "msg1")

	subj2_cols = c("folder", "block", "Subject", "label", "time", "IsImit", "IsSync", "Role", 
            "hr_subj2_linear", "hr_subj2_nearest", "hr_subj2_ecg_linear", "hr_subj2_ecg_nearest", 
            "msg2")

	columns = c("folder", "block", "Subject", "label", "time", "IsImit", "IsSync", "Role", 
            "hr_subj_linear", "hr_subj_nearest", "hr_subj_ecg_linear", "hr_subj_ecg_nearest", 
            "msg")

	df['Role'] = NA
	df['Subject'] = NA
	subj1_id = rep(1, nrow(df))
	subj2_id = rep(2, nrow(df))

	subj1_imitator_indexes = which(df["Imitator"] == 1)
	subj2_imitator_indexes = which(df["Imitator"] == 2)
	
	subj1_role = df$Imitator
	subj1_role[subj1_imitator_indexes] = "Imitator"
	subj1_role[subj2_imitator_indexes] = "Model"

	subj2_role = df$Imitator
	subj2_role[subj2_imitator_indexes] = "Imitator"
	subj2_role[subj1_imitator_indexes] = "Model"

	df_subj1 = df[subj1_cols]
	df_subj1['Role'] = subj1_role
	df_subj1['Subject'] = subj1_id

	df_subj2 = df[subj2_cols]
	df_subj2['Role'] = subj2_role
	df_subj2['Subject'] = subj2_id

	final_df = data.frame(matrix(nrow=0, ncol=length(columns)))

	for (i in seq(1, nrow(df))) {
		final_df[2*(i-1)+1, ] = df_subj1[i, ]
		final_df[2*(i-1)+2, ] = df_subj2[i, ]
	}

	colnames(final_df) = columns
	write.table(final_df, file='grouped_roles.tsv', sep="\t", col.names=NA)
}