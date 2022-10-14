x = ggplot(df$subj1_linear, aes(x=Group, y=.data[[str_title]], color=Group))
x = ggplot(df$subj1_linear, aes(x=label, color=label))
grid::grid.draw(x)
x = ggplot(df$subj1_linear)
x = ggplot(df$subj1_linear) + geom_density(alpha = 0.2)
x = ggplot(df$subj1_linear, aes(.data[[label]])) + geom_density(alpha = 0.2)
x = ggplot(df$subj1_linear, aes(.data[[block]])) + geom_density(alpha = 0.2)
x = ggplot(df$subj1_linear, aes(.data[["block"]])) + geom_density(alpha = 0.2)
x = ggplot(df$subj1_linear, aes(.data[["label"]])) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["subj1_linear"]])) + geom_density(alpha = 0.2)



x = ggplot(df, aes(.data[["hr_subj1_linear"]])) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=label)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=Imitator)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=Model)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=IsImit)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=IsSync)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], color=Imitator)) + geom_density(alpha = 0.2)
x = ggplot(df_data, aes(.data[[str_title]], fill=Group)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], fill=block)) + geom_density(alpha = 0.2)
x = ggplot(df_data, aes(.data[[str_title]], fill=Group)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[[str_title]], fill=Group)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_linear"]], fill=block)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_nearest"]], fill=block)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj1_ecg_nearest"]], fill=block)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=block)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=Imitator)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=IsImit)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=IsSync)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=Model)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["hr_subj2_ecg_nearest"]], fill=label)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(.data[["d_hr_subj2_ecg_nearest"]], fill=label)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(log(.data[["d_hr_subj2_ecg_nearest"]]), fill=label)) + geom_density(alpha = 0.2)
x = ggplot(df, aes(log(.data[["d_hr_subj2_ecg_nearest"]]), fill=label)) + geom_density(alpha = 0.2) + scale_x_log10()
x = ggplot(df, aes(.data[["d_hr_subj2_ecg_nearest"]], fill=label)) + geom_density(alpha = 0.2) + scale_x_log10()
x = ggplot(df, aes(.data[["d_hr_subj2_ecg_nearest"]], fill=label)) + geom_density(alpha = 0.2) + scale_y_log10()
x = ggplot(df, aes(.data[["d_hr_subj2_ecg_nearest"]], fill=label)) + geom_density(alpha = 0.2) 





