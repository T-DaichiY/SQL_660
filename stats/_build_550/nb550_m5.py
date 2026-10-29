"""550 M5: t procedures, conditions & bootstrap, one-way ANOVA & post-hoc, chi-square tests (built-in data + made-up tables)."""
from nb_build import N
from practice_gen import SRC

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"

A = [
N(1, 1, "One-sample t interval and test", "Is the mean sleep gain in the built-in `sleep` data (group 1) different from 0?", "", "",
  '''# === Complete example — read and run ===
g1 <- sleep$extra[sleep$group == 1]
res <- t.test(g1, mu = 0)                 # H0: mu = 0, Ha: mu != 0
res
round(c(t = unname(res$statistic), df = unname(res$parameter), p = res$p.value), 4)
round(res$conf.int, 3)''', [("t", "res$statistic", 4)]),
N(2, 2, "Two-sample Welch t test", "Compare mpg of automatic (am = 0) and manual (am = 1) cars in `mtcars`.", "",
  '''res <- t.test(mpg ~ ___, data = ___)          # Welch by default
round(c(t = unname(res$statistic), df = unname(res$___), p = res$p.value), 4)
round(res$conf.int, 3)                          # CI for mu(auto) - mu(manual)''',
  '''res <- t.test(mpg ~ am, data = mtcars)          # Welch by default
round(c(t = unname(res$statistic), df = unname(res$parameter), p = res$p.value), 4)
round(res$conf.int, 3)                          # CI for mu(auto) - mu(manual)''', [("df", "res$parameter", 2), ("p", "res$p.value", 4)]),
N(3, 3, "Paired t test", "The `sleep` data give two drugs to the SAME 10 patients (ID). Run a paired t test of drug 2 vs drug 1 and compare its p-value with an unpaired test.", "",
  "# Write all your code here\n# Hint: reshape with sleep$extra[sleep$group == 1] and [== 2]\n",
  '''d1 <- sleep$extra[sleep$group == 1]
d2 <- sleep$extra[sleep$group == 2]
paired <- t.test(d2, d1, paired = TRUE)
unpaired <- t.test(d2, d1)
round(c(p_paired = paired$p.value, p_unpaired = unpaired$p.value), 4)''', [("p_paired", "paired$p.value", 4)]),
N(4, 4, "Checking conditions", "Before a t test on `ToothGrowth` (len for supp = VC vs OJ), check the conditions: sample sizes, histograms/boxplots, and shapiro.test() per group. Then run the test.", "",
  '''# 1. n per group
# 2. boxplot(len ~ supp, data = ToothGrowth)
# 3. shapiro.test() for each group
# 4. Welch t test
# 5. Conclusion (comment): are the conditions reasonable? what does the test say?
''',
  '''table(ToothGrowth$supp)
boxplot(len ~ supp, data = ToothGrowth, col = "lightblue")
sw <- tapply(ToothGrowth$len, ToothGrowth$supp, function(x) shapiro.test(x)$p.value)
round(sw, 4)
res <- t.test(len ~ supp, data = ToothGrowth)
round(c(t = unname(res$statistic), p = res$p.value), 4)
# Conditions: 30 per group and no strong skew, so the t procedure is reasonable.
# The p-value is just above 0.05: weak evidence that OJ gives longer teeth.''', [("p", "res$p.value", 4)]),
N(5, 5, "Bootstrap t interval", "Bootstrap the mean of `ToothGrowth$len[ToothGrowth$supp == 'VC']` (`set.seed(5)`, 5,000 resamples). Compare the percentile 95% interval with the t interval. Write 3 sentences.", "",
  '''# 1. x <- the VC lengths
# 2. boot_means <- replicate(5000, mean(sample(x, replace = TRUE)))
# 3. Percentile interval: quantile(boot_means, c(0.025, 0.975))
# 4. t interval: t.test(x)$conf.int
# 5. Report (3 sentences as comments):
''',
  '''x <- ToothGrowth$len[ToothGrowth$supp == "VC"]
set.seed(5)
boot_means <- replicate(5000, mean(sample(x, replace = TRUE)))
boot_ci <- quantile(boot_means, c(0.025, 0.975))
t_ci <- t.test(x)$conf.int
round(rbind(bootstrap = boot_ci, t = t_ci), 3)
hist(boot_means, breaks = 40, col = "lightblue")
# The bootstrap resamples the data with replacement to imitate repeated sampling.
# Its percentile interval is very close to the t interval here.
# The bootstrap is useful when we doubt the normality condition.''', [("boot_lower", "boot_ci[1]", 2)]),
]

B = [
N(6, 1, "One-way ANOVA", "Do chick weights differ by feed type (`chickwts`)?", "", "",
  '''# === Complete example — read and run ===
boxplot(weight ~ feed, data = chickwts, las = 2, col = "lightblue")
fit <- aov(weight ~ feed, data = chickwts)
summary(fit)
tab <- summary(fit)[[1]]
round(c(F = tab$`F value`[1], p = tab$`Pr(>F)`[1]), 6)''', [("F", "summary(fit)[[1]]$`F value`[1]", 3)]),
N(7, 2, "ANOVA pieces by hand", "Compute SSB, SSW, MSB, MSW and F for `weight ~ feed` and check against Q6.", "",
  '''y <- chickwts$weight; g <- chickwts$feed
grand <- mean(y)
group_means <- tapply(y, g, mean); n_g <- tapply(y, g, length)
SSB <- sum(n_g * (group_means - ___)^2)
SSW <- sum((y - group_means[___])^2)
k <- length(n_g); N <- length(y)
MSB <- SSB / (k - ___); MSW <- SSW / (N - ___)
F_stat <- MSB / MSW
round(c(SSB = SSB, SSW = SSW, F = F_stat), 2)''',
  '''y <- chickwts$weight; g <- chickwts$feed
grand <- mean(y)
group_means <- tapply(y, g, mean); n_g <- tapply(y, g, length)
SSB <- sum(n_g * (group_means - grand)^2)
SSW <- sum((y - group_means[g])^2)
k <- length(n_g); N <- length(y)
MSB <- SSB / (k - 1); MSW <- SSW / (N - k)
F_stat <- MSB / MSW
round(c(SSB = SSB, SSW = SSW, F = F_stat), 2)''', [("SSB", "SSB", 1), ("F", "F_stat", 3)]),
N(8, 3, "p-value from the F distribution", "Use `pf()` to get the ANOVA p-value from F, df1 and df2 in Q7, and draw the F curve with the observed F marked.", "",
  "# Write all your code here\n",
  '''p_val <- pf(F_stat, df1 = k - 1, df2 = N - k, lower.tail = FALSE)
signif(p_val, 3)
curve(df(x, k - 1, N - k), from = 0, to = 20, ylab = "Density", xlab = "F")
abline(v = F_stat, col = "red")''', [("p", "p_val", 10)]),
N(9, 4, "Insect sprays", "An agronomist compares six sprays (`InsectSprays`, count of insects). Run the ANOVA, report F and p, and say which spray has the lowest mean count.", "",
  '''# 1. Boxplot of count by spray
# 2. Group means
# 3. ANOVA: F, df and p-value
# 4. Conclusion (comment):
''',
  '''boxplot(count ~ spray, data = InsectSprays, col = "lightblue")
means <- round(tapply(InsectSprays$count, InsectSprays$spray, mean), 2)
means
names(which.min(means))
fit2 <- aov(count ~ spray, data = InsectSprays)
summary(fit2)
# Conclusion: the sprays differ strongly (very small p); spray C has the lowest mean count.''', [("F", "summary(fit2)[[1]]$`F value`[1]", 2)]),
N(10, 5, "Post-hoc tests", "After the chickwts ANOVA, run TukeyHSD() and a Bonferroni pairwise t test. How many of the 15 pairs are significant at 0.05 with each method? Write 3 sentences on why we need post-hoc tests.", "",
  '''# 1. TukeyHSD(fit)
# 2. Count pairs with p adj < 0.05
# 3. pairwise.t.test(..., p.adjust.method = "bonferroni")
# 4. Count pairs with p < 0.05
# 5. Report (3 sentences as comments):
''',
  '''tk <- TukeyHSD(fit)$feed
n_tukey <- sum(tk[, "p adj"] < 0.05)
pw <- pairwise.t.test(chickwts$weight, chickwts$feed, p.adjust.method = "bonferroni")
n_bonf <- sum(pw$p.value < 0.05, na.rm = TRUE)
c(n_tukey = n_tukey, n_bonf = n_bonf)
# ANOVA only says that at least one mean differs, not which ones.
# Testing 15 pairs at 0.05 each would inflate the chance of a false positive.
# Tukey and Bonferroni adjust for many comparisons; Bonferroni is the more conservative.''', [("n_tukey", "n_tukey", 0), ("n_bonf", "n_bonf", 0)]),
]

C = [
N(11, 1, "Chi-square goodness of fit", "A store expects equal sales on weekdays Mon–Fri. Observed sales (made-up) are below.", "obs <- c(Mon = 54, Tue = 41, Wed = 39, Thu = 47, Fri = 69)", "",
  '''# === Complete example — read and run ===
expected <- rep(sum(obs) / 5, 5)
chi_sq <- sum((obs - expected)^2 / expected)
p_val <- pchisq(chi_sq, df = 5 - 1, lower.tail = FALSE)
round(c(chi_sq = chi_sq, p = p_val), 4)
chisq.test(obs)                        # same result''', [("chi_sq", "chi_sq", 3)]),
N(12, 2, "GOF with unequal proportions", "A website claims 50% of visitors use phones, 35% computers and 15% tablets. A sample of 400 visitors (made-up) is below.", "visits <- c(phone = 182, computer = 160, tablet = 58)",
  '''res <- chisq.test(visits, p = c(___, ___, ___))
round(res$statistic, 3); round(res$p.value, 4)
res$___                                 # expected counts''',
  '''res <- chisq.test(visits, p = c(0.50, 0.35, 0.15))
round(res$statistic, 3); round(res$p.value, 4)
res$expected                            # expected counts''', [("chi_sq", "res$statistic", 3), ("p", "res$p.value", 4)]),
N(13, 3, "Test of independence", "Is hair colour independent of eye colour? Use `HairEyeColor` summed over Sex (`margin.table(HairEyeColor, c(1, 2))`). Report χ², df, p and the largest standardized residual.", "",
  "# Write all your code here\n",
  '''he <- margin.table(HairEyeColor, c(1, 2))
res <- chisq.test(he)
round(c(chi_sq = unname(res$statistic), df = unname(res$parameter)), 2)
signif(res$p.value, 3)
which(abs(res$stdres) == max(abs(res$stdres)), arr.ind = TRUE)
round(max(abs(res$stdres)), 2)''', [("chi_sq", "res$statistic", 2), ("df", "res$parameter", 0)]),
N(14, 4, "Payment method and age group", "A café records the payment method of 300 customers by age group (made-up table). Test whether payment method depends on age group and describe the pattern with row proportions.",
  '''pay <- matrix(c(40, 25, 10,
                30, 45, 20,
                15, 50, 65), nrow = 3, byrow = TRUE,
              dimnames = list(age = c("18-29", "30-49", "50+"), method = c("Card", "Phone", "Cash")))''',
  '''# 1. addmargins(pay)
# 2. Row proportions (3 decimals)
# 3. chisq.test(pay): statistic, df, p
# 4. Check: all expected counts >= 5?
# 5. Conclusion (comment):
''',
  '''addmargins(pay)
round(proportions(pay, margin = 1), 3)
res <- chisq.test(pay)
res
all(res$expected >= 5)
# Conclusion: payment method depends on age group; cash use rises sharply with age.''', [("chi_sq", "res$statistic", 2)]),
N(15, 5, "Chi-square from raw data", "Using `mtcars`, make a table of gear by am and test independence. The expected counts are small: compare chisq.test() with simulate.p.value = TRUE (`set.seed(15)`, B = 10000) and fisher.test(). Write 3 sentences.", "",
  '''# 1. tab <- table(mtcars$gear, mtcars$am)
# 2. chisq.test(tab) and its expected counts (warning?)
# 3. chisq.test(tab, simulate.p.value = TRUE, B = 10000)
# 4. fisher.test(tab)
# 5. Report (3 sentences as comments):
''',
  '''tab <- table(gear = mtcars$gear, am = mtcars$am)
tab
r1 <- suppressWarnings(chisq.test(tab))
round(r1$expected, 2)
set.seed(15)
r2 <- chisq.test(tab, simulate.p.value = TRUE, B = 10000)
r3 <- fisher.test(tab)
signif(c(chisq = r1$p.value, simulated = r2$p.value, fisher = r3$p.value), 3)
# Several expected counts are below 5, so the chi-square approximation is doubtful.
# The simulated and Fisher p-values do not rely on that approximation.
# All three agree that gear and transmission type are strongly associated.''', [("p_fisher", "r3$p.value", 8)]),
]

D = [
N(16, 1, "Effect size for ANOVA", "Compute eta squared (SSB / SST) for the chickwts ANOVA.", "", "",
  '''# === Complete example — read and run ===
tab <- summary(aov(weight ~ feed, data = chickwts))[[1]]
ss <- tab$`Sum Sq`
eta_sq <- ss[1] / sum(ss)
round(eta_sq, 3)            # share of variation in weight explained by feed''', [("eta_sq", "eta_sq", 3)]),
N(17, 2, "Choosing the test", "For each research question, choose the test and run it on the data given.", "",
  '''# a) Is mean Ozone different between May and August (airquality)?   -> ___ test
t.test(Ozone ~ Month, data = subset(airquality, Month %in% c(___, ___)))$p.value
# b) Does the number of cylinders differ by transmission (mtcars)?   -> ___ test
suppressWarnings(chisq.test(table(mtcars$___, mtcars$___))$p.value)
# c) Does mean breaks differ across tension levels (warpbreaks)?       -> ___
summary(aov(breaks ~ ___, data = warpbreaks))''',
  '''# a) two-sample t test
t.test(Ozone ~ Month, data = subset(airquality, Month %in% c(5, 8)))$p.value
# b) chi-square test of independence
suppressWarnings(chisq.test(table(mtcars$cyl, mtcars$am))$p.value)
# c) one-way ANOVA
summary(aov(breaks ~ tension, data = warpbreaks))''', [("p_a", "t.test(Ozone ~ Month, data = subset(airquality, Month %in% c(5, 8)))$p.value", 6)]),
N(18, 3, "Statistical vs practical significance", "With `set.seed(18)`, simulate two groups of 20,000 with means 100 and 100.5 (SD 15). Run a t test and compute Cohen's d. Is the result important?", "",
  "# Write all your code here\n",
  '''set.seed(18)
a <- rnorm(20000, 100, 15); b <- rnorm(20000, 100.5, 15)
p <- t.test(a, b)$p.value
d <- (mean(b) - mean(a)) / sqrt((var(a) + var(b)) / 2)
signif(p, 3); round(d, 3)
# A tiny effect can be statistically significant with huge samples; check the effect size.''', [("d", "d", 3)]),
N(19, 4, "Warp breaks by tension", "A textile mill compares breaks for low, medium and high tension (`warpbreaks`). Run the ANOVA and Tukey test, and report which pairs differ.", "",
  '''# 1. Group means of breaks by tension
# 2. aov() and summary()
# 3. TukeyHSD(): which pairs have p adj < 0.05?
# 4. Recommendation (comment):
''',
  '''round(tapply(warpbreaks$breaks, warpbreaks$tension, mean), 2)
fit_w <- aov(breaks ~ tension, data = warpbreaks)
summary(fit_w)
tk <- TukeyHSD(fit_w)$tension
round(tk, 4)
rownames(tk)[tk[, "p adj"] < 0.05]
# Recommendation: low tension gives the most breaks; medium or high tension is better.''', [("F", "summary(fit_w)[[1]]$`F value`[1]", 3)]),
N(20, 5, "Mini report: supplement and dose", "ToothGrowth has two supplements and three doses. (1) Test dose with a one-way ANOVA. (2) Test supp × dose-group independence of 'long teeth' (len > 20). (3) Write a 4-sentence report for a nutrition team.", "",
  '''# 1. ToothGrowth$dose_f <- factor(ToothGrowth$dose); ANOVA of len ~ dose_f
# 2. long <- ToothGrowth$len > 20; table(ToothGrowth$supp, long); chisq.test()
# 3. Report (4 sentences as comments):
# Question:
# Results:
# Conclusion:
# Recommendation:
''',
  '''ToothGrowth$dose_f <- factor(ToothGrowth$dose)
fit_d <- aov(len ~ dose_f, data = ToothGrowth)
summary(fit_d)
long <- ToothGrowth$len > 20
tab <- table(supp = ToothGrowth$supp, long = long)
tab
res <- chisq.test(tab)
round(c(chi_sq = unname(res$statistic), p = res$p.value), 4)
# Question: does tooth length depend on dose, and does supplement type relate to long teeth?
# Results: the dose ANOVA is highly significant; the supp x long-teeth test is reported above.
# Conclusion: higher doses give longer teeth.
# Recommendation: choose the dose first; use the supplement result as secondary evidence.''', [("F_dose", "summary(fit_d)[[1]]$`F value`[1]", 2)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M5 QUICK REFERENCE                                  ║
║  t.test(x, mu = 0)    t.test(y ~ group, data = df)   ║
║  t.test(x2, x1, paired = TRUE)   shapiro.test(x)     ║
║  bootstrap: replicate(B, mean(sample(x, TRUE)))      ║
║  aov(y ~ group, data = df)   summary(fit)            ║
║  F = MSB / MSW   pf(F, k - 1, N - k, lower = FALSE)  ║
║  TukeyHSD(fit)   pairwise.t.test(y, g, 'bonferroni') ║
║  chisq.test(obs, p = probs)       goodness of fit    ║
║  chisq.test(table)  $expected  $stdres  fisher.test  ║
║  eta^2 = SSB / SST    Cohen's d = diff / SD          ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/stats/m5_t_intro.html (M5 t / ANOVA / chi-square)"
MOD = dict(key="n550_m5", title="550 M5 — t Procedures, ANOVA & Chi-square Tests: R Coding Practice (20 Questions)",
           file="m5_practice_v1.Rmd", folder=SRC + "/Module 5", wd=SRC + "/Module 5",
           data_note="No data files are needed: built-in data sets (sleep, mtcars, ToothGrowth, chickwts, InsectSprays, HairEyeColor, warpbreaks, airquality) and small made-up tables.",
           header_link=LINK, site_rmd=[STATS + "/rmd"],
           topics=[("t Procedures, Conditions & Bootstrap", A), ("One-way ANOVA & Post-hoc Tests", B),
                   ("Chi-square Tests", C), ("Choosing Tests & Reporting", D)], card=CARD)
MOD["questions"] = A + B + C + D
