#Projet R et python avancer

data <- read.csv("/home/elfriedkinzoun/Downloads/arch/Housing.csv")

data

ggplot(data , aes(x=area, y=price)) + geom_point(size=2, shape=1) + geom_smooth()

#Interprètation

#Le graphique ci-dessus illustre la relation entre la surface (area) et le prix (price) d'un ensemble d'observations. Chaque point représente une observation individuelle, indiquant comment le prix varie en fonction de la surface. La ligne bleue indique la tendance générale de cette relation, révélant qu'en général, à mesure que la surface augmente, le prix a tendance à augmenter également. Cependant, cette relation n'est pas parfaitement linéaire, comme en témoigne la courbure de la ligne bleue. La zone grise entourant cette ligne représente l'intervalle de confiance, démontrant une incertitude croissante pour les valeurs plus élevées de surface. Cette incertitude suggère que pour des surfaces plus grandes, le prix devient plus variable et moins prévisible. En outre, la dispersion des points autour de la ligne de tendance souligne l'existence d'autres facteurs influençant le prix en plus de la surface, et la présence de valeurs aberrantes mérite une analyse plus approfondie. En conclusion, bien que la surface soit un indicateur important du prix, elle n'explique pas entièrement la variation des prix observés.