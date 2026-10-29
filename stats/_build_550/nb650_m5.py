"""650 M5: multiple regression, diagnostics, standardized coefficients, influence, VIF, polynomial,
categorical & date predictors, interaction, variable selection and evaluation (MASS::Boston + mtcars)."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]
LIB = "library(MASS)      # Boston housing data\nlibrary(car)       # vif()"

A = [
N(1, 1, "A multiple regression", "Predict median home value (medv, $1000s) from rooms (rm), lower-status share (lstat) and pupil-teacher ratio (ptratio).", LIB, "",
  '''# === Complete example — read and run ===
fit <- lm(medv ~ rm + lstat + ptratio, data = Boston)
summary(fit)
round(coef(fit), 4)
# rm: one extra room is linked to about $4,500 more, holding lstat and ptratio fixed.''', [("b_rm", "coef(fit)['rm']", 4)]),
N(2, 2, "Reading the summary", "Extract R², adjusted R², the residual SE and the overall F-test p-value.", LIB,
  '''s <- summary(___)
r2 <- s$___; adj <- s$___; sigma <- s$___
f <- s$fstatistic
p_overall <- pf(f[1], f[2], f[3], lower.tail = ___)
round(c(r2 = r2, adj = adj, sigma = sigma), 4); signif(p_overall, 3)''',
  '''s <- summary(fit)
r2 <- s$r.squared; adj <- s$adj.r.squared; sigma <- s$sigma
f <- s$fstatistic
p_overall <- pf(f[1], f[2], f[3], lower.tail = FALSE)
round(c(r2 = r2, adj = adj, sigma = sigma), 4); signif(p_overall, 3)''', [("adj_r2", "summary(fit)$adj.r.squared", 4)]),
N(3, 3, "Standardized coefficients", "Which predictor matters most? Refit the model on scale()d variables (or multiply each slope by sd(x)/sd(y)) and compare the standardized coefficients.", LIB,
  "# Write all your code here\n",
  '''std <- coef(fit)[-1] * sapply(Boston[, c("rm", "lstat", "ptratio")], sd) / sd(Boston$medv)
round(std, 3)
fit_z <- lm(scale(medv) ~ scale(rm) + scale(lstat) + scale(ptratio), data = Boston)
round(coef(fit_z)[-1], 3)          # same numbers
names(which.max(abs(std)))''', [("std_lstat", "coef(fit)['lstat'] * sd(Boston$lstat) / sd(Boston$medv)", 3)]),
N(4, 4, "Diagnostics", "An analyst wants to trust this model. Check residuals vs fitted, the Q-Q plot, and count observations with |standardized residual| > 3.", LIB,
  '''# 1. par(mfrow = c(2, 2)); plot(fit)
# 2. rstandard(fit): how many beyond +/- 3?
# 3. Which homes are they (row numbers)?
# 4. Conclusion (comment):
''',
  '''par(mfrow = c(2, 2)); plot(fit); par(mfrow = c(1, 1))
rs <- rstandard(fit)
n_big <- sum(abs(rs) > 3)
n_big
which(abs(rs) > 3)
# Conclusion: the curved residual pattern and several large residuals (many at medv = 50, a capped value) show the model misses part of the structure.''', [("n_big", "n_big", 0)]),
N(5, 5, "Influential points", "Use Cook's distance (rule of thumb 4/n) to find influential homes, refit without them, and compare the coefficients. Write 3 sentences on whether to drop them.", LIB,
  '''# 1. cd <- cooks.distance(fit)
# 2. Count cd > 4 / n
# 3. Refit without them and compare coef()
# 4. Report (3 sentences as comments):
''',
  '''cd <- cooks.distance(fit)
cut <- 4 / nrow(Boston)
infl <- which(cd > cut)
length(infl)
fit_wo <- lm(medv ~ rm + lstat + ptratio, data = Boston[-infl, ])
round(rbind(all = coef(fit), without = coef(fit_wo)), 3)
# A few homes pull the fitted plane noticeably; the rm slope changes the most.
# They are real observations (for example, very expensive homes), not typing errors.
# Report both fits and keep the data unless there is a reason the points are wrong.''', [("n_infl", "length(infl)", 0)]),
]

B = [
N(6, 1, "Multicollinearity and VIF", "Check the VIF of a model with correlated predictors.", LIB, "",
  '''# === Complete example — read and run ===
fit_big <- lm(medv ~ rm + lstat + ptratio + tax + rad + nox, data = Boston)
v <- vif(fit_big)
round(v, 2)
round(cor(Boston$tax, Boston$rad), 3)      # tax and rad move together''', [("vif_tax", "car::vif(lm(medv ~ rm + lstat + ptratio + tax + rad + nox, data = Boston))['tax']", 2)]),
N(7, 2, "Dropping a collinear predictor", "Remove the predictor with the largest VIF and recompute the VIFs and adjusted R².", LIB,
  '''worst <- names(which.max(___))
fit_small <- update(fit_big, . ~ . - ___)          # use the name stored in worst
round(vif(fit_small), 2)
round(c(big = summary(fit_big)$adj.r.squared, small = summary(fit_small)$___), 4)''',
  '''worst <- names(which.max(v))
fit_small <- update(fit_big, as.formula(paste(". ~ . -", worst)))
round(vif(fit_small), 2)
round(c(big = summary(fit_big)$adj.r.squared, small = summary(fit_small)$adj.r.squared), 4)''', [("adj_small", "summary(fit_small)$adj.r.squared", 4)]),
N(8, 3, "Polynomial term", "medv vs lstat is curved. Compare a straight-line model with a quadratic one (lstat + I(lstat^2)) using adjusted R² and anova().", LIB,
  "# Write all your code here\n",
  '''m1 <- lm(medv ~ lstat, data = Boston)
m2 <- lm(medv ~ lstat + I(lstat^2), data = Boston)
round(c(linear = summary(m1)$adj.r.squared, quadratic = summary(m2)$adj.r.squared), 4)
anova(m1, m2)
plot(medv ~ lstat, data = Boston, col = "gray40")
o <- order(Boston$lstat); lines(Boston$lstat[o], fitted(m2)[o], col = "red", lwd = 2)''', [("adj_quad", "summary(lm(medv ~ lstat + I(lstat^2), data = Boston))$adj.r.squared", 4)]),
N(9, 4, "A categorical predictor", "Does being on the Charles River (chas = 1) add value after rm and lstat? Convert chas to a factor, fit the model and interpret the coefficient.", LIB,
  '''# 1. Boston$river <- factor(Boston$chas, labels = c("no", "yes"))
# 2. lm(medv ~ rm + lstat + river)
# 3. Coefficient and p-value of riveryes
# 4. Interpretation (comment):
''',
  '''Boston$river <- factor(Boston$chas, labels = c("no", "yes"))
fit_r <- lm(medv ~ rm + lstat + river, data = Boston)
round(summary(fit_r)$coefficients["riveryes", ], 4)
# Interpretation: river homes are worth about $4,000 more on average, holding rooms and lstat fixed.''', [("b_river", "coef(lm(medv ~ rm + lstat + factor(chas), data = Boston))[4]", 3)]),
N(10, 5, "Interaction", "Does the effect of rooms depend on lstat? Fit medv ~ rm * lstat, test the interaction, and compute the slope of rm at lstat = 5 and at lstat = 25. Write 3 sentences.", LIB,
  '''# 1. fit_i <- lm(medv ~ rm * lstat, data = Boston)
# 2. p-value of rm:lstat
# 3. Slope of rm = b_rm + b_int * lstat, at 5 and at 25
# 4. Report (3 sentences as comments):
''',
  '''fit_i <- lm(medv ~ rm * lstat, data = Boston)
b <- coef(fit_i)
signif(summary(fit_i)$coefficients["rm:lstat", 4], 3)
slope_rm <- function(l) unname(b["rm"] + b["rm:lstat"] * l)
round(c(at5 = slope_rm(5), at25 = slope_rm(25)), 3)
# The interaction is highly significant: the value of an extra room depends on the neighbourhood.
# In areas with few lower-status residents an extra room adds a lot of value.
# In areas with many lower-status residents (lstat = 25) the rm slope even turns negative.''', [("slope_at5", "slope_rm(5)", 3)]),
]

C = [
N(11, 1, "Working with dates", "Turn date strings into Date objects and extract useful predictors (made-up sales data).", "", "",
  '''# === Complete example — read and run ===
set.seed(11)
day <- seq(as.Date("2025-01-01"), as.Date("2025-12-31"), by = "day")
sales <- data.frame(date = day,
                    units = round(200 + 30 * sin(2 * pi * as.numeric(format(day, "%j")) / 365) +
                                  25 * (weekdays(day) %in% c("Saturday", "Sunday")) + rnorm(length(day), 0, 10)))
sales$month <- factor(format(sales$date, "%m"))
sales$weekend <- weekdays(sales$date) %in% c("Saturday", "Sunday")
head(sales, 3)
round(tapply(sales$units, sales$weekend, mean), 2)''', [("n_days", "nrow(sales)", 0)]),
N(12, 2, "Dates as predictors", "Regress units on weekend and month. How many extra units does a weekend day sell?", "",
  '''fit_d <- lm(units ~ ___ + ___, data = sales)
round(coef(fit_d)["weekendTRUE"], 2)
round(summary(fit_d)$___, 4)''',
  '''fit_d <- lm(units ~ weekend + month, data = sales)
round(coef(fit_d)["weekendTRUE"], 2)
round(summary(fit_d)$adj.r.squared, 4)''', [("b_weekend", "coef(fit_d)['weekendTRUE']", 2)]),
N(13, 3, "Days since a start date", "Create `t` = days since 2025-01-01 (as.numeric(date - start)) and test whether there is a linear trend after controlling for weekend.", "",
  "# Write all your code here\n",
  '''sales$t <- as.numeric(sales$date - as.Date("2025-01-01"))
fit_t <- lm(units ~ t + weekend, data = sales)
round(summary(fit_t)$coefficients["t", ], 4)''', [("b_t", "coef(lm(units ~ t + weekend, data = sales))['t']", 4)]),
N(14, 4, "Dummy coding by hand", "Recreate R's dummy variables for `cyl` in mtcars with model.matrix(), and show that lm() with the factor gives the same coefficients as lm() with the dummies.", "",
  '''# 1. model.matrix(~ factor(cyl), data = mtcars)
# 2. lm(mpg ~ factor(cyl)) vs lm(mpg ~ d6 + d8)
# 3. Which level is the baseline? (comment)
''',
  '''X <- model.matrix(~ factor(cyl), data = mtcars)
head(X, 3)
d6 <- X[, 2]; d8 <- X[, 3]
round(rbind(factor = coef(lm(mpg ~ factor(cyl), data = mtcars)), dummies = coef(lm(mpg ~ d6 + d8, data = mtcars))), 4)
# The baseline is 4 cylinders: each dummy is the difference from 4-cylinder cars.''', [("b8", "coef(lm(mpg ~ factor(cyl), data = mtcars))[3]", 4)]),
N(15, 5, "Changing the baseline", "Use relevel() to make 8 cylinders the baseline, refit, and explain how the coefficients changed while the fitted values stayed the same. Write 3 sentences.", "",
  '''# 1. mtcars$cyl_f <- relevel(factor(mtcars$cyl), ref = "8")
# 2. Refit lm(mpg ~ cyl_f)
# 3. Check: are the fitted values identical? all.equal()
# 4. Report (3 sentences as comments):
''',
  '''mtcars$cyl_f <- relevel(factor(mtcars$cyl), ref = "8")
m8 <- lm(mpg ~ cyl_f, data = mtcars)
m4 <- lm(mpg ~ factor(cyl), data = mtcars)
round(coef(m8), 4)
all.equal(unname(fitted(m8)), unname(fitted(m4)))
# The intercept is now the mean mpg of 8-cylinder cars.
# The other coefficients are differences from 8 cylinders, so their signs flip to positive.
# The model itself is the same: identical fitted values, residuals and R-squared.''', [("int8", "coef(m8)[1]", 4)]),
]

D = [
N(16, 1, "Train/test split and RMSE", "Evaluate a model on data it has not seen.", LIB, "",
  '''# === Complete example — read and run ===
set.seed(16)
idx <- sample(nrow(Boston), round(0.7 * nrow(Boston)))
train <- Boston[idx, ]; test <- Boston[-idx, ]
m <- lm(medv ~ rm + lstat + ptratio, data = train)
rmse <- function(obs, pred) sqrt(mean((obs - pred)^2))
round(c(train = rmse(train$medv, fitted(m)), test = rmse(test$medv, predict(m, test))), 3)''', [("rmse_test", "rmse(test$medv, predict(m, test))", 3)]),
N(17, 2, "Backward selection with step()", "Start from a model with all predictors and let step() remove variables by AIC.", LIB,
  '''full <- lm(medv ~ ., data = Boston[, setdiff(names(Boston), "river")])
back <- step(full, direction = "___", trace = 0)
formula(back)
length(coef(___)) - 1          # number of predictors kept''',
  '''full <- lm(medv ~ ., data = Boston[, setdiff(names(Boston), "river")])
back <- step(full, direction = "backward", trace = 0)
formula(back)
length(coef(back)) - 1          # number of predictors kept''', [("n_kept", "length(coef(back)) - 1", 0)]),
N(18, 3, "Forward and stepwise selection", "Run forward selection (scope = the full model) from the empty model, and both-direction stepwise selection. Do they choose the same predictors as backward selection?", LIB,
  "# Write all your code here\n",
  '''B2 <- Boston[, setdiff(names(Boston), "river")]
empty <- lm(medv ~ 1, data = B2)
fwd <- step(empty, scope = formula(full), direction = "forward", trace = 0)
both <- step(empty, scope = formula(full), direction = "both", trace = 0)
sel <- function(m) sort(names(coef(m))[-1])
identical(sel(fwd), sel(back)); identical(sel(both), sel(back))
sel(back)''', [("aic_back", "AIC(back)", 2)]),
N(19, 4, "Compare candidate models", "A realtor wants a simple but accurate model. Compare three models (rm + lstat; rm + lstat + ptratio; the backward-selection model) with adjusted R², AIC, BIC and test RMSE (same split as Q16).", LIB,
  '''# 1. Fit the three models on train
# 2. A table of adj. R-squared, AIC, BIC and test RMSE
# 3. Recommendation (comment): which model?
''',
  '''cands <- list(small = medv ~ rm + lstat, medium = medv ~ rm + lstat + ptratio, selected = formula(back))
tab <- t(sapply(cands, function(f) {
  m <- lm(f, data = train)
  c(adj_r2 = summary(m)$adj.r.squared, AIC = AIC(m), BIC = BIC(m), test_rmse = rmse(test$medv, predict(m, test)))
}))
round(tab, 3)
# Recommendation: the selected model predicts best; the medium model is a good simpler choice.''', [("rmse_medium", "rmse(test$medv, predict(lm(medv ~ rm + lstat + ptratio, data = train), test))", 3)]),
N(20, 5, "Cross-validation", "Estimate the prediction error of the medium model with 5-fold cross-validation (`set.seed(20)`) instead of a single split. Write a 4-sentence report.", LIB,
  '''# 1. folds <- sample(rep(1:5, length.out = nrow(Boston)))
# 2. For each fold: fit on the other folds, RMSE on this fold
# 3. Mean and SD of the 5 RMSEs
# 4. Report (4 sentences as comments):
''',
  '''set.seed(20)
folds <- sample(rep(1:5, length.out = nrow(Boston)))
cv_rmse <- sapply(1:5, function(k) {
  m <- lm(medv ~ rm + lstat + ptratio, data = Boston[folds != k, ])
  rmse(Boston$medv[folds == k], predict(m, Boston[folds == k, ]))
})
round(cv_rmse, 3)
round(c(mean = mean(cv_rmse), sd = sd(cv_rmse)), 3)
# Question: how well does the 3-predictor model predict new homes?
# Method: 5-fold cross-validation uses every home once as test data.
# Result: the mean RMSE above is the typical prediction error in $1000s.
# The fold-to-fold spread shows that one train/test split alone can be misleading.''', [("cv_mean", "mean(cv_rmse)", 3)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M5 QUICK REFERENCE (multiple regression)        ║
║  lm(y ~ x1 + x2 + x3)  summary()  adj.r.squared      ║
║  standardized: lm(scale(y) ~ scale(x1) + ...)        ║
║  rstandard(fit)  cooks.distance(fit) > 4/n           ║
║  car::vif(fit) > 5-10 = collinearity                 ║
║  poly: y ~ x + I(x^2)    interaction: y ~ x1 * x2    ║
║  factor(x)  relevel(f, ref)  model.matrix(~ f)       ║
║  dates: as.Date()  format(d, '%m')  weekdays(d)      ║
║  step(fit, direction = 'backward'/'forward'/'both')  ║
║  AIC() BIC()  RMSE = sqrt(mean((obs - pred)^2))      ║
║  k-fold CV: sample(rep(1:k, length.out = n))         ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/m5_ch1.html (650 M5 multiple regression, Ch.1-12)"
MOD = dict(key="n650_m5", title="650 M5 — Multiple Regression: R Coding Practice (20 Questions)",
           file="650_m5_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/M5", wd=R650 + "/650 - Data Visualization/M5",
           data_note="Needs MASS (comes with R) and car (`install.packages(\"car\")` once). Data: `Boston` (MASS), `mtcars` and a simulated sales data set.",
           header_link=LINK, site_rmd=SITE,
           topics=[("Fitting & Diagnosing a Multiple Regression", A), ("Collinearity, Polynomials, Categories & Interaction", B),
                   ("Dates & Dummy Variables", C), ("Variable Selection & Evaluation", D)], card=CARD)
MOD["questions"] = A + B + C + D
