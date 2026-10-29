"""550 M4: sampling & bias, test statistics & p-values, errors & power, SE & confidence intervals (base R, simulated data)."""
from nb_build import N
from practice_gen import SRC

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"
POP = '''set.seed(2026)
pop <- round(rnorm(10000, mean = 0.9, sd = 0.3), 2)   # mercury (ppm) of 10,000 fish'''

A = [
N(1, 1, "Population vs. simple random sample", "Compare a simple random sample of 60 fish with the true population mean.", POP, "",
  '''# === Complete example — read and run ===
mu <- mean(pop)                         # population parameter (normally unknown)
set.seed(1)
srs <- sample(pop, size = 60)           # simple random sample, without replacement
xbar <- mean(srs)                       # sample statistic
round(c(mu = mu, xbar = xbar, error = xbar - mu), 4)''', [("xbar", "xbar", 4)]),
N(2, 2, "A biased convenience sample", "A boat only catches the largest fish (top 20% of mercury values). Show the bias.", POP,
  '''cut_off <- quantile(pop, ___)               # 80th percentile
big_fish <- pop[pop > ___]
set.seed(1)
conv <- sample(big_fish, size = ___)
round(mean(conv) - mean(___), 4)            # bias''',
  '''cut_off <- quantile(pop, 0.80)              # 80th percentile
big_fish <- pop[pop > cut_off]
set.seed(1)
conv <- sample(big_fish, size = 60)
round(mean(conv) - mean(pop), 4)            # bias''', [("bias", "mean(conv) - mean(pop)", 4)]),
N(3, 3, "Many samples: how much do sample means vary?", "Draw 1,000 random samples of size 60 from `pop` (`set.seed(3)`), store the sample means, and report their mean and SD. Compare the SD with sd(pop)/sqrt(60).", POP,
  "# Write all your code here\n",
  '''set.seed(3)
means <- replicate(1000, mean(sample(pop, 60)))
round(c(mean_of_means = mean(means), sd_of_means = sd(means), theory = sd(pop) / sqrt(60)), 4)
hist(means, col = "lightblue", main = "1,000 sample means (n = 60)")''', [("sd_of_means", "sd(means)", 4)]),
N(4, 4, "Observational study or experiment?", "A café tests a new menu: 40 branches are randomly split into 20 with the new menu and 20 without (made-up data below). Decide the study type, the explanatory and response variables, and compare the mean sales.",
  '''set.seed(44)
branch <- data.frame(menu  = rep(c("new", "old"), each = 20),
                     sales = round(c(rnorm(20, 5200, 400), rnorm(20, 4900, 400))))''',
  '''# 1. Study type (comment): observational or experiment? Why?
# 2. Explanatory and response variables (comment)
# 3. Mean sales for each menu with tapply()
# 4. Difference new - old
# 5. Conclusion (comment): can we talk about cause and effect here?
''',
  '''# Experiment: the menu was randomly assigned to branches.
# Explanatory: menu (new / old). Response: sales.
means <- tapply(branch$sales, branch$menu, mean)
means
diff_new_old <- means[["new"]] - means[["old"]]
diff_new_old
# Because the menu was randomly assigned, a real difference could be read as an effect of the menu
# (we still need a test to rule out chance - Topic B).''', [("diff_new_old", "diff_new_old", 1)]),
N(5, 5, "Survey non-response", "A university emails 2,000 students; only 30% reply, and students who reply study more hours. Simulate this and show how non-response biases the estimate of mean study hours. Write a 3-sentence report.",
  '''set.seed(55)
hours <- round(rgamma(2000, shape = 4, rate = 0.25), 1)      # weekly study hours of all students
p_reply <- pmin(0.9, 0.05 + hours / 40)                     # keener students reply more often
replied <- runif(2000) < p_reply''',
  '''# 1. True mean hours of all 2,000 students
# 2. Response rate
# 3. Mean hours of the students who replied
# 4. Size of the bias
# 5. Report (3 sentences as comments):
''',
  '''true_mean <- mean(hours)
resp_rate <- mean(replied)
reply_mean <- mean(hours[replied])
bias <- reply_mean - true_mean
round(c(true_mean = true_mean, resp_rate = resp_rate, reply_mean = reply_mean, bias = bias), 3)
# Only part of the students replied, and repliers study more than the rest.
# Their mean is therefore higher than the true mean: the estimate is biased upward.
# A random sample does not protect us when non-response depends on the variable we measure.''', [("bias", "bias", 3)]),
]

B = [
N(6, 1, "z test statistic and p-value", "A machine should fill 500 g bags (σ = 6 g). A sample of 36 bags has mean 502.5 g. Test H0: μ = 500 vs Ha: μ ≠ 500.", "", "",
  '''# === Complete example — read and run ===
xbar <- 502.5; mu0 <- 500; sigma <- 6; n <- 36
se <- sigma / sqrt(n)
z <- (xbar - mu0) / se                     # test statistic = standardized score
p_two <- 2 * pnorm(abs(z), lower.tail = FALSE)
round(c(se = se, z = z, p = p_two), 4)
if (p_two < 0.05) cat("Reject H0\\n") else cat("Fail to reject H0\\n")''', [("z", "z", 4), ("p", "p_two", 4)]),
N(7, 2, "One-tailed test", "Same machine. The manager only worries about over-filling: Ha: μ > 500.", "",
  '''xbar <- 502.5; mu0 <- 500; sigma <- 6; n <- 36
z <- (xbar - ___) / (sigma / sqrt(___))
p_right <- pnorm(z, lower.tail = ___)
round(c(z, p_right), 4)
# Compare with the two-tailed p-value from Q6 (comment):''',
  '''xbar <- 502.5; mu0 <- 500; sigma <- 6; n <- 36
z <- (xbar - mu0) / (sigma / sqrt(n))
p_right <- pnorm(z, lower.tail = FALSE)
round(c(z, p_right), 4)
# The one-tailed p-value is half of the two-tailed one.''', [("p_right", "p_right", 4)]),
N(8, 3, "Critical values", "Find the critical z values for α = 0.05 and α = 0.01, for two-tailed and right-tailed tests (4 values, 3 decimals). Is z = 2.5 significant in each case?", "",
  "# Write all your code here\n",
  '''crit <- c(two_05 = qnorm(0.975), two_01 = qnorm(0.995),
          right_05 = qnorm(0.95), right_01 = qnorm(0.99))
round(crit, 3)
2.5 > crit''', [("two_01", "qnorm(0.995)", 3)]),
N(9, 4, "Battery life claim", "A company claims mean battery life is 20 hours (σ = 2.4). A reviewer tests 25 batteries and finds a mean of 19.1 hours. Test whether the true mean is less than claimed at α = 0.05.", "",
  '''# 1. H0 and Ha (comment)
# 2. SE, z and the p-value
# 3. Decision at alpha = 0.05
# 4. Conclusion in context (comment):
''',
  '''# H0: mu = 20   Ha: mu < 20
se <- 2.4 / sqrt(25)
z <- (19.1 - 20) / se
p <- pnorm(z)
round(c(se = se, z = z, p = p), 4)
if (p < 0.05) cat("Reject H0\\n") else cat("Fail to reject H0\\n")
# Conclusion: there is evidence that the mean battery life is below 20 hours.''', [("z", "z", 4), ("p", "p", 4)]),
N(10, 5, "Simulating the null distribution", "Simulate 10,000 sample means under H0 (μ = 500, σ = 6, n = 36, `set.seed(10)`). Estimate the two-tailed p-value for x̄ = 502.5 from the simulation and compare it with Q6. Write 3 sentences on what a p-value means.", "",
  '''# 1. null_means <- replicate(10000, mean(rnorm(36, 500, 6)))
# 2. Share of null means at least as far from 500 as 502.5
# 3. Compare with the formula p-value
# 4. Histogram with a red line at 502.5
# 5. Report (3 sentences as comments):
''',
  '''set.seed(10)
null_means <- replicate(10000, mean(rnorm(36, 500, 6)))
p_sim <- mean(abs(null_means - 500) >= 2.5)
p_formula <- 2 * pnorm(2.5, lower.tail = FALSE)
round(c(p_sim = p_sim, p_formula = p_formula), 4)
hist(null_means, breaks = 50, col = "lightblue"); abline(v = c(497.5, 502.5), col = "red")
# The p-value is the chance of a result at least this extreme IF H0 were true.
# Both the simulation and the formula give about 1%.
# It is not the probability that H0 is true.''', [("p_sim", "p_sim", 4)]),
]

C = [
N(11, 1, "Type I error rate by simulation", "If H0 is true and we test at α = 0.05, how often do we wrongly reject?", "", "",
  '''# === Complete example — read and run ===
set.seed(11)
p_values <- replicate(5000, {
  x <- rnorm(30, mean = 50, sd = 10)          # H0 (mu = 50) is TRUE
  t.test(x, mu = 50)$p.value
})
type1_rate <- mean(p_values < 0.05)
type1_rate                                    # close to alpha = 0.05''', [("type1_rate", "type1_rate", 3)]),
N(12, 2, "Power with power.t.test()", "Find the power of a two-sided one-sample t test with n = 30, true difference δ = 4, SD = 10, α = 0.05.", "",
  '''res <- power.t.test(n = ___, delta = ___, sd = ___, sig.level = ___,
                    type = "one.sample", alternative = "two.sided")
round(res$power, 3)
1 - res$___                    # probability of a Type II error (beta)''',
  '''res <- power.t.test(n = 30, delta = 4, sd = 10, sig.level = 0.05,
                    type = "one.sample", alternative = "two.sided")
round(res$power, 3)
1 - res$power                  # probability of a Type II error (beta)''', [("power", "res$power", 3)]),
N(13, 3, "Sample size for 80% power", "How many observations are needed to reach 80% and 90% power for δ = 4, SD = 10, α = 0.05 (one-sample, two-sided)? Round up.", "",
  "# Write all your code here\n",
  '''n80 <- ceiling(power.t.test(delta = 4, sd = 10, power = 0.80, type = "one.sample")$n)
n90 <- ceiling(power.t.test(delta = 4, sd = 10, power = 0.90, type = "one.sample")$n)
c(n80 = n80, n90 = n90)''', [("n80", "n80", 0), ("n90", "n90", 0)]),
N(14, 4, "Effect size (Cohen's d)", "A tutoring program raises the mean score from 70 to 74.5 (SD 12). Compute Cohen's d, classify it (0.2 small / 0.5 medium / 0.8 large) and find the power for n = 50 at α = 0.05.", "",
  '''# 1. Cohen's d = difference / SD
# 2. Size category (comment)
# 3. Power for n = 50 (one-sample, two-sided)
# 4. Conclusion (comment):
''',
  '''d <- (74.5 - 70) / 12
round(d, 3)
pw <- power.t.test(n = 50, delta = 4.5, sd = 12, type = "one.sample")$power
round(pw, 3)
# d is about 0.38: between small and medium.
# With n = 50 the power is below 80%, so a real effect could easily be missed.''', [("d", "d", 3), ("power", "pw", 3)]),
N(15, 5, "Errors and α", "Simulate 5,000 studies where the true mean is 53 (H0: μ = 50, SD 10, n = 30, `set.seed(15)`). Estimate the power and the Type II error rate at α = 0.05 and α = 0.01. Write 3 sentences on the trade-off.", "",
  '''# 1. p-values from 5,000 simulated t tests (true mean 53)
# 2. Power at alpha 0.05 and 0.01
# 3. Type II error rates (1 - power)
# 4. Report (3 sentences as comments):
''',
  '''set.seed(15)
p_alt <- replicate(5000, t.test(rnorm(30, 53, 10), mu = 50)$p.value)
power05 <- mean(p_alt < 0.05); power01 <- mean(p_alt < 0.01)
round(c(power05 = power05, beta05 = 1 - power05, power01 = power01, beta01 = 1 - power01), 3)
# Lowering alpha from 0.05 to 0.01 reduces Type I errors...
# ...but it also lowers the power, so Type II errors become more common.
# A larger sample is the way to keep both error rates small.''', [("power05", "power05", 3), ("power01", "power01", 3)]),
]

D = [
N(16, 1, "Standard error and the CLT", "Sample means of a right-skewed variable become approximately normal as n grows.", "", "",
  '''# === Complete example — read and run ===
set.seed(16)
skewed <- rexp(100000, rate = 1 / 20)          # right-skewed population, mean 20, sd 20
par(mfrow = c(1, 2))
hist(skewed, breaks = 60, main = "Population", col = "gray")
means40 <- replicate(2000, mean(sample(skewed, 40)))
hist(means40, breaks = 40, main = "Means of n = 40", col = "lightblue")
par(mfrow = c(1, 1))
se_theory <- sd(skewed) / sqrt(40)
round(c(sd_of_means = sd(means40), se_theory = se_theory), 3)''', [("se_theory", "se_theory", 3)]),
N(17, 2, "A 95% confidence interval by hand", "Build a 95% CI for the mean of `mtcars$mpg` using t* and check it with t.test().", "",
  '''x <- mtcars$mpg
n <- length(x); xbar <- mean(x); se <- sd(x) / sqrt(___)
tstar <- qt(___, df = n - 1)
ci <- xbar + c(-1, 1) * ___ * se
round(ci, 3)
round(t.test(x)$___, 3)''',
  '''x <- mtcars$mpg
n <- length(x); xbar <- mean(x); se <- sd(x) / sqrt(n)
tstar <- qt(0.975, df = n - 1)
ci <- xbar + c(-1, 1) * tstar * se
round(ci, 3)
round(t.test(x)$conf.int, 3)''', [("lower", "ci[1]", 3), ("upper", "ci[2]", 3)]),
N(18, 3, "CI width vs. n and confidence level", "For SD = 15, compute the margin of error of a mean CI for n = 25, 100, 400 at 95%, and for n = 100 at 90% and 99% (use z*). What happens when n is multiplied by 4?", "",
  "# Write all your code here\n",
  '''me <- function(n, conf = 0.95, s = 15) qnorm(1 - (1 - conf) / 2) * s / sqrt(n)
round(c(n25 = me(25), n100 = me(100), n400 = me(400)), 3)
round(c(c90 = me(100, 0.90), c95 = me(100), c99 = me(100, 0.99)), 3)
# Multiplying n by 4 halves the margin of error.''', [("me100", "me(100)", 3)]),
N(19, 4, "Coffee shop wait times", "A coffee shop records 40 wait times (minutes, below). Build a 95% CI for the mean wait, report the margin of error and decide whether the target of 5 minutes is plausible.",
  '''set.seed(19)
wait <- round(rgamma(40, shape = 6, rate = 1.1), 1)''',
  '''# 1. Mean, SD, n, SE
# 2. 95% CI with t.test()
# 3. Margin of error
# 4. Is 5 inside the CI? (logical)
# 5. Conclusion (comment):
''',
  '''round(c(mean = mean(wait), sd = sd(wait), n = length(wait), se = sd(wait) / sqrt(length(wait))), 3)
ci <- t.test(wait)$conf.int
round(ci, 3)
moe <- diff(ci) / 2
round(moe, 3)
5 >= ci[1] & 5 <= ci[2]
# Conclusion: use the logical result above - if TRUE, a 5-minute mean wait is plausible.''', [("moe", "moe", 3)]),
N(20, 5, "Coverage of 95% intervals", "Simulate 2,000 samples of size 25 from N(100, 15) (`set.seed(20)`), build a 95% t interval for each, and count how many contain 100. Plot the first 50 intervals. Write 3 sentences on what '95% confidence' means.", "",
  '''# 1. A function that returns TRUE if the CI of one sample contains 100
# 2. Coverage over 2,000 samples
# 3. Plot the first 50 intervals (segments) with a line at 100
# 4. Report (3 sentences as comments):
''',
  '''set.seed(20)
cis <- t(replicate(2000, t.test(rnorm(25, 100, 15))$conf.int))
covered <- cis[, 1] <= 100 & cis[, 2] >= 100
coverage <- mean(covered)
coverage
plot(NULL, xlim = range(cis[1:50, ]), ylim = c(1, 50), xlab = "CI", ylab = "Sample")
segments(cis[1:50, 1], 1:50, cis[1:50, 2], 1:50, col = ifelse(covered[1:50], "gray40", "red"))
abline(v = 100, col = "blue")
# About 95% of the intervals contain the true mean of 100.
# "95% confident" describes the method: in the long run 95% of such intervals capture mu.
# Any single interval either contains mu or not; we just do not know which.''', [("coverage", "coverage", 3)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M4 QUICK REFERENCE                                  ║
║  sample(x, n)  replicate(B, expr)  set.seed()        ║
║  SE = sd / sqrt(n)        z = (xbar - mu0) / SE      ║
║  p two-sided: 2 * pnorm(abs(z), lower.tail = FALSE)  ║
║  critical: qnorm(0.975)  qt(0.975, df = n - 1)       ║
║  t.test(x, mu = 50, alternative = 'less')            ║
║  CI: xbar + c(-1, 1) * tstar * SE                    ║
║  power.t.test(n, delta, sd, sig.level, type)         ║
║  Type I = alpha   Type II = beta = 1 - power         ║
║  Cohen's d = difference / SD                         ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/stats/m3_basics.html (M4 ①–③)"
MOD = dict(key="n550_m4", title="550 M4 — Sampling, Hypothesis Testing & Confidence Intervals: R Coding Practice (20 Questions)",
           file="m4_practice_v1.Rmd", folder=SRC + "/Module 4", wd=SRC + "/Module 3",
           data_note="No data files are needed: every data set is simulated or built into R.",
           header_link=LINK, site_rmd=[STATS + "/rmd"],
           topics=[("Samples, Populations & Bias", A), ("Test Statistics & p-values", B),
                   ("Errors, Power & Effect Size", C), ("Standard Error & Confidence Intervals", D)], card=CARD)
MOD["questions"] = A + B + C + D
