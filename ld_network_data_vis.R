{
  library(ggplot2)
  library(ggnet)
  library(igraph)
  library(sna)
  library(randomcoloR)
}

data <- read.csv('output_2000gen.csv')


ggplot(data, aes(log(threshold), clustering, group=generation, color=generation)) + geom_point() + geom_line()

ggplot(data, aes((threshold), mean_degree, group=generation, color=generation)) + geom_point() + geom_line()

ggplot(data, aes((threshold), modularity, group=generation, color=generation)) + geom_point() + geom_line()

