"""650 M3 (NAs, outliers, correlation): NCBirths2004.csv + airquality + mtcars."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]
LOAD = '''library(readr)
library(dplyr)
library(tidyr)
births <- read_csv("NCBirths2004.csv", show_col_types = FALSE)'''

A = [
N(1, 1, "Count missing values", "Count NAs in every column of `airquality` and in the births data.", LOAD, "",
  '''# === Complete example — read and run ===
colSums(is.na(airquality))
sum(is.na(births))                     # the births data have no NAs
mean(is.na(airquality$Ozone))          # share of missing Ozone values''', [("na_ozone", "sum(is.na(airquality$Ozone))", 0)]),
N(2, 2, "Create NAs for practice", "Copy the births data and put NAs in on purpose (as in the lesson), then count them.", LOAD,
  '''b_ill <- births
b_ill[1, ] <- ___                       # whole first row missing
b_ill[2, "Tobacco"] <- NA
b_ill[3, "___"] <- NA                   # one missing Weight
colSums(is.na(___))
sum(is.na(b_ill))''',
  '''b_ill <- births
b_ill[1, ] <- NA                        # whole first row missing
b_ill[2, "Tobacco"] <- NA
b_ill[3, "Weight"] <- NA                # one missing Weight
colSums(is.na(b_ill))
sum(is.na(b_ill))''', [("total_na", "sum(is.na(b_ill))", 0)]),
N(3, 3, "drop_na(): all columns vs one column", "Compare nrow() after drop_na() on all columns and after drop_na(Weight). Then compute mean Weight with na.rm = TRUE.", LOAD,
  "# Write all your code here\n",
  '''n_all <- nrow(drop_na(b_ill))
n_weight <- nrow(drop_na(b_ill, Weight))
c(original = nrow(b_ill), drop_all = n_all, drop_weight = n_weight)
round(mean(b_ill$Weight, na.rm = TRUE), 2)''', [("n_all", "n_all", 0), ("n_weight", "n_weight", 0)]),
N(4, 4, "Imputing Ozone", "An analyst must report mean Ozone per month from `airquality`. Compare (a) dropping NAs, (b) imputing the overall median, (c) imputing each month's median. Which choice changes the monthly means most?", "library(dplyr)\nlibrary(tidyr)",
  '''# 1. Monthly mean Ozone with na.rm = TRUE
# 2. replace_na() with the overall median, then monthly means (Ozone is integer: use as.numeric() first)
# 3. Group-wise median imputation (group_by(Month) + mutate(if_else(is.na(...))))
# 4. Compare the three tables and comment
''',
  '''a <- airquality |> group_by(Month) |> summarise(drop = mean(Ozone, na.rm = TRUE))
med_all <- median(airquality$Ozone, na.rm = TRUE)
b <- airquality |> mutate(Ozone = replace_na(as.numeric(Ozone), med_all)) |>
  group_by(Month) |> summarise(overall_median = mean(Ozone))
c2 <- airquality |> group_by(Month) |>
  mutate(Ozone = as.numeric(Ozone),
         Ozone = if_else(is.na(Ozone), median(Ozone, na.rm = TRUE), Ozone)) |>
  summarise(month_median = mean(Ozone))
cmp <- a |> left_join(b, by = "Month") |> left_join(c2, by = "Month")
round(as.data.frame(cmp), 2)
# June has the most missing values, so imputing one overall median changes June the most.''', [("june_drop", "mean(airquality$Ozone[airquality$Month == 6], na.rm = TRUE)", 2)]),
N(5, 5, "When is dropping NAs risky?", "With `set.seed(5)`, make Ozone values missing completely at random (20%) vs. missing only when Ozone > 60. Compare the mean of the observed values with the true mean of the complete cases. Write 3 sentences.", "library(dplyr)\noz <- airquality$Ozone[!is.na(airquality$Ozone)]",
  '''# 1. true <- mean(oz)
# 2. MCAR: a random 20% become NA, mean of the rest
# 3. Not at random: values > 60 become NA, mean of the rest
# 4. Compare the two biases
# 5. Report (3 sentences as comments):
''',
  '''true <- mean(oz)
set.seed(5)
mcar <- oz; mcar[sample(length(oz), round(0.2 * length(oz)))] <- NA
mnar <- oz; mnar[oz > 60] <- NA
bias <- c(mcar = mean(mcar, na.rm = TRUE) - true, mnar = mean(mnar, na.rm = TRUE) - true)
round(c(true = true, bias), 2)
# When values are missing at random, dropping them barely changes the mean.
# When high values are the ones that go missing, the mean of what is left is far too low.
# Before dropping NAs, ask WHY the data are missing.''', [("bias_mnar", "bias[['mnar']]", 2)]),
]

B = [
N(6, 1, "1.5 × IQR outliers", "Find outliers in birth Weight with the 1.5·IQR rule.", LOAD, "",
  '''# === Complete example — read and run ===
q1 <- quantile(births$Weight, 0.25); q3 <- quantile(births$Weight, 0.75)
iqr <- IQR(births$Weight)
low <- q1 - 1.5 * iqr; high <- q3 + 1.5 * iqr
c(low = unname(low), high = unname(high))
n_out_iqr <- sum(births$Weight < low | births$Weight > high)
n_out_iqr
boxplot(births$Weight, horizontal = TRUE, col = "lightblue")''', [("n_out_iqr", "n_out_iqr", 0)]),
N(7, 2, "3 SD outliers", "Use the mean ± 3 SD rule on Weight and compare with Q6.", LOAD,
  '''m <- mean(births$___); s <- ___(births$Weight)
lower <- m - ___ * s; upper <- m + 3 * s
n_out_sd <- sum(births$Weight < lower | births$Weight ___ upper)
round(c(lower, upper), 1); n_out_sd''',
  '''m <- mean(births$Weight); s <- sd(births$Weight)
lower <- m - 3 * s; upper <- m + 3 * s
n_out_sd <- sum(births$Weight < lower | births$Weight > upper)
round(c(lower, upper), 1); n_out_sd''', [("n_out_sd", "n_out_sd", 0)]),
N(8, 3, "Remove outliers with filter()", "Create `births_clean` without the 1.5·IQR outliers using filter(), and compare n, mean and SD before and after.", LOAD,
  "# Write all your code here\n",
  '''births_clean <- births |> filter(Weight >= low, Weight <= high)
rbind(before = c(n = nrow(births), mean = mean(births$Weight), sd = sd(births$Weight)),
      after = c(n = nrow(births_clean), mean = mean(births_clean$Weight), sd = sd(births_clean$Weight)))''', [("n_clean", "nrow(births_clean)", 0)]),
N(9, 4, "Outliers by group", "A midwife asks whether smokers have more low-weight outliers. Apply the 1.5·IQR rule within each Smoker group (group_by + mutate) and count outliers per group.", LOAD,
  '''# 1. group_by(Smoker) |> mutate(low = ..., high = ..., outlier = ...)
# 2. count outliers per group and their share
# 3. Boxplot of Weight by Smoker
# 4. Answer for the midwife (comment):
''',
  '''flagged <- births |>
  group_by(Smoker) |>
  mutate(low = quantile(Weight, 0.25) - 1.5 * IQR(Weight),
         high = quantile(Weight, 0.75) + 1.5 * IQR(Weight),
         outlier = Weight < low | Weight > high) |>
  ungroup()
flagged |> group_by(Smoker) |> summarise(n = n(), outliers = sum(outlier), share = mean(outlier))
boxplot(Weight ~ Smoker, data = births, col = "lightblue")
# Answer: compare the shares above; counts alone mislead because the groups differ in size.''', [("out_smokers", "sum(dplyr::filter(flagged, Smoker == 'Yes')$outlier)", 0)]),
N(10, 5, "Should we remove them?", "Low birth weights are real, important cases. Compare the mean weight of smokers vs non-smokers with and without IQR outliers, and run a t test in both cases. Write a 3-sentence recommendation.", LOAD,
  '''# 1. Mean Weight by Smoker: all data and births_clean
# 2. t.test(Weight ~ Smoker) on both
# 3. Did removing outliers change the conclusion?
# 4. Recommendation (3 sentences as comments):
''',
  '''all_means <- tapply(births$Weight, births$Smoker, mean)
clean_means <- tapply(births_clean$Weight, births_clean$Smoker, mean)
round(rbind(all = all_means, clean = clean_means), 1)
p_all <- t.test(Weight ~ Smoker, data = births)$p.value
p_clean <- t.test(Weight ~ Smoker, data = births_clean)$p.value
signif(c(p_all = p_all, p_clean = p_clean), 3)
# Non-smokers have heavier babies on average, with or without the outliers.
# Removing outliers changes the size of the difference a little but not the conclusion.
# Report the analysis with all data, and mention the check without outliers - do not delete real cases.''', [("p_all", "p_all", 6)]),
]

C = [
N(11, 1, "Correlation with cor()", "Correlations among mpg, wt, hp and disp (`mtcars`).", "", "",
  '''# === Complete example — read and run ===
v <- mtcars[, c("mpg", "wt", "hp", "disp")]
round(cor(v), 3)
plot(mtcars$wt, mtcars$mpg, pch = 16)''', [("r_mpg_wt", "cor(mtcars$mpg, mtcars$wt)", 3)]),
N(12, 2, "Missing values in cor()", "cor() returns NA when a column has NAs. Fix it with `use =`.", "",
  '''aq <- airquality[, c("Ozone", "Solar.R", "Wind", "Temp")]
cor(aq)                                       # NAs appear
round(cor(aq, use = "___"), 3)               # only rows complete in ALL columns
round(cor(aq, use = "___"), 3)               # complete rows per pair''',
  '''aq <- airquality[, c("Ozone", "Solar.R", "Wind", "Temp")]
cor(aq)                                       # NAs appear
round(cor(aq, use = "complete.obs"), 3)      # only rows complete in ALL columns
round(cor(aq, use = "pairwise.complete.obs"), 3)  # complete rows per pair''', [("r_oz_temp", "cor(airquality$Ozone, airquality$Temp, use = 'complete.obs')", 3)]),
N(13, 3, "Spearman vs Pearson", "Compute Pearson and Spearman correlations of Ozone and Wind (complete cases) and test both with cor.test(). Why do they differ?", "",
  "# Write all your code here\n",
  '''aq2 <- na.omit(airquality[, c("Ozone", "Wind")])
round(c(pearson = cor(aq2$Ozone, aq2$Wind), spearman = cor(aq2$Ozone, aq2$Wind, method = "spearman")), 3)
signif(cor.test(aq2$Ozone, aq2$Wind)$p.value, 3)
signif(suppressWarnings(cor.test(aq2$Ozone, aq2$Wind, method = "spearman"))$p.value, 3)
# Spearman uses ranks, so it handles the curved (non-linear) pattern and the outliers better.''', [("spearman", "cor(aq2$Ozone, aq2$Wind, method = 'spearman')", 3)]),
N(14, 4, "Weight and gestation", "A hospital asks how strongly gestation week relates to birth weight. Make a scatterplot, compute r, test it, and say what share of the variation in weight is explained (r²).", LOAD,
  '''# 1. Scatterplot of Weight vs Gestation
# 2. r and cor.test()
# 3. r^2 as a percentage
# 4. Answer for the hospital (comment):
''',
  '''plot(births$Gestation, births$Weight, pch = 16, col = rgb(0, 0, 1, 0.3))
r <- cor(births$Gestation, births$Weight)
round(r, 3)
signif(cor.test(births$Gestation, births$Weight)$p.value, 3)
round(100 * r^2, 1)
# Answer: a weak-to-moderate positive relationship; gestation explains only about 12% of the variation in weight.''', [("r", "r", 3)]),
N(15, 5, "Correlation is not causation", "Using `mtcars`, find the variable most correlated with mpg (in absolute value). Then show that cyl and disp are also highly correlated with each other, and explain why a strong r between mpg and one variable does not show cause and effect. Write 3 sentences.", "",
  '''# 1. Correlations of mpg with all other columns, sorted by absolute value
# 2. cor(mtcars$cyl, mtcars$disp)
# 3. Report (3 sentences as comments):
''',
  '''r_mpg <- cor(mtcars)[ , "mpg"][-1]
round(sort(abs(r_mpg), decreasing = TRUE), 3)[1:4]
round(cor(mtcars$cyl, mtcars$disp), 3)
# Several engine measures (wt, cyl, disp, hp) are all strongly related to mpg AND to each other.
# Because they move together, one correlation alone cannot tell us which one causes lower mpg.
# Causal claims need an experiment or careful control of the other variables.''', [("r_cyl_disp", "cor(mtcars$cyl, mtcars$disp)", 3)]),
]

D = [
N(16, 1, "Categorical data in a correlation analysis", "Correlation needs numbers. Convert Smoker (Yes/No) to 0/1 and correlate with Weight (a point-biserial correlation).", LOAD, "",
  '''# === Complete example — read and run ===
births$smoker01 <- as.numeric(births$Smoker == "Yes")
round(cor(births$smoker01, births$Weight), 3)
table(births$Smoker)''', [("r_pb", "cor(as.numeric(births$Smoker == 'Yes'), births$Weight)", 3)]),
N(17, 2, "Ordered categories", "MothersAge is stored as text groups. Turn it into an ordered number (1 = under 15 … 8 = 45-49) and compute the Spearman correlation with Weight.", LOAD,
  '''age_levels <- c("under 15", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49")
births$age_rank <- match(births$___, ___)
table(births$age_rank)
round(cor(births$age_rank, births$Weight, method = "___"), 3)''',
  '''age_levels <- c("under 15", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49")
births$age_rank <- match(births$MothersAge, age_levels)
table(births$age_rank)
round(cor(births$age_rank, births$Weight, method = "spearman"), 3)''', [("rho", "cor(match(births$MothersAge, c('under 15','15-19','20-24','25-29','30-34','35-39','40-44','45-49')), births$Weight, method = 'spearman')", 3)]),
N(18, 3, "A correlation heatmap with ggplot2", "Turn the airquality correlation matrix (pairwise) into long format and draw a heatmap with geom_tile() and the values as labels.", "library(ggplot2)",
  "# Write all your code here\n",
  '''cm <- round(cor(airquality[, 1:4], use = "pairwise.complete.obs"), 2)
long <- as.data.frame(as.table(cm))
names(long) <- c("var1", "var2", "r")
ggplot(long, aes(var1, var2, fill = r)) + geom_tile() + geom_text(aes(label = r)) +
  scale_fill_gradient2(low = "red", mid = "white", high = "blue", limits = c(-1, 1))
nrow(long)''', [("cells", "16", 0)]),
N(19, 4, "Clean, then correlate", "Build a pipeline: from `airquality`, drop rows with NA Ozone or Solar.R, remove Ozone outliers (1.5·IQR), then report r between Ozone and Temp before and after the cleaning.", "library(dplyr)\nlibrary(tidyr)",
  '''# 1. aq_c <- airquality |> drop_na(Ozone, Solar.R)
# 2. IQR fences for Ozone and filter()
# 3. r(Ozone, Temp) before and after removing outliers
# 4. Comment: did the outliers matter?
''',
  '''aq_c <- airquality |> drop_na(Ozone, Solar.R)
lo <- quantile(aq_c$Ozone, 0.25) - 1.5 * IQR(aq_c$Ozone)
hi <- quantile(aq_c$Ozone, 0.75) + 1.5 * IQR(aq_c$Ozone)
aq_o <- aq_c |> filter(Ozone >= lo, Ozone <= hi)
round(c(n_before = nrow(aq_c), n_after = nrow(aq_o),
        r_before = cor(aq_c$Ozone, aq_c$Temp), r_after = cor(aq_o$Ozone, aq_o$Temp)), 3)
# Comment: compare r_before and r_after; a few extreme ozone days affect the strength of r.''', [("r_after", "cor(aq_o$Ozone, aq_o$Temp)", 3)]),
N(20, 5, "Data-quality report", "Write a short data-quality report for the births data: missing values, outliers in Weight and Gestation (1.5·IQR), impossible values (e.g. Gestation outside 20-45 weeks), and the correlation of Weight with Gestation with and without the flagged rows. Finish with 4 sentences of advice.", LOAD,
  '''# 1. Missing values per column
# 2. Outliers in Weight and Gestation
# 3. Impossible or suspicious values
# 4. r(Weight, Gestation) with and without flagged rows
# 5. Advice (4 sentences as comments):
''',
  '''colSums(is.na(births))
fence <- function(x) x < quantile(x, 0.25) - 1.5 * IQR(x) | x > quantile(x, 0.75) + 1.5 * IQR(x)
range(births$Gestation)                       # only full-term births (37-42 weeks)
flag <- fence(births$Weight) | fence(births$Gestation) | births$Gestation < 20 | births$Gestation > 45
c(flagged = sum(flag), share = round(mean(flag), 3))
round(c(r_all = cor(births$Weight, births$Gestation),
        r_unflagged = cor(births$Weight[!flag], births$Gestation[!flag])), 3)
# The births data have no missing values and no impossible gestation values (all are 37-42 weeks).
# Only a few birth weights are flagged as outliers, and they are plausible real babies.
# Removing them barely changes the weight-gestation correlation.
# Keep and report them; note that premature births are not in this data at all.''', [("flagged", "sum(flag)", 0)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M3 QUICK REFERENCE (NA, outliers, correlation)  ║
║  is.na(x)  colSums(is.na(df))  mean(x, na.rm = TRUE) ║
║  drop_na(df)  drop_na(df, col)  replace_na(x, v)     ║
║  IQR rule: Q1 - 1.5*IQR,  Q3 + 1.5*IQR               ║
║  SD rule:  mean +/- 3 * sd                           ║
║  filter(x >= low, x <= high)   group_by() + mutate() ║
║  cor(df, use = 'complete.obs' / 'pairwise...')       ║
║  cor(x, y, method = 'spearman')   cor.test(x, y)     ║
║  ask WHY values are missing or extreme               ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/na_missing.html (650 NAs, outliers & correlation)"
MOD = dict(key="n650_m3", title="650 — Missing Values, Outliers & Correlation: R Coding Practice (20 Questions)",
           file="650_m3_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/Dealing with NAs",
           wd=R650 + "/650 - Data Visualization/Dealing with NAs",
           data_note="Needs readr, dplyr, tidyr and ggplot2 (or `library(tidyverse)`). Uses `NCBirths2004.csv` (same folder as this notebook), `airquality` and `mtcars`.",
           header_link=LINK, site_rmd=SITE,
           topics=[("Missing Values", A), ("Outliers", B), ("Correlation", C), ("Cleaning Pipelines & Reporting", D)], card=CARD)
MOD["questions"] = A + B + C + D
