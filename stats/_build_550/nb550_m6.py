"""550 M6: correlation, least-squares regression, residuals & R², inference for the slope, categorical & multiple regression."""
from nb_build import N
from practice_gen import SRC

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"

A = [
N(1, 1, "Scatterplot and correlation", "How strongly is car weight related to fuel economy (`mtcars`)?", "", "",
  '''# === Complete example — read and run ===
plot(mpg ~ wt, data = mtcars, pch = 16, xlab = "Weight (1000 lb)", ylab = "mpg")
r <- cor(mtcars$wt, mtcars$mpg)
round(r, 4)            # strong negative linear association''', [("r", "r", 4)]),
N(2, 2, "Correlation by hand", "Compute r from z-scores: r = Σ(zx · zy) / (n − 1).", "",
  '''x <- mtcars$wt; y <- mtcars$mpg; n <- length(x)
zx <- (x - mean(x)) / ___(x)
zy <- (y - ___(y)) / sd(y)
r_hand <- sum(___ * ___) / (n - 1)
round(c(r_hand, cor(x, y)), 4)''',
  '''x <- mtcars$wt; y <- mtcars$mpg; n <- length(x)
zx <- (x - mean(x)) / sd(x)
zy <- (y - mean(y)) / sd(y)
r_hand <- sum(zx * zy) / (n - 1)
round(c(r_hand, cor(x, y)), 4)''', [("r_hand", "r_hand", 4)]),
N(3, 3, "Correlation matrix", "Make a correlation matrix of mpg, wt, hp and qsec (`mtcars`), rounded to 2 decimals, and a scatterplot matrix with pairs(). Which variable is most strongly correlated with mpg?", "",
  "# Write all your code here\n",
  '''vars <- mtcars[, c("mpg", "wt", "hp", "qsec")]
cm <- round(cor(vars), 2)
cm
pairs(vars, pch = 16)
names(which.max(abs(cm["mpg", -1])))''', [("r_mpg_hp", "cor(mtcars$mpg, mtcars$hp)", 2)]),
N(4, 4, "Properties of r", "Show with `airquality` (Temp vs Ozone, complete cases) that r does not change when Temp is converted from °F to °C, nor when x and y are swapped. Then test the correlation with cor.test().", "",
  '''# 1. aq <- na.omit(airquality[, c("Ozone", "Temp")])
# 2. r with Temp in F, then in C ((F - 32) * 5 / 9)
# 3. r with x and y swapped
# 4. cor.test(): r, p-value, 95% CI
# 5. Conclusion (comment):
''',
  '''aq <- na.omit(airquality[, c("Ozone", "Temp")])
r_f <- cor(aq$Temp, aq$Ozone)
r_c <- cor((aq$Temp - 32) * 5 / 9, aq$Ozone)
r_swap <- cor(aq$Ozone, aq$Temp)
round(c(r_f, r_c, r_swap), 4)
ct <- cor.test(aq$Temp, aq$Ozone)
round(c(r = unname(ct$estimate), p = ct$p.value), 4); round(ct$conf.int, 3)
# r has no units and is symmetric; the positive association is highly significant.''', [("r", "r_f", 4)]),
N(5, 5, "Cautions: outliers and non-linear patterns", "With `anscombe`, compute r for the four (x, y) pairs and plot them in a 2 × 2 grid. Then show how one outlier changes r for made-up data. Write 3 sentences of cautions about correlation.",
  '''set.seed(5)
x <- 1:20; y <- 2 + 0.5 * x + rnorm(20)''',
  '''# 1. r for anscombe x1-y1 ... x4-y4
# 2. par(mfrow = c(2, 2)) and four plots
# 3. r for (x, y), then add the point (40, 2) and recompute
# 4. Report (3 sentences as comments):
''',
  '''r4 <- sapply(1:4, function(i) cor(anscombe[[paste0("x", i)]], anscombe[[paste0("y", i)]]))
round(r4, 3)
par(mfrow = c(2, 2))
for (i in 1:4) plot(anscombe[[paste0("x", i)]], anscombe[[paste0("y", i)]], pch = 16, main = paste("Set", i))
par(mfrow = c(1, 1))
r_before <- cor(x, y); r_after <- cor(c(x, 40), c(y, 2))
round(c(r_before = r_before, r_after = r_after), 3)
# The four Anscombe sets share the same r but look completely different: always plot first.
# A single outlier can change r a lot.
# Correlation measures only LINEAR association and never proves causation.''', [("r_after", "r_after", 3)]),
]

B = [
N(6, 1, "Fit a least-squares line", "Regress mpg on wt and interpret the slope.", "", "",
  '''# === Complete example — read and run ===
fit <- lm(mpg ~ wt, data = mtcars)
coef(fit)
plot(mpg ~ wt, data = mtcars, pch = 16); abline(fit, col = "red", lwd = 2)
# Slope: each extra 1,000 lb is associated with about 5.34 fewer mpg on average.''', [("slope", "coef(fit)[2]", 4), ("intercept", "coef(fit)[1]", 4)]),
N(7, 2, "Slope and intercept from formulas", "b1 = r · sy / sx and b0 = ȳ − b1 · x̄. Check against coef().", "",
  '''x <- mtcars$wt; y <- mtcars$mpg
b1 <- cor(x, y) * ___(y) / ___(x)
b0 <- mean(___) - b1 * mean(___)
round(c(b0 = b0, b1 = b1), 4)''',
  '''x <- mtcars$wt; y <- mtcars$mpg
b1 <- cor(x, y) * sd(y) / sd(x)
b0 <- mean(y) - b1 * mean(x)
round(c(b0 = b0, b1 = b1), 4)''', [("b1", "b1", 4)]),
N(8, 3, "Residuals and prediction", "Predict mpg for a car of 3,000 lb (wt = 3). Find the residual of the Mazda RX4 and the car with the largest positive residual.", "",
  "# Write all your code here\n",
  '''pred3 <- predict(fit, newdata = data.frame(wt = 3))
round(pred3, 3)
res <- resid(fit)
round(res["Mazda RX4"], 3)
names(which.max(res))''', [("pred3", "pred3", 3)]),
N(9, 4, "Is the line appropriate?", "Check the mpg ~ wt model: residual plot, R² and the residual standard error. Then try mpg ~ hp and compare R².", "",
  '''# 1. plot(fitted(fit), resid(fit)); abline(h = 0)
# 2. R-squared and residual standard error from summary(fit)
# 3. fit_hp <- lm(mpg ~ hp, data = mtcars): its R-squared
# 4. Conclusion (comment): which predictor explains more variation?
''',
  '''plot(fitted(fit), resid(fit), pch = 16); abline(h = 0, col = "red")
s <- summary(fit)
round(c(r2 = s$r.squared, sigma = s$sigma), 4)
fit_hp <- lm(mpg ~ hp, data = mtcars)
round(summary(fit_hp)$r.squared, 4)
# Conclusion: weight explains more of the variation in mpg (higher R-squared) than horsepower.
# The residual plot shows a slight curve, a hint that a straight line is not perfect.''', [("r2", "s$r.squared", 4)]),
N(10, 5, "Why least squares?", "Compare the sum of squared residuals (SSE) of the least-squares line with two other lines (y = 37 − 5x and y = 40 − 6x) for mpg ~ wt. Show that R² = r². Write 3 sentences.", "",
  '''# 1. SSE function for a given intercept and slope
# 2. SSE for the lm line and the two other lines
# 3. R-squared vs cor(wt, mpg)^2
# 4. Report (3 sentences as comments):
''',
  '''sse <- function(b0, b1) sum((mtcars$mpg - (b0 + b1 * mtcars$wt))^2)
c(lm = sse(coef(fit)[1], coef(fit)[2]), line1 = sse(37, -5), line2 = sse(40, -6))
round(c(R2 = summary(fit)$r.squared, r_sq = cor(mtcars$wt, mtcars$mpg)^2), 4)
# The least-squares line has the smallest possible sum of squared residuals.
# Any other line, even a close one, has a larger SSE.
# In simple regression, R-squared equals the square of the correlation.''', [("sse_lm", "sum(resid(fit)^2)", 2)]),
]

C = [
N(11, 1, "Inference for the slope", "Is the slope of mpg ~ wt different from 0?", "", "",
  '''# === Complete example — read and run ===
s <- summary(fit)
s$coefficients                      # estimate, SE, t value, p-value
round(confint(fit, level = 0.95), 4)
# t = estimate / SE, df = n - 2''', [("t_slope", "summary(fit)$coefficients[2, 3]", 3)]),
N(12, 2, "Slope t statistic and CI by hand", "Rebuild t and the 95% CI for the slope from its estimate and SE.", "",
  '''est <- summary(fit)$coefficients["wt", "___"]
se  <- summary(fit)$coefficients["wt", "___"]
t_stat <- est / se
df <- nrow(mtcars) - ___
tstar <- qt(___, df)
round(c(t = t_stat, lower = est - tstar * se, upper = est + tstar * se), 4)''',
  '''est <- summary(fit)$coefficients["wt", "Estimate"]
se  <- summary(fit)$coefficients["wt", "Std. Error"]
t_stat <- est / se
df <- nrow(mtcars) - 2
tstar <- qt(0.975, df)
round(c(t = t_stat, lower = est - tstar * se, upper = est + tstar * se), 4)''', [("lower", "est - tstar * se", 4)]),
N(13, 3, "Ozone and temperature", "Regress Ozone on Temp (`airquality`, complete cases). Report the slope, its 95% CI, p-value and R². Interpret the slope in context.", "",
  "# Write all your code here\n",
  '''aq <- na.omit(airquality)
fit_aq <- lm(Ozone ~ Temp, data = aq)
round(coef(fit_aq), 4)
round(confint(fit_aq)["Temp", ], 4)
signif(summary(fit_aq)$coefficients["Temp", 4], 3)
round(summary(fit_aq)$r.squared, 4)
# Each extra degree F is associated with about 2.4 ppb more ozone on average.''', [("slope", "coef(fit_aq)[2]", 4)]),
N(14, 4, "Faithful eruptions", "A park ranger predicts the waiting time to the next eruption from the eruption length (`faithful`). Fit the model, test the slope, and give a 95% prediction interval for a 4-minute eruption.", "",
  '''# 1. Scatterplot and lm(waiting ~ eruptions)
# 2. Slope, its p-value and R-squared
# 3. 95% prediction interval for eruptions = 4
# 4. Advice for visitors (comment):
''',
  '''plot(waiting ~ eruptions, data = faithful, pch = 16)
fit_f <- lm(waiting ~ eruptions, data = faithful)
abline(fit_f, col = "red")
round(c(slope = unname(coef(fit_f)[2]), r2 = summary(fit_f)$r.squared), 4)
pi4 <- predict(fit_f, newdata = data.frame(eruptions = 4), interval = "prediction")
round(pi4, 2)
# Advice: after a 4-minute eruption, expect the next one roughly 65 to 88 minutes later.''', [("fit4", "pi4[1]", 2), ("pi_lower", "pi4[2]", 2)]),
N(15, 5, "Does the slope hold up?", "Use bootstrapping (`set.seed(15)`, 2,000 resamples of rows of mtcars) to get a 95% percentile interval for the mpg ~ wt slope and compare it with confint(). Write 3 sentences.", "",
  '''# 1. A function that refits lm on a resample of rows and returns the slope
# 2. 2,000 bootstrap slopes
# 3. quantile(..., c(0.025, 0.975)) vs confint(fit)
# 4. Report (3 sentences as comments):
''',
  '''set.seed(15)
boot_slopes <- replicate(2000, {
  idx <- sample(nrow(mtcars), replace = TRUE)
  coef(lm(mpg ~ wt, data = mtcars[idx, ]))[2]
})
round(rbind(bootstrap = quantile(boot_slopes, c(0.025, 0.975)), t_based = confint(fit)["wt", ]), 3)
hist(boot_slopes, breaks = 40, col = "lightblue")
# Both intervals are clearly below zero: heavier cars get fewer miles per gallon.
# The bootstrap interval does not rely on normal residuals.
# The two intervals are similar, which supports the t-based inference.''', [("boot_lower", "quantile(boot_slopes, 0.025)", 2)]),
]

D = [
N(16, 1, "A categorical predictor", "Regress mpg on transmission type (am as a factor).", "", "",
  '''# === Complete example — read and run ===
mtcars$trans <- factor(mtcars$am, labels = c("auto", "manual"))
fit_c <- lm(mpg ~ trans, data = mtcars)
coef(fit_c)
tapply(mtcars$mpg, mtcars$trans, mean)
# Intercept = mean of the baseline (auto); slope = manual - auto.''', [("diff", "coef(fit_c)[2]", 4)]),
N(17, 2, "Three-level factor", "Regress mpg on number of cylinders as a factor and read the coefficients.", "",
  '''mtcars$cyl_f <- factor(mtcars$___)
fit_cyl <- lm(mpg ~ ___, data = mtcars)
round(coef(fit_cyl), 4)
round(tapply(mtcars$mpg, mtcars$___, mean), 4)''',
  '''mtcars$cyl_f <- factor(mtcars$cyl)
fit_cyl <- lm(mpg ~ cyl_f, data = mtcars)
round(coef(fit_cyl), 4)
round(tapply(mtcars$mpg, mtcars$cyl_f, mean), 4)''', [("cyl8", "coef(fit_cyl)[3]", 4)]),
N(18, 3, "Multiple regression", "Fit mpg ~ wt + hp. Compare the wt coefficient with the simple model and report adjusted R² for both models.", "",
  "# Write all your code here\n",
  '''fit_m <- lm(mpg ~ wt + hp, data = mtcars)
round(coef(fit_m), 4)
round(c(simple = summary(fit)$adj.r.squared, multiple = summary(fit_m)$adj.r.squared), 4)
# The wt coefficient moves from about -5.3 to about -3.9 because hp now explains part of the variation.''', [("adj_r2", "summary(fit_m)$adj.r.squared", 4)]),
N(19, 4, "Predicting with two predictors", "A buyer wants the expected mpg of a 3,200 lb car with 150 hp, with a 95% confidence interval for the mean and a 95% prediction interval for one car.", "",
  '''# 1. newcar <- data.frame(wt = 3.2, hp = 150)
# 2. predict(..., interval = "confidence")
# 3. predict(..., interval = "prediction")
# 4. Explain the difference (comment):
''',
  '''newcar <- data.frame(wt = 3.2, hp = 150)
ci <- predict(fit_m, newcar, interval = "confidence")
pi <- predict(fit_m, newcar, interval = "prediction")
round(rbind(confidence = ci, prediction = pi), 2)
# The CI is for the AVERAGE mpg of all such cars; the PI is for ONE car, so it is much wider.''', [("fit", "ci[1]", 2)]),
N(20, 5, "Model report", "Compare three models for mpg: wt; wt + hp; wt + hp + trans. Use adjusted R², the residual SE and the p-value of each new term. Choose a model and write a 4-sentence report.", "",
  '''# 1. Fit the three models
# 2. Table of adjusted R-squared and sigma
# 3. anova(model2, model3): does trans add anything?
# 4. Residual plot of the chosen model
# 5. Report (4 sentences as comments):
''',
  '''m1 <- lm(mpg ~ wt, data = mtcars)
m2 <- lm(mpg ~ wt + hp, data = mtcars)
m3 <- lm(mpg ~ wt + hp + trans, data = mtcars)
cmp <- sapply(list(m1 = m1, m2 = m2, m3 = m3), function(m) c(adj_r2 = summary(m)$adj.r.squared, sigma = summary(m)$sigma))
round(cmp, 4)
anova(m2, m3)
plot(fitted(m2), resid(m2), pch = 16); abline(h = 0, col = "red")
# Adding hp to weight raises adjusted R-squared and lowers the residual SE.
# Adding transmission type does not improve the model significantly (see anova).
# We choose mpg ~ wt + hp as a simple model that explains most of the variation.
# The residual plot still shows mild curvature, so a transformation could be tried next.''', [("adj_m2", "summary(m2)$adj.r.squared", 4)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  M6 QUICK REFERENCE                                  ║
║  plot(y ~ x, data = df)   cor(x, y)   cor(df)        ║
║  cor.test(x, y)   pairs(df)                          ║
║  fit <- lm(y ~ x, data = df)  coef  resid  fitted    ║
║  b1 = r * sy / sx     b0 = ybar - b1 * xbar          ║
║  summary(fit)$r.squared   $sigma   $coefficients     ║
║  confint(fit)   t = estimate / SE   df = n - 2       ║
║  predict(fit, newdata, interval = 'confidence')      ║
║  predict(fit, newdata, interval = 'prediction')      ║
║  factor predictors: lm(y ~ factor(g))  baseline      ║
║  lm(y ~ x1 + x2)  adj.r.squared  anova(m1, m2)       ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/stats/m6_corr_basics.html (M6 correlation & regression)"
MOD = dict(key="n550_m6", title="550 M6 — Correlation & Linear Regression: R Coding Practice (20 Questions)",
           file="m6_practice_v1.Rmd", folder=SRC + "/Module 6", wd=SRC + "/Module 6",
           data_note="No data files are needed: built-in data sets (mtcars, airquality, anscombe, faithful).",
           header_link=LINK, site_rmd=[STATS + "/rmd"],
           topics=[("Correlation", A), ("Least-squares Regression", B),
                   ("Inference for the Slope & Prediction", C), ("Categorical & Multiple Regression", D)], card=CARD)
MOD["questions"] = A + B + C + D
