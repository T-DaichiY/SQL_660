"""650 M2: data import (readr) and dplyr verbs: rows, columns, the pipe, groups."""
from nb_build import N

R650 = "/Users/apple/Documents/02_Areas/School_Teaching_Master/Eastern"
SITE = [R650 + "/650 - Data Visualization/Lesson_website/rmd", R650 + "/660 - SQL/Lesson_website/r650/rmd"]
LIB = "library(readr)\nlibrary(dplyr)"

A = [
N(1, 1, "Read a CSV with read_csv()", "Read `students.csv` (the R4DS example file in the M2 folder) and look at it.", LIB, "",
  '''# === Complete example — read and run ===
students <- read_csv("students.csv")
students
spec(students)            # the column types readr guessed
dim(students)''', [("rows", "nrow(students)", 0)]),
N(2, 2, "Missing-value codes and column names", "Treat both \"N/A\" and empty cells as missing, and rename the awkward columns.", LIB,
  '''students <- read_csv("students.csv", na = c("___", "___"))
students <- students |>
  rename(student_id = `Student ID`, full_name = `___`,
         favourite_food = favourite.food, meal_plan = ___, age = ___)
sum(is.na(students$favourite_food))''',
  '''students <- read_csv("students.csv", na = c("N/A", ""))
students <- students |>
  rename(student_id = `Student ID`, full_name = `Full Name`,
         favourite_food = favourite.food, meal_plan = mealPlan, age = AGE)
sum(is.na(students$favourite_food))''', [("n_na_food", "sum(is.na(students$favourite_food))", 0)]),
N(3, 3, "Fix the types", "`age` was read as text because one value is \"five\". Fix it (\"five\" → 5), convert age to a number and meal_plan to a factor. Report the mean age.", LIB,
  "# Write all your code here\n",
  '''students <- students |>
  mutate(age = parse_number(if_else(age == "five", "5", age)),
         meal_plan = factor(meal_plan))
students
round(mean(students$age, na.rm = TRUE), 2)
levels(students$meal_plan)''', [("mean_age", "mean(students$age, na.rm = TRUE)", 2)]),
N(4, 4, "Write and re-read a file", "Save the cleaned data to a CSV in tempdir(), read it back, and check whether the column types survive the round trip.", LIB,
  '''# 1. write_csv() to file.path(tempdir(), "students_clean.csv")
# 2. read_csv() it back
# 3. Compare the classes of the columns before and after
# 4. Conclusion (comment): what is lost when we save to CSV?
''',
  '''path <- file.path(tempdir(), "students_clean.csv")
write_csv(students, path)
back <- read_csv(path, show_col_types = FALSE)
sapply(students, class)
sapply(back, class)
# A CSV only stores text: the factor comes back as character, so types must be set again.''', [("cols", "ncol(back)", 0)]),
N(5, 5, "Inline data and parsing problems", "Read the inline CSV below with read_csv(I(...)). Use `col_types` to read `price` as a number and `date` as a date, find the problem rows with problems(), and write 3 sentences on good import habits.",
  '''raw <- "item,price,date
apple,1.20,2026-01-05
pear,unknown,2026-01-06
fig,2.50,05/01/2026"''',
  '''# 1. read_csv(I(raw), col_types = cols(price = col_double(), date = col_date()))
# 2. problems() on the result
# 3. How many NAs did the parsing create?
# 4. Report (3 sentences as comments):
''',
  '''d <- read_csv(I(raw), col_types = cols(item = col_character(), price = col_double(), date = col_date()))
d
problems(d)
n_new_na <- sum(is.na(d$price)) + sum(is.na(d$date))
n_new_na
# Always check the types readr guessed (spec) and set them with col_types when needed.
# Values that cannot be parsed become NA and are listed by problems().
# Fix the raw data or the parsing rule instead of silently keeping those NAs.''', [("n_new_na", "n_new_na", 0)]),
]

B = [
N(6, 1, "filter() and arrange()", "Find the starwars characters taller than 200 cm, tallest first.", LIB, "",
  '''# === Complete example — read and run ===
tall <- starwars |>
  filter(height > 200) |>
  arrange(desc(height)) |>
  select(name, height, species)
tall
nrow(tall)''', [("n_tall", "nrow(tall)", 0)]),
N(7, 2, "Several conditions", "Keep humans OR droids whose mass is known, sorted by mass.", LIB,
  '''starwars |>
  filter(species ___ c("Human", "Droid"), !is.na(___)) |>
  arrange(___) |>
  select(name, species, mass)''',
  '''starwars |>
  filter(species %in% c("Human", "Droid"), !is.na(mass)) |>
  arrange(mass) |>
  select(name, species, mass)''', [("n_rows", "nrow(dplyr::filter(starwars, species %in% c('Human','Droid'), !is.na(mass)))", 0)]),
N(8, 3, "distinct() and counts", "How many different homeworlds are there in starwars (excluding NA)? Which homeworld appears most often? Use distinct() and count().", LIB,
  "# Write all your code here\n",
  '''n_worlds <- starwars |> filter(!is.na(homeworld)) |> distinct(homeworld) |> nrow()
n_worlds
starwars |> count(homeworld, sort = TRUE) |> head(3)''', [("n_worlds", "n_worlds", 0)]),
N(9, 4, "Storm search", "A meteorologist wants all observations of category-5 hurricanes in `storms`. Filter them, list the distinct storm names and years, and find the strongest wind recorded.", LIB,
  '''# 1. filter(category == 5)
# 2. distinct(name, year), sorted by year
# 3. Maximum wind speed
# 4. Note for the meteorologist (comment):
''',
  '''cat5 <- storms |> filter(category == 5)
cat5 |> distinct(name, year) |> arrange(year)
max(cat5$wind)
# Note: the list above shows every storm that reached category 5 and when.''', [("max_wind", "max(storms$wind[storms$category == 5], na.rm = TRUE)", 0)]),
N(10, 5, "Missing values in filter()", "filter() drops rows where the condition is NA. Show this with starwars: count characters with mass > 80, mass <= 80, and NA mass, and check that the three add up to the total. Write 3 sentences.", LIB,
  '''# 1. n with mass > 80
# 2. n with mass <= 80
# 3. n with is.na(mass)
# 4. Do they add up to nrow(starwars)?
# 5. Report (3 sentences as comments):
''',
  '''n_heavy <- starwars |> filter(mass > 80) |> nrow()
n_light <- starwars |> filter(mass <= 80) |> nrow()
n_na <- starwars |> filter(is.na(mass)) |> nrow()
c(n_heavy, n_light, n_na, total = nrow(starwars), sum = n_heavy + n_light + n_na)
# filter() keeps only rows where the condition is TRUE; NA rows silently disappear.
# The two opposite conditions together miss the characters with unknown mass.
# Always check is.na() separately when a column has missing values.''', [("n_na", "n_na", 0)]),
]

C = [
N(11, 1, "select(), rename(), relocate()", "Pick and tidy columns of starwars.", LIB, "",
  '''# === Complete example — read and run ===
sw <- starwars |>
  select(name, height, mass, species, homeworld) |>
  rename(world = homeworld) |>
  relocate(species, .before = height)
sw
ncol(sw)''', [("ncol", "ncol(sw)", 0)]),
N(12, 2, "mutate(): BMI", "Add BMI = mass / (height/100)^2 and keep the five highest.", LIB,
  '''starwars |>
  ___(bmi = mass / (height / 100)^___) |>
  select(name, height, mass, bmi) |>
  arrange(desc(___)) |>
  head(5)''',
  '''starwars |>
  mutate(bmi = mass / (height / 100)^2) |>
  select(name, height, mass, bmi) |>
  arrange(desc(bmi)) |>
  head(5)''', [("max_bmi", "max(starwars$mass / (starwars$height / 100)^2, na.rm = TRUE)", 1)]),
N(13, 3, "Select helpers", "From `storms`, select name, year and every column that ends with \"_diameter\". Then add a column `ts_km` with tropicalstorm_force_diameter in kilometres (1 nautical mile = 1.852 km).", LIB,
  "# Write all your code here\n",
  '''st <- storms |>
  select(name, year, ends_with("_diameter")) |>
  mutate(ts_km = tropicalstorm_force_diameter * 1.852)
names(st)''', [("ncols", "ncol(dplyr::select(storms, name, year, dplyr::ends_with('_diameter'))) + 1", 0)]),
N(14, 4, "Fuel cost per 100 km", "A rental company wants the fuel cost of each car in `ggplot2::mpg` for 100 km of highway driving at $1.60 per litre. Convert hwy (miles per US gallon) to L/100 km (235.215 / hwy) and add the cost. Which model is cheapest?", "library(dplyr)\nmpg <- ggplot2::mpg",
  '''# 1. mutate(l_per_100 = 235.215 / hwy, cost_100km = l_per_100 * 1.60)
# 2. select the useful columns only
# 3. arrange by cost and show the cheapest 3
# 4. Recommendation (comment):
''',
  '''costs <- mpg |>
  mutate(l_per_100 = 235.215 / hwy, cost_100km = l_per_100 * 1.60) |>
  select(manufacturer, model, year, hwy, l_per_100, cost_100km) |>
  arrange(cost_100km)
head(costs, 3)
round(costs$cost_100km[1], 2)
# Recommendation: the small cars at the top of this list are the cheapest to run on the highway.''', [("min_cost", "min(235.215 / mpg$hwy * 1.60)", 2)]),
N(15, 5, "if_else() and case_when()", "Classify starwars characters by height: 'short' (< 150), 'medium' (150-190), 'tall' (> 190), and NA when height is unknown. Count each group and write 3 sentences on case_when() vs if_else().", LIB,
  '''# 1. mutate(size = case_when(...))
# 2. count(size)
# 3. A second column with if_else(): 'droid' vs 'not droid'
# 4. Report (3 sentences as comments):
''',
  '''sized <- starwars |>
  mutate(size = case_when(height < 150 ~ "short",
                          height <= 190 ~ "medium",
                          height > 190 ~ "tall",
                          .default = NA),
         droid = if_else(species == "Droid", "droid", "not droid", missing = "unknown"))
sized |> count(size)
sized |> count(droid)
# if_else() is for two outcomes; case_when() handles many conditions in order.
# The first condition that is TRUE wins, so the order of the lines matters.
# Rows that match nothing (here unknown height) get the .default value.''', [("n_tall", "sum(starwars$height > 190, na.rm = TRUE)", 0)]),
]

D = [
N(16, 1, "group_by() and summarise()", "Mean height and count per species (species with at least 2 characters).", LIB, "",
  '''# === Complete example — read and run ===
by_species <- starwars |>
  group_by(species) |>
  summarise(n = n(), mean_height = mean(height, na.rm = TRUE)) |>
  filter(n >= 2) |>
  arrange(desc(n))
by_species''', [("n_species", "nrow(by_species)", 0)]),
N(17, 2, "The pipe |> reads like a sentence", "Rewrite the nested code as a pipe.", LIB,
  '''# Nested:
head(arrange(filter(starwars, !is.na(mass)), desc(mass)), 3)
# Piped (fill in):
starwars |>
  ___(!is.na(mass)) |>
  ___(desc(mass)) |>
  ___(3)''',
  '''# Nested:
head(arrange(filter(starwars, !is.na(mass)), desc(mass)), 3)
# Piped:
starwars |>
  filter(!is.na(mass)) |>
  arrange(desc(mass)) |>
  head(3)''', [("top_mass", "max(starwars$mass, na.rm = TRUE)", 0)]),
N(18, 3, "Storm summary by year", "For `storms`, compute per year: number of distinct storms, maximum wind and mean pressure. Which year had the most distinct storms?", LIB,
  "# Write all your code here\n",
  '''per_year <- storms |>
  group_by(year) |>
  summarise(n_storms = n_distinct(name), max_wind = max(wind), mean_pressure = mean(pressure))
per_year |> arrange(desc(n_storms)) |> head(3)''', [("max_storms", "max(dplyr::summarise(dplyr::group_by(storms, year), n = dplyr::n_distinct(name))$n)", 0)]),
N(19, 4, "Car report by class", "Using `ggplot2::mpg`, make a table per class with: number of models, mean hwy, mean cty and the share of 4-wheel drive. Sort by mean hwy and identify the most and least efficient classes.", "library(dplyr)\nmpg <- ggplot2::mpg",
  '''# 1. group_by(class) |> summarise(...)
# 2. arrange(desc(mean_hwy))
# 3. Most / least efficient class (comment)
''',
  '''report <- mpg |>
  group_by(class) |>
  summarise(n = n(), mean_hwy = mean(hwy), mean_cty = mean(cty), share_4wd = mean(drv == "4")) |>
  arrange(desc(mean_hwy))
report
# Most efficient: compact / subcompact; least efficient: pickup.''', [("top_hwy", "max(tapply(mpg$hwy, mpg$class, mean))", 2)]),
N(20, 5, "Grouped mutate and .by", "For each storm (name + year), compute its peak wind with a grouped mutate(), keep only the row(s) where wind equals the peak, and compare with summarise(.by = ...). Count storms whose peak wind is at least 100 knots. Write 3 sentences.", LIB,
  '''# 1. group_by(name, year) |> mutate(peak = max(wind)) |> filter(wind == peak)
# 2. summarise(peak = max(wind), .by = c(name, year))
# 3. Number of storms with peak >= 100
# 4. Report (3 sentences as comments):
''',
  '''peaks_rows <- storms |>
  group_by(name, year) |>
  mutate(peak = max(wind)) |>
  filter(wind == peak) |>
  ungroup()
peaks <- storms |> summarise(peak = max(wind), .by = c(name, year))
n_strong <- sum(peaks$peak >= 100)
c(rows_at_peak = nrow(peaks_rows), storms = nrow(peaks), strong = n_strong)
# A grouped mutate() keeps every row and adds the group value to each one.
# summarise() collapses each group to one row; .by groups just for that step.
# Remember ungroup() after group_by(), or later steps will still work per group.''', [("n_strong", "n_strong", 0)]),
]

CARD = '''╔══════════════════════════════════════════════════════╗
║  650 M2 QUICK REFERENCE (readr + dplyr)              ║
║  read_csv('f.csv', na = c('N/A', ''))  spec()        ║
║  col_types = cols(x = col_double())   problems()     ║
║  rename(new = `old name`)  parse_number()            ║
║  filter(a > 1, b %in% c(...))   arrange(desc(x))     ║
║  distinct(x)   count(x, sort = TRUE)                 ║
║  select(a, b, ends_with('_x'))  relocate(.before)    ║
║  mutate(y = ...)  if_else()  case_when(... ~ ...)    ║
║  group_by(g) |> summarise(n = n(), m = mean(x))      ║
║  summarise(..., .by = g)   ungroup()                 ║
║  x |> f() |> g()   ==   g(f(x))                      ║
╚══════════════════════════════════════════════════════╝'''

LINK = "📖 Matching lessons: https://t-daichiy.github.io/SQL_660/r650/m2_import.html (650 M2 import & dplyr)"
MOD = dict(key="n650_m2", title="650 M2 — Data Import & Transformation with dplyr: R Coding Practice (20 Questions)",
           file="650_m2_practice_v1.Rmd", folder=R650 + "/650 - Data Visualization/M2", wd=R650 + "/650 - Data Visualization/M2",
           data_note="Needs the readr and dplyr packages (or `library(tidyverse)`). Topic A uses `students.csv` (R4DS example file in the M2 folder); the rest use `starwars`, `storms` (dplyr) and `mpg` (ggplot2).",
           header_link=LINK, site_rmd=SITE,
           topics=[("Data Import with readr", A), ("Rows: filter, arrange, distinct", B),
                   ("Columns: select, rename, mutate", C), ("The Pipe & Groups", D)], card=CARD)
MOD["questions"] = A + B + C + D
