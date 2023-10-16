library (readr)

# Read file
data <- read_csv("data.csv")

# Draw plot
plot(data$x_shell,
     data$y_shell,
     main="100 random shoots",
     xlab="x coord",
     ylab="y coord",
     pch=19)