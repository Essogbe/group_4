
data <- read.csv("C:\\Users\\emma\\OneDrive\\Bureau\\r_work\\Housing.csv")
head(data)

print(names(data))

hist(data$bedrooms)

# Intèprètation:

L'histogramme montre que la plupart des propriétés dans le dataset ont entre 2 et 4 chambres, ce qui représente le segment le plus fréquent. Les maisons avec 1 à 5 chambres sont moins courantes, indiquant une distribution moins uniforme. Cette tendance suggère que le marché immobilier est principalement composé de maisons adaptées à des familles de taille moyenne.
