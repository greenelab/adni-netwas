library("ggplot2")

data = read.delim("results-proc.txt")

# We'll use this for error bars
stat_sum_df <- function(fun, geom="crossbar", ...) {
  stat_summary(fun.data=fun, colour="red", geom=geom, width=0.2, ...)
}

pdf("figures/Figure2.pdf", width=5, height=6)
ggplot(data, aes(x=Method, AUC)) + geom_point(stat="identity", position="jitter")  + stat_sum_df("mean_cl_boot", geom = "errorbar")  + facet_grid( GWAS ~ . ) + theme_bw()
dev.off()
