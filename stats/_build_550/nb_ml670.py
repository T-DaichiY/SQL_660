"""670 ML statistics review: explore & prepare, split & regression, classification, overfitting/CV/uncertainty (base R, simulated + built-in data)."""
from nb_build import N
from practice_gen import SRC

STATS = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern/660 - SQL/Lesson_website/stats"
SKEW = 'skew <- function(x) { x <- x[!is.na(x)]; mean((x - mean(x))^3) / mean((x - mean(x))^2)^1.5 }'
APT = '''set.seed(670)
n <- 400
apt <- data.frame(area  = round(runif(n, 25, 120)),
                  rooms = sample(1:4, n, replace = TRUE, prob = c(.2, .4, .3, .1)),
                  age   = round(runif(n, 0, 50)))
apt$price <- round(40 + 2.2 * apt$area + 12 * apt$rooms - 0.8 * apt$age + rnorm(n, 0, 25), 1)  # 1000 USD
set.seed(1)
idx   <- sample(n, size = 0.8 * n)
train <- apt[idx, ]
test  <- apt[-idx, ]
rmse  <- function(y, p) sqrt(mean((y - p)^2))'''
TI = '''d  <- as.data.frame(Titanic)                       # R's built-in Titanic table (2,201 people)
ti <- d[rep(seq_len(nrow(d)), d$Freq), c("Class", "Sex", "Age", "Survived")]
rownames(ti) <- NULL
ti$Survived <- as.integer(ti$Survived == "Yes")
set.seed(1)
idx <- sample(nrow(ti), size = 0.8 * nrow(ti))
tr  <- ti[idx, ]
te  <- ti[-idx, ]'''
SINE = '''set.seed(15)
x <- runif(60, 0, 10); y <- sin(x) + rnorm(60, 0, 0.5)
dat <- data.frame(x, y)
train <- dat[1:25, ]; test <- dat[26:60, ]
rmse <- function(a, b) sqrt(mean((a - b)^2))'''

A = [
N(1, 1, "Summary and skewness", "Describe the ozone levels in `airquality`: compare mean and median, then measure skewness.", "", "",
  '''# === Complete example — read and run ===
x <- airquality$Ozone
summary(x)                                  # mean (42.1) is larger than the median (31.5)
sd(x, na.rm = TRUE)
''' + SKEW + '''
skew_oz <- skew(x)
round(skew_oz, 2)                           # > 1: strongly right-skewed''', [("skew_oz", "skew_oz", 2)]),
N(2, 2, "Outliers with the 1.5 x IQR rule", "Find the upper fence for wind speed in `airquality` and count the days above it.", "",
  '''w <- airquality$Wind
q <- quantile(w, c(___, ___))
iqr <- unname(diff(q))
upper <- unname(q[2]) + ___ * iqr
n_out <- sum(w > ___)
round(c(upper = upper, n_out = n_out), 2)''',
  '''w <- airquality$Wind
q <- quantile(w, c(.25, .75))
iqr <- unname(diff(q))
upper <- unname(q[2]) + 1.5 * iqr
n_out <- sum(w > upper)
round(c(upper = upper, n_out = n_out), 2)''', [("upper", "upper", 2), ("n_out", "n_out", 0)]),
N(3, 3, "Log transform", "Show that a log transform reduces the skewness of the ozone levels. Report the skewness before and after (2 decimals).", "",
  "# Write all your code here (define the skew() helper yourself)\n",
  SKEW + '''
oz <- airquality$Ozone
skew_raw <- skew(oz)
skew_log <- skew(log(oz))
round(c(before = skew_raw, after = skew_log), 2)
par(mfrow = c(1, 2)); hist(oz, main = "raw"); hist(log(oz), main = "log")''', [("skew_log", "skew_log", 2)]),
N(4, 4, "Standardizing without leakage", "Standardize `area` for the apartment data. Compute the mean and SD on the TRAINING rows only, apply them to both train and test, and report the mean and SD of the standardized test column.", APT,
  '''# 1. mean and SD of train$area
# 2. z-scores for the train rows and the test rows (using the train mean/SD)
# 3. Mean and SD of the standardized TEST column (3 decimals)
# 4. Why is the test mean not exactly 0? (comment)
''',
  '''mu <- mean(train$area); s <- sd(train$area)
z_train <- (train$area - mu) / s
z_test  <- (test$area  - mu) / s
test_mean_z <- mean(z_test)
test_sd_z <- sd(z_test)
round(c(train_mean = mean(z_train), train_sd = sd(z_train), test_mean = test_mean_z, test_sd = test_sd_z), 3)
# The train column is exactly mean 0 / SD 1. The test column uses the TRAIN statistics, so it is only close to 0 and 1.
# That is correct: the test set must not influence the scaling (no data leakage).''', [("test_mean_z", "test_mean_z", 3), ("test_sd_z", "test_sd_z", 3)]),
N(5, 5, "Dropping vs imputing missing values", "In `airquality`, compare two ways of handling missing Ozone: drop the rows, or fill with the median. Report the rows kept, the SD of Ozone, and the correlation between Ozone and Temp for each method. Write 3 sentences on what imputation does to the relationship.", "",
  '''# 1. NA count per column
# 2. Method 1: drop rows with an NA in Ozone (rows kept, SD, cor with Temp)
# 3. Method 2: median imputation (SD, cor with Temp)
# 4. Report (3 sentences as comments):
''',
  '''colSums(is.na(airquality))
aq <- airquality
drop <- aq[!is.na(aq$Ozone), ]
rows_kept <- nrow(drop)
cor_drop <- cor(drop$Ozone, drop$Temp)
aq$Ozone_imp <- ifelse(is.na(aq$Ozone), median(aq$Ozone, na.rm = TRUE), aq$Ozone)
sd_imp <- sd(aq$Ozone_imp)
cor_imp <- cor(aq$Ozone_imp, aq$Temp)
round(c(rows_kept = rows_kept, sd_drop = sd(drop$Ozone), sd_imp = sd_imp, cor_drop = cor_drop, cor_imp = cor_imp), 3)
# Median imputation keeps all 153 rows and keeps the mean almost unchanged.
# But it shrinks the SD (29 vs 33) and weakens the Ozone-Temp correlation (0.70 -> 0.60),
# because the 37 filled values ignore Temp. Imputation is convenient, but it slightly distorts relationships.''',
  [("rows_kept", "rows_kept", 0), ("sd_imp", "sd_imp", 2), ("cor_drop", "cor_drop", 3), ("cor_imp", "cor_imp", 3)]),
]

B = [
N(6, 1, "Split and fit a linear model", "Split the apartment data 80/20 and fit price ~ area + rooms + age on the training rows.", APT, "",
  '''# === Complete example — read and run ===
c(train = nrow(train), test = nrow(test))
fit <- lm(price ~ area + rooms + age, data = train)
coefs <- coef(fit)
round(coefs, 2)                             # +1 m2 of area adds about 2.2 (1000 USD), others fixed
coef_area <- coefs[["area"]]''', [("coef_area", "coef_area", 2)]),
N(7, 2, "RMSE, MAE and R² on the test set", "Evaluate `fit` on the test rows (not the training rows).", APT + "\nfit <- lm(price ~ area + rooms + age, data = train)",
  '''pred <- predict(fit, newdata = ___)
res  <- test$price - ___
rmse_test <- sqrt(mean(___^2))
mae_test  <- mean(abs(res))
r2_test   <- 1 - sum(res^2) / sum((test$price - mean(___))^2)
round(c(RMSE = rmse_test, MAE = mae_test, R2 = r2_test), 3)''',
  '''pred <- predict(fit, newdata = test)
res  <- test$price - pred
rmse_test <- sqrt(mean(res^2))
mae_test  <- mean(abs(res))
r2_test   <- 1 - sum(res^2) / sum((test$price - mean(test$price))^2)
round(c(RMSE = rmse_test, MAE = mae_test, R2 = r2_test), 3)''', [("rmse_test", "rmse_test", 2), ("mae_test", "mae_test", 2), ("r2_test", "r2_test", 3)]),
N(8, 3, "Beat the baseline", "A baseline always predicts the TRAINING mean price. Compute its test RMSE, compare it with the model's test RMSE, and report the percentage improvement (1 decimal).", APT + "\nfit <- lm(price ~ area + rooms + age, data = train)",
  "# Write all your code here\n",
  '''base_rmse  <- rmse(test$price, mean(train$price))
model_rmse <- rmse(test$price, predict(fit, test))
improve_pct <- 100 * (base_rmse - model_rmse) / base_rmse
round(c(baseline = base_rmse, model = model_rmse, improvement_pct = improve_pct), 1)''', [("improve_pct", "improve_pct", 1)]),
N(9, 4, "Residual check", "Plot the test residuals against the fitted values and find the apartment with the largest absolute residual. Report that residual and the mean of the TRAINING residuals.", APT + "\nfit <- lm(price ~ area + rooms + age, data = train)",
  '''# 1. Residuals on the test set and fitted (predicted) values
# 2. Residual-vs-fitted plot with a horizontal line at 0
# 3. The largest absolute test residual and its row in `test`
# 4. Mean of the training residuals (3 decimals) and why it is ~0 (comment)
''',
  '''pred <- predict(fit, test)
res <- test$price - pred
plot(pred, res, pch = 16, xlab = "Predicted", ylab = "Residual"); abline(h = 0, col = "red", lty = 2)
max_abs <- max(abs(res))
test[which.max(abs(res)), ]
mean_res_train <- mean(resid(fit))
round(c(max_abs = max_abs, mean_res_train = mean_res_train), 3)
# Least squares with an intercept forces the training residuals to average exactly 0.
# The test residuals have no such guarantee; a pattern in the plot would show a missed relationship.''', [("max_abs", "max_abs", 1), ("mean_res_train", "mean_res_train", 3)]),
N(10, 5, "Which feature matters most?", "Standardize the training data, fit the model, and rank the features by the size of their standardized coefficients. Then compare the test RMSE of an area-only model with the full model. Write 3 sentences on what you learn.", APT,
  '''# 1. Standardized training data (scale) and the model fit on it
# 2. Standardized coefficients, ranked by absolute size
# 3. Test RMSE: price ~ area only vs price ~ area + rooms + age
# 4. Report (3 sentences as comments):
''',
  '''train_s <- as.data.frame(scale(train))
fit_s <- lm(price ~ area + rooms + age, data = train_s)
coef_std <- coef(fit_s)[-1]
sort(abs(round(coef_std, 2)), decreasing = TRUE)
coef_area_std <- coef_std[["area"]]
rmse_area <- rmse(test$price, predict(lm(price ~ area, train), test))
rmse_all  <- rmse(test$price, predict(lm(price ~ area + rooms + age, train), test))
round(c(coef_area_std = coef_area_std, rmse_area_only = rmse_area, rmse_all = rmse_all), 2)
# Area has by far the largest standardized coefficient (0.91), so it matters most.
# Rooms and age add useful information: the test RMSE drops from about 33 to 28.5.
# Standardizing lets us compare features measured in different units.''',
  [("coef_area_std", "coef_area_std", 2), ("rmse_area", "rmse_area", 1), ("rmse_all", "rmse_all", 1)]),
]

C = [
N(11, 1, "Logistic regression and odds ratios", "Predict Titanic survival from Class, Sex and Age with `glm()` and read the odds ratios.", TI, "",
  '''# === Complete example — read and run ===
m <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)
or <- exp(coef(m))                          # odds ratios
round(or, 2)
or_female <- or[["SexFemale"]]              # women: odds of survival about 11 times higher
round(or_female, 2)''', [("or_female", "or_female", 2)]),
N(12, 2, "Confusion matrix and accuracy", "Turn the predicted probabilities into classes with a 0.5 threshold and build the confusion matrix.", TI + "\nm <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)",
  '''p    <- predict(m, newdata = ___, type = "response")
pred <- as.integer(p >= ___)
tab  <- table(Truth = te$Survived, Predicted = ___)
tab
accuracy <- sum(diag(tab)) / sum(___)
round(accuracy, 3)''',
  '''p    <- predict(m, newdata = te, type = "response")
pred <- as.integer(p >= 0.5)
tab  <- table(Truth = te$Survived, Predicted = pred)
tab
accuracy <- sum(diag(tab)) / sum(tab)
round(accuracy, 3)''', [("accuracy", "accuracy", 3)]),
N(13, 3, "Precision, recall and F1", "From the predictions at threshold 0.5, compute precision, recall and F1 (3 decimals).", TI + "\nm <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)\np <- predict(m, te, type = 'response')\npred <- as.integer(p >= 0.5)",
  "# Write all your code here\n",
  '''TP <- sum(pred == 1 & te$Survived == 1); FP <- sum(pred == 1 & te$Survived == 0)
FN <- sum(pred == 0 & te$Survived == 1)
precision <- TP / (TP + FP)
recall    <- TP / (TP + FN)
f1 <- 2 * precision * recall / (precision + recall)
round(c(precision = precision, recall = recall, F1 = f1), 3)''', [("precision", "precision", 3), ("recall", "recall", 3)]),
N(14, 4, "Choosing a threshold", "A rescue team wants to find at least 60% of the survivors (recall >= 0.6). Compute precision and recall for thresholds 0.3, 0.5 and 0.7, and choose the best threshold for the team.", TI + "\nm <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)\np <- predict(m, te, type = 'response')",
  '''# 1. A function that returns precision and recall for one threshold
# 2. Apply it to 0.3, 0.5, 0.7 (3 decimals)
# 3. Which threshold satisfies recall >= 0.6 with the highest precision? (comment)
''',
  '''score <- function(th) {
  pr <- as.integer(p >= th)
  TP <- sum(pr == 1 & te$Survived == 1); FP <- sum(pr == 1 & te$Survived == 0); FN <- sum(pr == 0 & te$Survived == 1)
  c(precision = TP / (TP + FP), recall = TP / (TP + FN))
}
res <- t(sapply(c(0.3, 0.5, 0.7), score)); rownames(res) <- c(0.3, 0.5, 0.7)
round(res, 3)
recall_03 <- res["0.3", "recall"]; precision_07 <- res["0.7", "precision"]
# Only threshold 0.3 reaches recall >= 0.6 (0.639), with precision 0.686.
# Raising the threshold gives higher precision but misses more survivors.''', [("recall_03", "recall_03", 3), ("precision_07", "precision_07", 3)]),
N(15, 5, "ROC and AUC: is the model better than Sex alone?", "Compute the AUC with the rank formula for (a) the full model and (b) a model using only Sex. Draw both ROC curves. Write 3 sentences comparing them.", TI,
  '''# 1. Fit both models on tr; predict probabilities on te
# 2. An auc(y, score) function using ranks
# 3. AUC for each model (3 decimals)
# 4. ROC curves (both models, one plot, diagonal line)
# 5. Report (3 sentences as comments):
''',
  '''m_full <- glm(Survived ~ Class + Sex + Age, data = tr, family = binomial)
m_sex  <- glm(Survived ~ Sex, data = tr, family = binomial)
p_full <- predict(m_full, te, type = "response"); p_sex <- predict(m_sex, te, type = "response")
auc <- function(y, s) { r <- rank(s); n1 <- sum(y == 1); n0 <- sum(y == 0); (sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0) }
auc_full <- auc(te$Survived, p_full); auc_sex <- auc(te$Survived, p_sex)
round(c(full = auc_full, sex_only = auc_sex), 3)
roc <- function(p) { ths <- sort(unique(c(0, p, 1)), decreasing = TRUE)
  t(sapply(ths, function(th) c(mean(p[te$Survived == 0] >= th), mean(p[te$Survived == 1] >= th)))) }
r1 <- roc(p_full); r2 <- roc(p_sex)
plot(r1, type = "s", col = "#4471B8", lwd = 2, xlab = "False positive rate", ylab = "True positive rate")
lines(r2, type = "s", col = "#B84848", lwd = 2); abline(0, 1, lty = 2)
# The full model has a higher AUC (0.78 vs 0.73), so it ranks survivors above non-survivors more often.
# Sex alone already beats random guessing (0.5) by a wide margin.
# Class and Age add a modest but real improvement.''', [("auc_full", "auc_full", 3), ("auc_sex", "auc_sex", 3)]),
]

D = [
N(16, 1, "Underfitting and overfitting", "Fit polynomials of degree 1 and 10 to the noisy sine data and compare train and test RMSE.", SINE, "",
  '''# === Complete example — read and run ===
fit1  <- lm(y ~ poly(x, 1),  data = train)
fit10 <- lm(y ~ poly(x, 10), data = train)
tab <- rbind(degree1  = c(train = rmse(train$y, predict(fit1, train)),  test = rmse(test$y, predict(fit1, test))),
             degree10 = c(train = rmse(train$y, predict(fit10, train)), test = rmse(test$y, predict(fit10, test))))
round(tab, 3)
test_rmse_10 <- tab["degree10", "test"]''', [("test_rmse_10", "test_rmse_10", 3)]),
N(17, 2, "The U-shaped test error", "Loop over polynomial degrees 1 to 8, compute train and test RMSE, and find the degree with the lowest test RMSE.", SINE,
  '''deg <- 1:___
err <- t(sapply(deg, function(d) {
  f <- lm(y ~ poly(x, ___), data = train)
  c(train = rmse(train$y, predict(f, ___)), test = rmse(test$y, predict(f, test)))
}))
round(cbind(degree = deg, err), 3)
best_deg_test <- deg[which.min(err[, "___"])]
best_deg_test''',
  '''deg <- 1:8
err <- t(sapply(deg, function(d) {
  f <- lm(y ~ poly(x, d), data = train)
  c(train = rmse(train$y, predict(f, train)), test = rmse(test$y, predict(f, test)))
}))
round(cbind(degree = deg, err), 3)
best_deg_test <- deg[which.min(err[, "test"])]
best_deg_test''', [("best_deg_test", "best_deg_test", 0)]),
N(18, 3, "5-fold cross-validation", "Choose the polynomial degree (1 to 8) by 5-fold cross-validation on the TRAINING data only (`set.seed(2)` before creating the folds). Report the best degree and its CV RMSE (3 decimals).", SINE,
  "# Write all your code here\n",
  '''set.seed(2)
folds <- sample(rep(1:5, length.out = nrow(train)))
cv_rmse <- function(d) mean(sapply(1:5, function(k) {
  f <- lm(y ~ poly(x, d), data = train[folds != k, ])
  rmse(train$y[folds == k], predict(f, train[folds == k, ]))
}))
cv <- sapply(1:8, cv_rmse)
round(cv, 3)
best_deg_cv <- which.min(cv)
cv_min <- min(cv)
c(best_deg_cv = best_deg_cv, cv_min = round(cv_min, 3))''', [("best_deg_cv", "best_deg_cv", 0), ("cv_min", "cv_min", 3)]),
N(19, 4, "Ridge: shrinking the coefficients", "Standardize the apartment training data and fit ridge regression with lambda = 0, 100 and 1000 (`MASS::lm.ridge`). How does the coefficient of `area` change? Report it for lambda = 100 and lambda = 1000.", APT,
  '''# 1. Standardized training data: train_s
# 2. MASS::lm.ridge(price ~ area + rooms + age, data = train_s, lambda = c(0, 100, 1000))
# 3. The coefficient matrix (rows = lambda) rounded to 3 decimals
# 4. The area coefficient at lambda = 100 and 1000
# 5. What happens as lambda grows? (comment)
''',
  '''train_s <- as.data.frame(scale(train))
r <- MASS::lm.ridge(price ~ area + rooms + age, data = train_s, lambda = c(0, 100, 1000))
cf <- coef(r)
round(cf, 3)
area_100 <- cf[2, "area"]; area_1000 <- cf[3, "area"]
round(c(area_100 = area_100, area_1000 = area_1000), 3)
# As lambda grows, every coefficient is pulled toward 0 (area: 0.91 -> 0.69 -> 0.22).
# A stronger penalty lowers the model's variance but adds bias; choose lambda by cross-validation.''', [("area_100", "area_100", 3), ("area_1000", "area_1000", 3)]),
N(20, 5, "How uncertain is the test RMSE?", "Bootstrap the test rows of the apartment model (1,000 resamples, `set.seed(20)`) to get a 95% interval for the RMSE, and compare it with the t-based interval for the MSE (square-rooted). Write 3 sentences on what the interval tells you.", APT + "\nfit <- lm(price ~ area + rooms + age, data = train)",
  '''# 1. Squared errors on the test set
# 2. Bootstrap: resample the 80 squared errors 1,000 times, RMSE of each resample
# 3. 2.5% and 97.5% quantiles (1 decimal)
# 4. t-based 95% CI for the mean squared error, then sqrt
# 5. Report (3 sentences as comments):
''',
  '''sq <- (test$price - predict(fit, test))^2
set.seed(20)
boot <- replicate(1000, sqrt(mean(sample(sq, replace = TRUE))))
ci_boot <- quantile(boot, c(.025, .975))
ci_t <- sqrt(t.test(sq)$conf.int)
boot_lo <- ci_boot[[1]]; boot_hi <- ci_boot[[2]]; t_lo <- ci_t[1]; t_hi <- ci_t[2]
round(c(RMSE = sqrt(mean(sq)), boot_lo = boot_lo, boot_hi = boot_hi, t_lo = t_lo, t_hi = t_hi), 1)
# The test RMSE is 28.5, but with 80 test rows the plausible range is roughly 24 to 32.
# Both methods agree closely, so the width comes from the small test set, not from the method.
# A difference between two models smaller than this width should not be treated as real.''',
  [("boot_lo", "boot_lo", 1), ("boot_hi", "boot_hi", 1), ("t_lo", "t_lo", 1), ("t_hi", "t_hi", 1)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  670 ML STATS REVIEW — QUICK REFERENCE               ║
║  summary(x)  sd(x)  quantile(x, c(.25,.75))          ║
║  IQR fence: Q1 - 1.5*IQR , Q3 + 1.5*IQR              ║
║  z = (x - mean_train) / sd_train     scale(x)        ║
║  idx <- sample(n, 0.8*n); train <- d[idx,]           ║
║  lm(y ~ ., train)   predict(fit, newdata = test)     ║
║  RMSE = sqrt(mean((y - p)^2))  MAE = mean(abs(y - p))║
║  R2 = 1 - sum(res^2) / sum((y - mean(y))^2)          ║
║  glm(y ~ ., family = binomial)   exp(coef(m))        ║
║  precision = TP/(TP+FP)   recall = TP/(TP+FN)        ║
║  AUC via rank():  (sum(r[y==1]) - n1(n1+1)/2)/(n1*n0)║
║  k-fold CV: folds <- sample(rep(1:k, length.out = n))║
║  ridge: MASS::lm.ridge(f, data, lambda = ...)        ║
║  bootstrap: replicate(B, stat(sample(x, replace=T))) ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/stats/ml_explore.html (670 ML 統計復習, 6 lessons)"
MOD = dict(key="ml670", title="670 ML Statistics Review — Explore, Split, Regression, Classification, Overfitting & Uncertainty: R Coding Practice (20 Questions)",
           file="ml670_practice_v1.Rmd", folder=SRC + "/670 ML Review", wd=SRC + "/Module 3",
           data_note="No data files are needed: every data set is simulated or built into R (airquality, Titanic).",
           header_link=LINK, site_rmd=[STATS + "/rmd"],
           topics=[("Explore & Prepare Data", A), ("Split & Regression", B),
                   ("Classification & Metrics", C), ("Overfitting, Cross-Validation & Uncertainty", D)], card=CARD)
MOD["questions"] = A + B + C + D
