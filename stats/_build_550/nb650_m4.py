"""650 M4: simple regression prediction, confidence vs prediction intervals, assumptions, non-normality & heteroskedasticity."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]

A = [
N(1, 1, "Fit and predict by hand", "Predict stopping distance from speed (`cars`).", "", "",
  '''# === Complete example — read and run ===
fit <- lm(dist ~ speed, data = cars)
b <- coef(fit)
b
pred_hand <- b[1] + b[2] * 21              # speed = 21 mph
pred_r <- predict(fit, newdata = data.frame(speed = 21))
round(c(hand = unname(pred_hand), predict = unname(pred_r)), 3)''', [("pred21", "pred_r", 3)]),
N(2, 2, "Predict several values", "Predict stopping distances for speeds 10, 15 and 20 mph with predict().", "",
  '''new <- data.frame(speed = c(___, ___, ___))
round(predict(___, newdata = ___), 2)''',
  '''new <- data.frame(speed = c(10, 15, 20))
round(predict(fit, newdata = new), 2)''', [("p15", "predict(fit, data.frame(speed = 15))", 2)]),
N(3, 3, "Interpolation vs extrapolation", "The data cover speeds 4–25 mph. Predict for speed = 2 and speed = 40, and explain in a comment why one of them is unreliable (look at the sign of the first prediction too).", "",
  "# Write all your code here\n",
  '''range(cars$speed)
round(predict(fit, data.frame(speed = c(2, 40))), 2)
# speed = 2 gives a negative distance and speed = 40 is far outside the data:
# both are extrapolations, so the straight line should not be trusted there.''', [("p2", "predict(fit, data.frame(speed = 2))", 2)]),
N(4, 4, "Ice-cream sales", "A shop records daily temperature (°C) and ice-cream sales (made-up). Fit a line, interpret the slope, and predict sales for a 30 °C day.",
  '''set.seed(4)
temp <- round(runif(40, 18, 34), 1)
sales <- round(60 + 9 * temp + rnorm(40, 0, 25))
shop <- data.frame(temp, sales)''',
  '''# 1. Scatterplot with the fitted line
# 2. Slope and its meaning (comment)
# 3. Predicted sales at 30 degrees
# 4. R-squared
''',
  '''fit_ice <- lm(sales ~ temp, data = shop)
plot(sales ~ temp, data = shop, pch = 16); abline(fit_ice, col = "red")
round(coef(fit_ice), 3)
round(predict(fit_ice, data.frame(temp = 30)), 1)
round(summary(fit_ice)$r.squared, 3)
# Each extra degree is associated with about 9 more ice creams sold on average.''', [("pred30", "predict(fit_ice, data.frame(temp = 30))", 1)]),
N(5, 5, "Residuals tell the story", "For the cars model, add fitted values and residuals to a data frame, find the three cars with the largest absolute residuals, and check that the residuals sum to 0. Write 3 sentences on what a residual means.", "",
  '''# 1. cars2 <- cars; cars2$fitted <- fitted(fit); cars2$resid <- resid(fit)
# 2. Rows with the 3 largest |resid|
# 3. sum(resid) and mean(resid)
# 4. Report (3 sentences as comments):
''',
  '''cars2 <- cars
cars2$fitted <- fitted(fit); cars2$resid <- resid(fit)
cars2[order(-abs(cars2$resid))[1:3], ]
round(c(sum = sum(cars2$resid), mean = mean(cars2$resid)), 10)
# A residual is observed minus predicted: how far the line misses each point.
# Positive residuals are cars that needed more distance than the line predicts.
# Least squares makes the residuals sum to exactly zero.''', [("max_abs_resid", "max(abs(resid(fit)))", 2)]),
]

B = [
N(6, 1, "Confidence vs prediction interval", "Compare the 95% CI for the mean distance and the 95% PI for one car at speed = 21.", "", "",
  '''# === Complete example — read and run ===
nd <- data.frame(speed = 21)
ci <- predict(fit, nd, interval = "confidence")
pi <- predict(fit, nd, interval = "prediction")
round(rbind(confidence = ci, prediction = pi), 2)''', [("pi_upper", "predict(fit, data.frame(speed = 21), interval = 'prediction')[3]", 2)]),
N(7, 2, "Different confidence levels", "Find 90% and 99% prediction intervals at speed = 21.", "",
  '''round(predict(fit, data.frame(speed = 21), interval = "___", level = ___), 2)
round(predict(fit, data.frame(speed = 21), interval = "prediction", level = ___), 2)''',
  '''round(predict(fit, data.frame(speed = 21), interval = "prediction", level = 0.90), 2)
round(predict(fit, data.frame(speed = 21), interval = "prediction", level = 0.99), 2)''', [("pi99_low", "predict(fit, data.frame(speed = 21), interval = 'prediction', level = 0.99)[2]", 2)]),
N(8, 3, "Interval width across x", "Compute the CI width at speeds 5, 15 and 25. Where is the interval narrowest and why?", "",
  "# Write all your code here\n",
  '''ci3 <- predict(fit, data.frame(speed = c(5, 15, 25)), interval = "confidence")
width <- ci3[, "upr"] - ci3[, "lwr"]
round(width, 2)
mean(cars$speed)
# Narrowest near the mean speed (about 15.4): the line is most certain at the centre of the data.''', [("width15", "diff(predict(fit, data.frame(speed = 15), interval = 'confidence')[2:3])", 2)]),
N(9, 4, "Bands on a plot", "Draw the cars scatterplot with the fitted line, the 95% confidence band and the 95% prediction band (use a grid of speeds from 4 to 25).", "",
  '''# 1. grid <- data.frame(speed = seq(4, 25, by = 0.5))
# 2. ci and pi on the grid
# 3. plot + lines() for fit, lwr and upr of both
# 4. What share of the cars lie inside the prediction band? (comment)
''',
  '''grid <- data.frame(speed = seq(4, 25, by = 0.5))
ci_g <- predict(fit, grid, interval = "confidence")
pi_g <- predict(fit, grid, interval = "prediction")
plot(dist ~ speed, data = cars, pch = 16)
lines(grid$speed, ci_g[, "fit"], col = "red", lwd = 2)
lines(grid$speed, ci_g[, "lwr"], col = "red", lty = 2); lines(grid$speed, ci_g[, "upr"], col = "red", lty = 2)
lines(grid$speed, pi_g[, "lwr"], col = "blue", lty = 3); lines(grid$speed, pi_g[, "upr"], col = "blue", lty = 3)
pi_obs <- predict(fit, cars, interval = "prediction")
inside <- mean(cars$dist >= pi_obs[, "lwr"] & cars$dist <= pi_obs[, "upr"])
inside
# About 95% of the cars fall inside the prediction band, as expected.''', [("inside", "inside", 2)]),
N(10, 5, "PI by hand", "Rebuild the 95% PI at speed = 21 from the formula ŷ ± t* · s · sqrt(1 + 1/n + (x0 − x̄)² / Σ(x − x̄)²) and compare with predict(). Also compute the CI version (without the 1). Write 3 sentences on why the PI is wider.", "",
  '''# 1. s (residual SE), n, xbar, Sxx
# 2. t* with df = n - 2
# 3. PI and CI by hand
# 4. Compare with predict()
# 5. Report (3 sentences as comments):
''',
  '''s <- summary(fit)$sigma; n <- nrow(cars); xbar <- mean(cars$speed)
sxx <- sum((cars$speed - xbar)^2); x0 <- 21
yhat <- unname(predict(fit, data.frame(speed = x0)))
tstar <- qt(0.975, n - 2)
pi_hand <- yhat + c(-1, 1) * tstar * s * sqrt(1 + 1 / n + (x0 - xbar)^2 / sxx)
ci_hand <- yhat + c(-1, 1) * tstar * s * sqrt(1 / n + (x0 - xbar)^2 / sxx)
round(rbind(pi_hand, ci_hand), 2)
# The CI only covers uncertainty about where the mean line is.
# The PI adds the scatter of a single car around the line (the extra 1 inside the root).
# That individual scatter never shrinks with more data, so the PI stays wide.''', [("pi_low", "pi_hand[1]", 2)]),
]

C = [
N(11, 1, "Diagnostic plots", "Look at the four standard diagnostic plots of the cars model.", "", "",
  '''# === Complete example — read and run ===
par(mfrow = c(2, 2))
plot(fit)              # residuals vs fitted, Q-Q, scale-location, leverage
par(mfrow = c(1, 1))
round(summary(fit)$sigma, 3)''', [("sigma", "summary(fit)$sigma", 3)]),
N(12, 2, "Normality of residuals", "Check the normality of the residuals with a Q-Q plot and shapiro.test().", "",
  '''r <- ___(fit)
qqnorm(r); qqline(r, col = "red")
sw <- ___(r)
round(sw$p.value, 4)''',
  '''r <- resid(fit)
qqnorm(r); qqline(r, col = "red")
sw <- shapiro.test(r)
round(sw$p.value, 4)''', [("sw_p", "shapiro.test(resid(fit))$p.value", 4)]),
N(13, 3, "Constant variance (Breusch–Pagan)", "Run lmtest::bptest() on the cars model and on a model for log(dist). Report both p-values.", "library(lmtest)",
  "# Write all your code here\n",
  '''bp1 <- bptest(fit)
fit_log <- lm(log(dist) ~ speed, data = cars)
bp2 <- bptest(fit_log)
round(c(raw = unname(bp1$p.value), log = unname(bp2$p.value)), 4)''', [("bp_raw", "lmtest::bptest(fit)$p.value", 4)]),
N(14, 4, "Independence (Durbin–Watson)", "Ozone readings in `airquality` are recorded day after day. Fit Ozone ~ Temp (complete cases) and test the residuals for autocorrelation with car::durbinWatsonTest() (`set.seed(14)` because it uses a bootstrap p-value).", "library(car)",
  '''# 1. aq <- na.omit(airquality); fit_aq <- lm(Ozone ~ Temp, data = aq)
# 2. durbinWatsonTest(fit_aq)
# 3. Plot residuals in time order
# 4. Conclusion (comment):
''',
  '''aq <- na.omit(airquality)
fit_aq <- lm(Ozone ~ Temp, data = aq)
set.seed(14)
dw <- durbinWatsonTest(fit_aq)
dw
plot(resid(fit_aq), type = "b", pch = 16, ylab = "Residual (time order)"); abline(h = 0, col = "red")
# A DW statistic near 2 means no autocorrelation; values well below 2 suggest positive autocorrelation.''', [("dw", "car::durbinWatsonTest(lm(Ozone ~ Temp, data = na.omit(airquality)), reps = 100)$dw", 3)]),
N(15, 5, "Full assumption check", "Check all four LINE assumptions for Ozone ~ Temp (airquality, complete cases): Linearity, Independence, Normality, Equal variance. Use a plot or a test for each and write a 4-sentence verdict.", "library(lmtest)\nlibrary(car)",
  '''# L: residuals vs fitted
# I: durbinWatsonTest()
# N: Q-Q plot + shapiro.test()
# E: bptest()
# Verdict (4 sentences as comments):
''',
  '''aq <- na.omit(airquality)
fit_aq <- lm(Ozone ~ Temp, data = aq)
plot(fitted(fit_aq), resid(fit_aq), pch = 16); abline(h = 0, col = "red")
set.seed(15)
dw_p <- durbinWatsonTest(fit_aq)$p
sw_p <- shapiro.test(resid(fit_aq))$p.value
bp_p <- unname(bptest(fit_aq)$p.value)
signif(c(dw_p = dw_p, shapiro_p = sw_p, bp_p = bp_p), 3)
# Linearity: the residual plot curves, so a straight line is not ideal.
# Independence: the Durbin-Watson p-value is large, so there is no sign of autocorrelation.
# Normality fails clearly (tiny Shapiro p-value); the Breusch-Pagan test does not flag unequal variance here.
# Verdict: the skewed residuals are the main problem - try transforming Ozone (Topic D).''', [("sw_p", "sw_p", 6)]),
]

D = [
N(16, 1, "Log transformation", "Model log(Ozone) instead of Ozone and compare the residual normality.", "", "",
  '''# === Complete example — read and run ===
aq <- na.omit(airquality)
fit_raw <- lm(Ozone ~ Temp, data = aq)
fit_lg  <- lm(log(Ozone) ~ Temp, data = aq)
round(c(raw = shapiro.test(resid(fit_raw))$p.value, log = shapiro.test(resid(fit_lg))$p.value), 4)
par(mfrow = c(1, 2)); qqnorm(resid(fit_raw)); qqnorm(resid(fit_lg)); par(mfrow = c(1, 1))''', [("sw_log", "shapiro.test(resid(lm(log(Ozone) ~ Temp, data = na.omit(airquality))))$p.value", 4)]),
N(17, 2, "Predicting on the original scale", "Predict Ozone at Temp = 85 from the log model and back-transform with exp().", "",
  '''pred_log <- predict(fit_lg, data.frame(Temp = ___), interval = "prediction")
round(___(pred_log), 2)            # back to ppb''',
  '''pred_log <- predict(fit_lg, data.frame(Temp = 85), interval = "prediction")
round(exp(pred_log), 2)            # back to ppb''', [("fit85", "exp(predict(fit_lg, data.frame(Temp = 85)))", 2)]),
N(18, 3, "Square-root transformation", "Try sqrt(dist) ~ speed for the cars data. Compare R² and the Breusch–Pagan p-value with the original model.", "library(lmtest)",
  "# Write all your code here\n",
  '''fit_sq <- lm(sqrt(dist) ~ speed, data = cars)
round(c(r2_raw = summary(fit)$r.squared, r2_sqrt = summary(fit_sq)$r.squared), 3)
round(c(bp_raw = unname(bptest(fit)$p.value), bp_sqrt = unname(bptest(fit_sq)$p.value)), 4)''', [("r2_sqrt", "summary(lm(sqrt(dist) ~ speed, data = cars))$r.squared", 3)]),
N(19, 4, "Robust standard errors", "When variance is not constant, heteroskedasticity-consistent SEs are an option. Compare the usual and HC3 standard errors of the slope for Ozone ~ Temp using car::hccm().", "library(car)",
  '''# 1. Usual SE from summary()
# 2. HC3 SE: sqrt(diag(hccm(fit_aq, type = "hc3")))
# 3. Compare the two t values
# 4. Comment: which SE should we report here?
''',
  '''aq <- na.omit(airquality)
fit_aq <- lm(Ozone ~ Temp, data = aq)
se_usual <- summary(fit_aq)$coefficients["Temp", "Std. Error"]
se_hc3 <- sqrt(diag(hccm(fit_aq, type = "hc3")))["Temp"]
round(c(usual = se_usual, hc3 = unname(se_hc3)), 4)
round(coef(fit_aq)["Temp"] / c(se_usual, se_hc3), 2)
# With unequal variance the robust (HC3) SE is the safer one to report.''', [("se_hc3", "sqrt(diag(car::hccm(lm(Ozone ~ Temp, data = na.omit(airquality)), type = 'hc3')))[2]", 4)]),
N(20, 5, "Before-and-after report", "Write a short analysis of Ozone ~ Temp: (1) the raw model and its assumption problems, (2) the log model and its checks, (3) a 95% prediction interval at 85 °F from each model. Finish with a 4-sentence recommendation.", "library(lmtest)",
  '''# 1. Raw model: R-squared, shapiro and bptest p-values
# 2. Log model: the same checks
# 3. PI at Temp = 85 from both models (back-transform the log one)
# 4. Recommendation (4 sentences as comments):
''',
  '''aq <- na.omit(airquality)
m_raw <- lm(Ozone ~ Temp, data = aq); m_log <- lm(log(Ozone) ~ Temp, data = aq)
chk <- function(m) c(r2 = summary(m)$r.squared, shapiro_p = shapiro.test(resid(m))$p.value, bp_p = unname(bptest(m)$p.value))
round(rbind(raw = chk(m_raw), log = chk(m_log)), 4)
nd <- data.frame(Temp = 85)
round(rbind(raw = predict(m_raw, nd, interval = "prediction"),
            log = exp(predict(m_log, nd, interval = "prediction"))), 2)
# The raw model has strongly skewed (non-normal) residuals.
# The log model's residuals are much closer to normal, but the Breusch-Pagan test now flags unequal variance.
# The back-transformed interval is asymmetric and cannot go below zero, which suits ozone.
# Recommendation: prefer the log model, report intervals on the ppb scale, and add robust SEs (Q19) because no model is perfect.''', [("r2_log", "summary(m_log)$r.squared", 4)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M4 QUICK REFERENCE (simple regression)          ║
║  fit <- lm(y ~ x, data)  coef  fitted  resid         ║
║  predict(fit, newdata = data.frame(x = ...))         ║
║  interval = 'confidence' (mean) / 'prediction' (one) ║
║  level = 0.90 / 0.99                                 ║
║  plot(fit)  qqnorm(resid)  shapiro.test(resid(fit))  ║
║  lmtest::bptest(fit)    car::durbinWatsonTest(fit)   ║
║  LINE: Linearity Independence Normality Equal var    ║
║  fixes: log(y)  sqrt(y)  car::hccm(fit, 'hc3')       ║
║  back-transform: exp(predict(log_model, ...))        ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/m4_predict.html (650 M4 prediction & assumptions)"
MOD = dict(key="n650_m4", title="650 M4 — Prediction, Intervals & Regression Assumptions: R Coding Practice (20 Questions)",
           file="650_m4_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/M4", wd=R650 + "/650 - Data Visualization/M4",
           data_note="Needs the lmtest and car packages (`install.packages(c(\"lmtest\", \"car\"))` once). Data: `cars`, `airquality` (built into R) and a small simulated data set.",
           header_link=LINK, site_rmd=SITE,
           topics=[("Predicting with a Regression Line", A), ("Confidence & Prediction Intervals", B),
                   ("Checking the Assumptions", C), ("Fixing Problems: Transformations & Robust SEs", D)], card=CARD)
MOD["questions"] = A + B + C + D
