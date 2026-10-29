"""650 M6: logistic regression — probability/odds/log-odds, glm(), interpreting coefficients,
deviance/AIC/z/pseudo R², prediction & classification (MASS::birthwt, mtcars)."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]
LIB = '''library(MASS)        # birthwt data
bw <- birthwt
bw$smoke_f <- factor(bw$smoke, labels = c("no", "yes"))
bw$race_f <- factor(bw$race, labels = c("white", "black", "other"))'''

A = [
N(1, 1, "Probability, odds and log-odds", "Convert between the three scales for p = 0.2.", "", "",
  '''# === Complete example — read and run ===
p <- 0.2
odds <- p / (1 - p)
logit <- log(odds)
round(c(p = p, odds = odds, logit = logit), 4)
# back again
round(c(odds = exp(logit), p = exp(logit) / (1 + exp(logit)), plogis = plogis(logit)), 4)''', [("logit", "logit", 4)]),
N(2, 2, "The logistic curve", "Draw p = plogis(x) for x from −6 to 6 and find the x where p = 0.9.", "",
  '''curve(___(x), from = -6, to = 6, ylab = "probability", xlab = "log-odds")
abline(h = 0.5, lty = 2)
x90 <- qlogis(___)
round(x90, 4)''',
  '''curve(plogis(x), from = -6, to = 6, ylab = "probability", xlab = "log-odds")
abline(h = 0.5, lty = 2)
x90 <- qlogis(0.9)
round(x90, 4)''', [("x90", "qlogis(0.9)", 4)]),
N(3, 3, "Why not a straight line?", "For mtcars, fit a linear model am ~ wt and a logistic model. Show that the linear model predicts probabilities below 0 or above 1 for some cars.", "",
  "# Write all your code here\n",
  '''lin <- lm(am ~ wt, data = mtcars)
logi <- glm(am ~ wt, data = mtcars, family = binomial)
range(fitted(lin))
range(fitted(logi))
sum(fitted(lin) < 0 | fitted(lin) > 1)''', [("n_bad", "sum(fitted(lm(am ~ wt, data = mtcars)) < 0 | fitted(lm(am ~ wt, data = mtcars)) > 1)", 0)]),
N(4, 4, "Low birth weight: first model", "A clinic studies low birth weight (`low`, 1 = under 2.5 kg) in `birthwt`. Fit low ~ smoke_f, report the coefficients and the predicted probability for smokers and non-smokers.", LIB,
  '''# 1. glm(low ~ smoke_f, family = binomial, data = bw)
# 2. Coefficients on the log-odds scale
# 3. predict(type = "response") for both groups
# 4. Check against the raw proportions with tapply()
''',
  '''m1 <- glm(low ~ smoke_f, family = binomial, data = bw)
round(coef(m1), 4)
round(predict(m1, data.frame(smoke_f = c("no", "yes")), type = "response"), 4)
round(tapply(bw$low, bw$smoke_f, mean), 4)
# With one binary predictor the fitted probabilities equal the group proportions.''', [("p_smoker", "mean(bw$low[bw$smoke == 1])", 4)]),
N(5, 5, "From the coefficients to a story", "Using m1, compute by hand: the odds for non-smokers (exp of the intercept), the odds for smokers, and the odds ratio. Explain in 3 sentences what the odds ratio means for a parent.", LIB,
  '''# 1. odds_no  <- exp(b0)
# 2. odds_yes <- exp(b0 + b1)
# 3. odds ratio = odds_yes / odds_no = exp(b1)
# 4. Report (3 sentences as comments):
''',
  '''m1 <- glm(low ~ smoke_f, family = binomial, data = bw)
b <- coef(m1)
odds_no <- exp(b[1]); odds_yes <- exp(b[1] + b[2])
or <- unname(exp(b[2]))
round(c(odds_no = unname(odds_no), odds_yes = unname(odds_yes), odds_ratio = or), 3)
# Mothers who smoke have about twice the odds of a low-birth-weight baby.
# Odds are not probabilities: the probability rises from about 25% to about 40%.
# The intercept is the log-odds for the baseline group (non-smokers).''', [("odds_ratio", "or", 3)]),
]

B = [
N(6, 1, "A continuous predictor", "Model low ~ lwt (mother's weight in pounds).", LIB, "",
  '''# === Complete example — read and run ===
m2 <- glm(low ~ lwt, family = binomial, data = bw)
round(coef(m2), 4)
round(exp(coef(m2)["lwt"]), 4)          # odds ratio per extra pound
round(exp(10 * coef(m2)["lwt"]), 4)     # per extra 10 pounds''', [("or10", "exp(10 * coef(glm(low ~ lwt, family = binomial, data = bw))['lwt'])", 4)]),
N(7, 2, "Two predictors", "Fit low ~ smoke_f + lwt and interpret the smoking odds ratio holding weight fixed.", LIB,
  '''m3 <- glm(low ~ ___ + ___, family = ___, data = bw)
round(exp(coef(m3)), 4)
round(exp(confint.default(___)), 4)      # Wald 95% CIs on the odds scale''',
  '''m3 <- glm(low ~ smoke_f + lwt, family = binomial, data = bw)
round(exp(coef(m3)), 4)
round(exp(confint.default(m3)), 4)      # Wald 95% CIs on the odds scale''', [("or_smoke", "exp(coef(glm(low ~ smoke_f + lwt, family = binomial, data = bw)))[2]", 4)]),
N(8, 3, "Predicted probabilities for profiles", "Using m3, predict the probability of low birth weight for a smoker and a non-smoker who both weigh 110 lb and 160 lb (4 profiles).", LIB,
  "# Write all your code here\n",
  '''prof <- expand.grid(smoke_f = c("no", "yes"), lwt = c(110, 160))
prof$p_low <- round(predict(m3, prof, type = "response"), 4)
prof''', [("p_yes110", "predict(m3, data.frame(smoke_f = 'yes', lwt = 110), type = 'response')", 4)]),
N(9, 4, "Race as a categorical predictor", "`race` is coded 1 = white, 2 = black, 3 = other. Make it a factor with labels, fit low ~ smoke_f + lwt + race_f, and report the odds ratios with white as the baseline.", LIB,
  '''# 1. Check the factor bw$race_f (made in the data chunk): levels(bw$race_f)
# 2. glm(...)
# 3. exp(coef()) and the p-values
# 4. Interpretation (comment):
''',
  '''levels(bw$race_f)
m4 <- glm(low ~ smoke_f + lwt + race_f, family = binomial, data = bw)
round(cbind(OR = exp(coef(m4)), p = summary(m4)$coefficients[, 4]), 4)
# Compared with white mothers, the odds are higher for black and 'other' mothers, after adjusting for smoking and weight.''', [("or_black", "exp(coef(m4))['race_fblack']", 3)]),
N(10, 5, "The logistic curve for lwt", "Plot the predicted probability of low birth weight against lwt for smokers and non-smokers (model m3) on one graph, with the observed 0/1 values jittered. Write 3 sentences describing the plot.", LIB,
  '''# 1. A grid of lwt values for each smoking group
# 2. predict(type = "response") on the grid
# 3. plot the observed points (jitter) and two curves
# 4. Report (3 sentences as comments):
''',
  '''grid <- expand.grid(lwt = seq(80, 250, by = 2), smoke_f = c("no", "yes"))
grid$p <- predict(m3, grid, type = "response")
set.seed(10)
plot(bw$lwt, jitter(bw$low, 0.1), pch = 16, col = "gray60", xlab = "Mother's weight (lb)", ylab = "P(low)")
lines(grid$lwt[grid$smoke_f == "no"], grid$p[grid$smoke_f == "no"], col = "blue", lwd = 2)
lines(grid$lwt[grid$smoke_f == "yes"], grid$p[grid$smoke_f == "yes"], col = "red", lwd = 2)
legend("topright", c("non-smoker", "smoker"), col = c("blue", "red"), lwd = 2, bty = "n")
round(range(grid$p), 3)
# The probability of low birth weight falls as the mother's weight rises.
# At every weight the smokers' curve lies above the non-smokers' curve.
# The curves are S-shaped pieces, so equal steps in weight do not change the probability equally.''', [("p_max", "max(grid$p)", 3)]),
]

C = [
N(11, 1, "Deviance and AIC", "Compare the null and residual deviance of m3 and read the AIC.", LIB, "",
  '''# === Complete example — read and run ===
m3 <- glm(low ~ smoke_f + lwt, family = binomial, data = bw)
round(c(null_dev = m3$null.deviance, resid_dev = m3$deviance, AIC = AIC(m3)), 3)
# AIC = deviance + 2 * (number of coefficients)
round(m3$deviance + 2 * length(coef(m3)), 3)''', [("AIC", "AIC(m3)", 3)]),
N(12, 2, "Likelihood-ratio (deviance) test", "Is m3 better than the model with smoking only (m1)? Use anova(..., test = 'Chisq').", LIB,
  '''m1 <- glm(low ~ smoke_f, family = binomial, data = bw)
anova(___, ___, test = "___")
drop <- m1$deviance - m3$___
round(c(drop = drop, p = pchisq(drop, df = 1, lower.tail = ___)), 4)''',
  '''m1 <- glm(low ~ smoke_f, family = binomial, data = bw)
anova(m1, m3, test = "Chisq")
drop <- m1$deviance - m3$deviance
round(c(drop = drop, p = pchisq(drop, df = 1, lower.tail = FALSE)), 4)''', [("drop", "m1$deviance - m3$deviance", 4)]),
N(13, 3, "z values and McFadden R²", "From summary(m3), report the z value and p-value of each coefficient, and compute McFadden's pseudo R² = 1 − residual deviance / null deviance.", LIB,
  "# Write all your code here\n",
  '''round(summary(m3)$coefficients[, c("z value", "Pr(>|z|)")], 4)
mcf <- 1 - m3$deviance / m3$null.deviance
round(mcf, 4)''', [("mcfadden", "1 - m3$deviance / m3$null.deviance", 4)]),
N(14, 4, "Choosing a model by AIC", "The clinic considers five candidate models for low birth weight. Fit them, build an AIC table, and pick the best. Also run step() from the model with smoke_f, lwt, race_f, age, ptl, ht and ui.", LIB,
  '''# 1. Candidates: ~ smoke_f; ~ smoke_f + lwt; ~ smoke_f + lwt + race_f;
#    ~ smoke_f + lwt + race_f + ht; ~ smoke_f + lwt + race_f + ht + ui
# 2. AIC table, sorted
# 3. step() on the full model (trace = 0): which variables stay?
# 4. Recommendation (comment):
''',
  '''forms <- list(a = low ~ smoke_f, b = low ~ smoke_f + lwt, c = low ~ smoke_f + lwt + race_f,
              d = low ~ smoke_f + lwt + race_f + ht, e = low ~ smoke_f + lwt + race_f + ht + ui)
aics <- sapply(forms, function(f) AIC(glm(f, family = binomial, data = bw)))
round(sort(aics), 2)
full <- glm(low ~ smoke_f + lwt + race_f + age + ptl + ht + ui, family = binomial, data = bw)
best <- step(full, trace = 0)
formula(best)
# Recommendation: use the model with the lowest AIC; step() confirms which predictors are worth keeping.''', [("aic_best", "min(aics)", 2)]),
N(15, 5, "The two K's in AIC", "AIC = −2·logLik + 2K, where K is the number of estimated coefficients. Compute it by hand for the best model from Q14, compare with AIC(), and show that a factor with 3 levels adds 2 to K. Write 3 sentences.", LIB,
  '''# 1. K <- length(coef(best)); ll <- logLik(best)
# 2. -2 * ll + 2 * K vs AIC(best)
# 3. K of a model with race_f vs without it
# 4. Report (3 sentences as comments):
''',
  '''K <- length(coef(best)); ll <- as.numeric(logLik(best))
round(c(by_hand = -2 * ll + 2 * K, AIC = AIC(best)), 3)
k_with <- length(coef(glm(low ~ smoke_f + lwt + race_f, family = binomial, data = bw)))
k_without <- length(coef(glm(low ~ smoke_f + lwt, family = binomial, data = bw)))
c(K_with_race = k_with, K_without_race = k_without)
# AIC rewards fit (low deviance) and penalises the number of coefficients K.
# A factor with 3 levels uses 2 dummy coefficients, so it costs 2 in K, not 1.
# Some software counts K differently (e.g. adding the dispersion), so compare AICs from the same function only.''', [("K", "K", 0)]),
]

D = [
N(16, 1, "Classify with a 0.5 threshold", "Turn predicted probabilities from the best model into 0/1 predictions and make a confusion matrix.", LIB, "",
  '''# === Complete example — read and run ===
# the model chosen by step() in Q14 (written out so this chunk runs on its own)
best <- glm(low ~ smoke_f + lwt + race_f + ptl + ht + ui, family = binomial, data = bw)
p_hat <- predict(best, type = "response")
pred <- ifelse(p_hat >= 0.5, 1, 0)
cm <- table(actual = bw$low, predicted = pred)
cm
accuracy <- mean(pred == bw$low)
round(accuracy, 4)''', [("accuracy", "accuracy", 4)]),
N(17, 2, "Sensitivity and specificity", "From the confusion matrix, compute sensitivity (true positive rate) and specificity (true negative rate).", LIB,
  '''TP <- cm["1", "1"]; FN <- cm["1", "___"]
TN <- cm["0", "0"]; FP <- cm["0", "___"]
sensitivity <- TP / (TP + ___)
specificity <- TN / (TN + ___)
round(c(sensitivity = sensitivity, specificity = specificity), 4)''',
  '''TP <- cm["1", "1"]; FN <- cm["1", "0"]
TN <- cm["0", "0"]; FP <- cm["0", "1"]
sensitivity <- TP / (TP + FN)
specificity <- TN / (TN + FP)
round(c(sensitivity = sensitivity, specificity = specificity), 4)''', [("sensitivity", "sensitivity", 4)]),
N(18, 3, "Changing the threshold", "A screening programme wants to catch more at-risk babies. Recompute sensitivity, specificity and accuracy for thresholds 0.2, 0.3, 0.4 and 0.5.", LIB,
  "# Write all your code here\n",
  '''rates <- sapply(c(0.2, 0.3, 0.4, 0.5), function(th) {
  pr <- as.numeric(p_hat >= th)
  c(threshold = th, sens = mean(pr[bw$low == 1] == 1), spec = mean(pr[bw$low == 0] == 0), acc = mean(pr == bw$low))
})
round(t(rates), 3)''', [("sens_03", "mean(as.numeric(p_hat >= 0.3)[bw$low == 1] == 1)", 3)]),
N(19, 4, "Test-set performance", "Split birthwt 70/30 (`set.seed(19)`), fit the best formula on the training set and report the test accuracy, sensitivity and specificity at threshold 0.3.", LIB,
  '''# 1. idx <- sample(nrow(bw), round(0.7 * nrow(bw)))
# 2. glm(formula(best), family = binomial, data = train)
# 3. Test predictions at threshold 0.3
# 4. Comment: how does test accuracy compare with Q18?
''',
  '''set.seed(19)
idx <- sample(nrow(bw), round(0.7 * nrow(bw)))
train <- bw[idx, ]; test <- bw[-idx, ]
mt <- glm(formula(best), family = binomial, data = train)
pt_hat <- predict(mt, test, type = "response")
pr <- as.numeric(pt_hat >= 0.3)
round(c(acc = mean(pr == test$low), sens = mean(pr[test$low == 1] == 1), spec = mean(pr[test$low == 0] == 0)), 3)
# Comment: performance on new data is usually a little worse than on the training data.''', [("test_acc", "mean(pr == test$low)", 3)]),
N(20, 5, "German-credit style scoring (simulated)", "Simulate 1,000 loan applicants (`set.seed(20)`) whose default probability depends on income and debt ratio, fit a logistic model, interpret the odds ratios, and choose a threshold that keeps the false-positive rate below 20%. Write a 4-sentence report for a loan officer.",
  '''set.seed(20)
n <- 1000
income <- round(rlnorm(n, log(50), 0.4), 1)           # $1000s
debt_ratio <- round(runif(n, 0, 0.8), 2)
p_default <- plogis(-1 - 0.03 * income + 4 * debt_ratio)
loans <- data.frame(income, debt_ratio, default = rbinom(n, 1, p_default))''',
  '''# 1. glm(default ~ income + debt_ratio, family = binomial)
# 2. Odds ratios: per $10,000 income and per +0.1 debt ratio
# 3. False-positive rate (good customers flagged) for thresholds 0.2-0.6
# 4. The lowest threshold with FPR < 0.20
# 5. Report (4 sentences as comments):
''',
  '''mL <- glm(default ~ income + debt_ratio, family = binomial, data = loans)
round(c(or_income_10k = exp(10 * coef(mL)["income"]), or_debt_01 = exp(0.1 * coef(mL)["debt_ratio"])), 3)
ph <- predict(mL, type = "response")
ths <- seq(0.2, 0.6, by = 0.05)
fpr <- sapply(ths, function(t) mean(ph[loans$default == 0] >= t))
round(rbind(threshold = ths, fpr = fpr), 3)
chosen <- min(ths[fpr < 0.20])
chosen
# Higher income lowers the odds of default; a higher debt ratio raises them.
# The model turns each applicant into a default probability.
# A threshold is a business choice: lower thresholds catch more defaults but reject more good customers.
# The chosen threshold keeps wrongly rejected good customers below 20%.''', [("chosen", "chosen", 2)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M6 QUICK REFERENCE (logistic regression)        ║
║  odds = p / (1 - p)   logit = log(odds)              ║
║  plogis(x) = p from log-odds   qlogis(p) = log-odds  ║
║  glm(y ~ x, family = binomial, data = df)            ║
║  exp(coef(m)) = odds ratios   confint.default(m)     ║
║  predict(m, newdata, type = 'response') = p          ║
║  m$deviance  m$null.deviance  AIC(m)  logLik(m)      ║
║  anova(m_small, m_big, test = 'Chisq')               ║
║  McFadden R2 = 1 - deviance / null.deviance          ║
║  table(actual, predicted)  sensitivity  specificity  ║
║  threshold choice trades sensitivity vs specificity  ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/m6_ch1.html (650 M6 logistic regression, Ch.1-13)"
MOD = dict(key="n650_m6", title="650 M6 — Logistic Regression: R Coding Practice (20 Questions)",
           file="650_m6_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/M6", wd=R650 + "/650 - Data Visualization/M6",
           data_note="Needs only MASS (comes with R). Data: `birthwt` (MASS), `mtcars` and a simulated loan data set.",
           header_link=LINK, site_rmd=SITE,
           topics=[("Odds, Log-odds & the Logistic Model", A), ("Interpreting Coefficients", B),
                   ("Evaluating Models: Deviance, AIC, z", C), ("Prediction & Classification", D)], card=CARD)
MOD["questions"] = A + B + C + D
