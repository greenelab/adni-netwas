# Generate QQ plots from ADNI VEGAS p-values to investigate deviation from
# uniform. Uses the gap library.
# docs: http://www.inside-r.org/packages/cran/gap/docs/qqunif

require(gap)

data = read.csv("combined-results.csv")

pdf("figures/vegas-ad1-qq.pdf", height=4, width=4)
qqunif(data$VEGAS_AD1, ci=T)
dev.off()


pdf("figures/vegas-ad2-qq.pdf", height=4, width=4)
qqunif(data$VEGAS_AD2, ci=T)
dev.off()
