"""650 M1: ggplot2 (R4DS Ch.1-2 style) with the mpg and diamonds data from ggplot2."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]
LIB = "library(ggplot2)"

A = [
N(1, 1, "Your first ggplot", "Plot engine size (displ) against highway mpg (hwy) for the `mpg` data.", LIB, "",
  '''# === Complete example — read and run ===
p <- ggplot(data = mpg, mapping = aes(x = displ, y = hwy)) +
  geom_point()
p
nrow(mpg)          # each point is one car model''', [("n", "nrow(mpg)", 0)]),
N(2, 2, "Map a third variable to colour", "Colour the points by `class`, and add axis labels.", LIB,
  '''ggplot(mpg, aes(x = displ, y = hwy, ___ = class)) +
  geom____() +
  labs(x = "Engine displacement (L)", y = "Highway mpg", ___ = "Car class")''',
  '''ggplot(mpg, aes(x = displ, y = hwy, colour = class)) +
  geom_point() +
  labs(x = "Engine displacement (L)", y = "Highway mpg", colour = "Car class")''', [("n_class", "length(unique(mpg$class))", 0)]),
N(3, 3, "Aesthetics vs. settings", "Make two plots of hwy vs displ: (a) all points blue and size 2 (a setting, outside aes()); (b) point size mapped to cyl (inside aes()). Explain the difference in a comment.", LIB,
  "# Write all your code here\n",
  '''ggplot(mpg, aes(displ, hwy)) + geom_point(colour = "blue", size = 2)     # setting
ggplot(mpg, aes(displ, hwy, size = cyl)) + geom_point(alpha = 0.5)      # mapping
# Inside aes() a variable controls the look; outside aes() one fixed value is used for every point.''', []),
N(4, 4, "Exploring fuel economy", "A car magazine wants to show that bigger engines use more fuel. Make a scatterplot of hwy vs displ with a smooth line, and compute the correlation and the mean hwy of cars with displ > 5.", LIB,
  '''# 1. Scatterplot + geom_smooth(method = "lm")
# 2. cor(mpg$displ, mpg$hwy)
# 3. Mean hwy for displ > 5
# 4. Headline for the magazine (comment):
''',
  '''ggplot(mpg, aes(displ, hwy)) + geom_point() + geom_smooth(method = "lm", formula = y ~ x)
r <- cor(mpg$displ, mpg$hwy)
round(r, 3)
round(mean(mpg$hwy[mpg$displ > 5]), 2)
# Headline: bigger engines, fewer miles - a strong negative relationship.''', [("r", "r", 3)]),
N(5, 5, "Why are some big engines efficient?", "In the hwy vs displ plot, a few cars with large engines have high hwy. Find them (displ > 5, hwy > 22), plot them in red on top of the others, and explain with the `class` variable. Write 3 sentences.", LIB,
  '''# 1. outliers <- mpg[mpg$displ > 5 & mpg$hwy > 22, ]
# 2. Their class and model
# 3. Plot all cars + geom_point(data = outliers, colour = "red", size = 3)
# 4. Report (3 sentences as comments):
''',
  '''outliers <- mpg[mpg$displ > 5 & mpg$hwy > 22, ]
outliers[, c("manufacturer", "model", "displ", "hwy", "class")]
ggplot(mpg, aes(displ, hwy)) + geom_point() +
  geom_point(data = outliers, colour = "red", size = 3)
# Five of the six unusual cars are two-seater Corvettes (the sixth is a midsize car).
# They have big engines but are light, so they still get good highway mileage.
# A third variable (class) explains the pattern that x and y alone cannot.''', [("n_out", "nrow(outliers)", 0)]),
]

B = [
N(6, 1, "Bar chart of a categorical variable", "Count cars by class.", LIB, "",
  '''# === Complete example — read and run ===
ggplot(mpg, aes(x = class)) + geom_bar()
counts <- table(mpg$class)
counts
ggplot(mpg, aes(x = factor(class, levels = names(sort(counts, decreasing = TRUE))))) +
  geom_bar() + labs(x = "class")                         # ordered by count''', [("n_suv", "sum(mpg$class == 'suv')", 0)]),
N(7, 2, "Histogram and binwidth", "Draw a histogram of `hwy` with binwidth 2, then a density plot.", LIB,
  '''ggplot(mpg, aes(x = ___)) + geom_histogram(binwidth = ___)
ggplot(mpg, aes(x = hwy)) + geom____()''',
  '''ggplot(mpg, aes(x = hwy)) + geom_histogram(binwidth = 2)
ggplot(mpg, aes(x = hwy)) + geom_density()''', [("mean_hwy", "mean(mpg$hwy)", 2)]),
N(8, 3, "Diamonds: price distribution", "Use `diamonds`. Plot a histogram of price (binwidth 500), describe the shape, and compute the mean and median price.", LIB,
  "# Write all your code here\n",
  '''ggplot(diamonds, aes(price)) + geom_histogram(binwidth = 500)
round(c(mean = mean(diamonds$price), median = median(diamonds$price)), 1)
# Strongly right-skewed: mean > median.''', [("median_price", "median(diamonds$price)", 1)]),
N(9, 4, "Comparing cut quality", "A jeweller asks how the diamond `cut` is distributed and whether better cuts are more expensive. Make a bar chart of cut and a boxplot of price by cut; report the median price per cut.", LIB,
  '''# 1. Bar chart of cut
# 2. Boxplot of price by cut
# 3. Median price per cut (tapply)
# 4. Answer for the jeweller (comment):
''',
  '''ggplot(diamonds, aes(cut)) + geom_bar()
ggplot(diamonds, aes(cut, price)) + geom_boxplot()
med <- tapply(diamonds$price, diamonds$cut, median)
med
# Surprisingly, Ideal diamonds have the LOWEST median price: they tend to be smaller (carat).''', [("med_ideal", "median(diamonds$price[diamonds$cut == 'Ideal'])", 1)]),
N(10, 5, "Stacked vs. dodged bars", "Show the count of cars by `class` and `drv` three ways: stacked, `position = 'dodge'` and `position = 'fill'`. Which chart answers 'what share of each class is 4-wheel drive?' Compute that share for SUVs. Write 3 sentences.", LIB,
  '''# 1. Stacked bar: aes(class, fill = drv)
# 2. position = "dodge"
# 3. position = "fill"
# 4. Share of 4wd among SUVs
# 5. Report (3 sentences as comments):
''',
  '''ggplot(mpg, aes(class, fill = drv)) + geom_bar()
ggplot(mpg, aes(class, fill = drv)) + geom_bar(position = "dodge")
ggplot(mpg, aes(class, fill = drv)) + geom_bar(position = "fill") + labs(y = "proportion")
share_4wd_suv <- mean(mpg$drv[mpg$class == "suv"] == "4")
round(share_4wd_suv, 3)
# Stacked bars show totals; dodged bars compare counts side by side.
# position = "fill" rescales every bar to 1, so it answers questions about shares.
# Most SUVs in the data are four-wheel drive.''', [("share", "share_4wd_suv", 3)]),
]

C = [
N(11, 1, "Smooth lines and groups", "Add a separate smoothed line for each drive type.", LIB, "",
  '''# === Complete example — read and run ===
ggplot(mpg, aes(displ, hwy, colour = drv)) +
  geom_point() +
  geom_smooth(method = "loess", formula = y ~ x, se = FALSE)
round(tapply(mpg$hwy, mpg$drv, mean), 2)''', [("hwy_f", "mean(mpg$hwy[mpg$drv == 'f'])", 2)]),
N(12, 2, "Facets", "Split the hwy vs displ scatterplot into one panel per `class`, and then a grid of drv × cyl.", LIB,
  '''ggplot(mpg, aes(displ, hwy)) + geom_point() + facet_wrap(~ ___)
ggplot(mpg, aes(displ, hwy)) + geom_point() + facet_grid(___ ~ ___)''',
  '''ggplot(mpg, aes(displ, hwy)) + geom_point() + facet_wrap(~ class)
ggplot(mpg, aes(displ, hwy)) + geom_point() + facet_grid(drv ~ cyl)''', [("n_panels", "length(unique(mpg$class))", 0)]),
N(13, 3, "Boxplots of hwy by class", "Draw boxplots of hwy for each class, ordered by median hwy (use `reorder()`), flipped horizontally. Which class has the highest median?", LIB,
  "# Write all your code here\n",
  '''ggplot(mpg, aes(x = reorder(class, hwy, FUN = median), y = hwy)) +
  geom_boxplot() + coord_flip() + labs(x = "class")
meds <- tapply(mpg$hwy, mpg$class, median)
names(which.max(meds)); max(meds)''', [("max_median", "max(tapply(mpg$hwy, mpg$class, median))", 1)]),
N(14, 4, "Carat, price and colour", "For `diamonds`, plot price against carat with transparency (alpha = 0.1) coloured by `color`, add a log10 scale on both axes, and compute the correlation of log10(carat) and log10(price).", LIB,
  '''# 1. Scatterplot with alpha = 0.1, colour = color
# 2. scale_x_log10() + scale_y_log10()
# 3. Correlation on the log scale
# 4. Conclusion (comment):
''',
  '''ggplot(diamonds, aes(carat, price, colour = color)) +
  geom_point(alpha = 0.1) + scale_x_log10() + scale_y_log10()
r_log <- cor(log10(diamonds$carat), log10(diamonds$price))
round(r_log, 3)
# On the log scale the relationship is almost a straight line: carat is the main driver of price.''', [("r_log", "r_log", 3)]),
N(15, 5, "Overplotting", "The `mpg` data have many identical (displ, hwy) points. Compare geom_point() with geom_jitter(width = 0.2, height = 0.2) (`set.seed(15)`) and geom_count(). How many rows share a (displ, hwy) pair with another row? Write 3 sentences.", LIB,
  '''# 1. geom_point() vs geom_jitter() vs geom_count()
# 2. Number of rows whose (displ, hwy) pair appears more than once
# 3. Report (3 sentences as comments):
''',
  '''ggplot(mpg, aes(displ, hwy)) + geom_point()
set.seed(15)
ggplot(mpg, aes(displ, hwy)) + geom_jitter(width = 0.2, height = 0.2)
ggplot(mpg, aes(displ, hwy)) + geom_count()
key <- paste(mpg$displ, mpg$hwy)
n_shared <- sum(key %in% key[duplicated(key)])
n_shared
# Values are rounded, so many cars sit exactly on top of each other.
# geom_point() hides them; jitter adds small random noise so every car becomes visible.
# geom_count() keeps the exact positions and shows how many cars are at each point.''', [("n_shared", "n_shared", 0)]),
]

D = [
N(16, 1, "Labels, themes and saving", "Add a title, subtitle and caption, change the theme and save the plot with ggsave().", LIB, "",
  '''# === Complete example — read and run ===
p <- ggplot(mpg, aes(displ, hwy, colour = class)) + geom_point() +
  labs(title = "Fuel efficiency generally decreases with engine size",
       subtitle = "Two-seaters are an exception because they are light",
       caption = "Data: ggplot2::mpg", x = "Engine displacement (L)", y = "Highway mpg") +
  theme_minimal()
p
out <- file.path(tempdir(), "mpg_plot.png")
ggsave(out, p, width = 7, height = 4, dpi = 150)
file.exists(out)''', []),
N(17, 2, "Fixing common errors", "Each line below has a bug. Fix them so every plot runs.", LIB,
  '''# a) the + must be at the END of a line
ggplot(mpg, aes(displ, hwy))
  ___ geom_point()
# b) a fixed colour goes OUTSIDE aes()
ggplot(mpg, aes(displ, hwy)) + geom_point(___ = "red")
# c) a variable name must be spelled exactly
ggplot(mpg, aes(displ, ___)) + geom_point()          # was: hwyy''',
  '''# a) the + must be at the END of a line
ggplot(mpg, aes(displ, hwy)) +
  geom_point()
# b) a fixed colour goes OUTSIDE aes()
ggplot(mpg, aes(displ, hwy)) + geom_point(colour = "red")
# c) a variable name must be spelled exactly
ggplot(mpg, aes(displ, hwy)) + geom_point()''', []),
N(18, 3, "Recreate a plot", "Recreate: city mpg (cty) on the y-axis vs. hwy on the x-axis, points coloured by drv, a dashed 45° line (geom_abline(linetype = 'dashed')), and coord_fixed(). What share of cars have cty < hwy?", LIB,
  "# Write all your code here\n",
  '''ggplot(mpg, aes(hwy, cty, colour = drv)) + geom_point() +
  geom_abline(linetype = "dashed") + coord_fixed()
share_lower <- mean(mpg$cty < mpg$hwy)
share_lower''', [("share", "mean(mpg$cty < mpg$hwy)", 3)]),
N(19, 4, "A chart for the manager", "Make one clear chart that compares the mean highway mpg of each manufacturer (sorted, horizontal bars, with the overall mean as a vertical line). Save it as a PNG in tempdir().", LIB,
  '''# 1. Mean hwy per manufacturer (aggregate() or tapply())
# 2. Horizontal bar chart sorted by the mean (geom_col + reorder)
# 3. geom_hline/vline for the overall mean
# 4. ggsave() to tempdir()
# 5. Which manufacturer is best? (comment)
''',
  '''m <- aggregate(hwy ~ manufacturer, data = mpg, FUN = mean)
p <- ggplot(m, aes(x = hwy, y = reorder(manufacturer, hwy))) +
  geom_col(fill = "steelblue") +
  geom_vline(xintercept = mean(mpg$hwy), linetype = "dashed") +
  labs(x = "Mean highway mpg", y = NULL, title = "Highway mpg by manufacturer")
p
ggsave(file.path(tempdir(), "hwy_by_maker.png"), p, width = 6, height = 4)
m$manufacturer[which.max(m$hwy)]
# Best: the manufacturer printed above (highest mean highway mpg).''', [("best_mean", "max(aggregate(hwy ~ manufacturer, data = mpg, FUN = mean)$hwy)", 2)]),
N(20, 5, "Exploratory mini report", "Explore `diamonds` with three plots of your choice (one distribution, one relationship, one comparison across groups). For each, write the question it answers and one finding. Finish with a 3-sentence summary.", LIB,
  '''# Plot 1 (distribution): question + finding as comments
# Plot 2 (relationship):  question + finding as comments
# Plot 3 (comparison):    question + finding as comments
# Summary (3 sentences as comments):
''',
  '''# Plot 1: How are carat sizes distributed? -> right-skewed, with peaks at "round" sizes (0.5, 1, 1.5).
ggplot(diamonds, aes(carat)) + geom_histogram(binwidth = 0.05)
# Plot 2: How does price change with carat? -> price rises steeply with carat.
ggplot(diamonds, aes(carat, price)) + geom_point(alpha = 0.05)
# Plot 3: Does clarity relate to size? -> better clarity grades tend to be smaller stones.
ggplot(diamonds, aes(clarity, carat)) + geom_boxplot()
round(tapply(diamonds$carat, diamonds$clarity, median), 2)
# Summary: carat is the strongest driver of price.
# Better cut and clarity grades are common among smaller stones, which hides their effect on price.
# Comparisons across quality grades should therefore control for carat.''', [("med_carat_IF", "median(diamonds$carat[diamonds$clarity == 'IF'])", 2)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M1 QUICK REFERENCE (ggplot2)                    ║
║  ggplot(data, aes(x, y, colour = g)) + geom_point()  ║
║  setting: geom_point(colour = 'red')  outside aes()  ║
║  geom_bar()  geom_histogram(binwidth)  geom_density()║
║  geom_boxplot()  geom_smooth(method = 'lm')          ║
║  position = 'dodge' / 'fill'   geom_jitter()         ║
║  facet_wrap(~ g)   facet_grid(r ~ c)                 ║
║  labs(title, x, y, colour)  theme_minimal()          ║
║  scale_x_log10()  coord_flip()  coord_fixed()        ║
║  ggsave('file.png', p, width, height)                ║
║  the + goes at the END of a line                     ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/m1_intro.html (650 M1 ggplot2)"
MOD = dict(key="n650_m1", title="650 M1 — Data Visualization with ggplot2: R Coding Practice (20 Questions)",
           file="650_m1_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/M1", wd=R650 + "/650 - Data Visualization/M1",
           data_note="Needs the ggplot2 package (`install.packages(\"ggplot2\")` once). Data sets `mpg` and `diamonds` come with ggplot2.",
           header_link=LINK, site_rmd=SITE,
           topics=[("First Plots & Aesthetics", A), ("Distributions", B),
                   ("Relationships, Groups & Facets", C), ("Communicating & Saving", D)], card=CARD)
MOD["questions"] = A + B + C + D
