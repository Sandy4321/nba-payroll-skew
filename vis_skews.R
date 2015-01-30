library(ggplot2)
librar(reshape2)
library(dplyr)

perf_skew <- read.csv("skew_record.csv")
ggplot(perf_skew, aes(x=skew, y=reg_season_wp)) + geom_point()

perf_skew_clean <- perf_skew[which(!is.na(perf_skew$skew)),]
cor.test(perf_skew_clean$skew, perf_skew_clean$reg_season_wp)
cor.test(perf_skew_clean$skew, perf_skew_clean$reg_season_wp, 
    method="kendall")
cor.test(perf_skew_clean$skew, perf_skew_clean$reg_season_wp, 
    method="spearman")

ggplot(perf_skew, aes(x=skew, y=playoff_wp)) + geom_point()
perf_skew_clean_playoff <- perf_skew[which(!is.na(perf_skew_clean$playoff_wp)),]
cor.test(perf_skew_clean_playoff$skew, perf_skew_clean_playoff$reg_season_wp)
cor.test(perf_skew_clean_playoff$skew, perf_skew_clean_playoff$reg_season_wp, 
    method="kendall")
cor.test(perf_skew_clean_playoff$skew, perf_skew_clean_playoff$reg_season_wp, 
    method="spearman")

ggplot(perf_skew_clean_playoff, aes(x=reg_season_wp, y=playoff_wp)) + geom_point()
cor.test(perf_skew_clean_playoff$reg_season_wp, perf_skew_clean_playoff$playoff_wp)
cor.test(perf_skew_clean_playoff$reg_season_wp, perf_skew_clean_playoff$playoff_wp,
    method="kendall")
cor.test(perf_skew_clean_playoff$reg_season_wp, perf_skew_clean_playoff$playoff_wp,
    method="spearman")