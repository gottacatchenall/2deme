{
  library(ggplot2)
  library(ggnet)
  library(igraph)
  library(sna)
  library(randomcoloR)
}


get_mod_curve <- function(id){
  linkage <- read.csv('linkage.csv')
  global_linkage <- read.csv('global_linkage.csv')

  n_loci <- length(levels(as.factor(linkage$locus1)))
  
  # construct series of graphs
  
  
  data <- data.frame(matrix(ncol=4,nrow=1))
  colnames(data) <- c("gen", "mod", "mean_deg","thr")
  
  ct = 0
  for (gen in levels(as.factor(global_linkage$generation))){
    this_gen_gbl <- subset(global_linkage, generation == gen)
  
    thr <- seq(0.01, 0.25, 0.01)
    
    for (t in thr){
      mat <- matrix( rep( 0, len=n_loci*n_loci), nrow = n_loci)
      rownames(mat) <- 1:n_loci
      colnames(mat) <- 1:n_loci
      
      for (i in 1:nrow(this_gen_gbl)){
        this_row <- this_gen_gbl[i,]
        l1 <- this_row$locus1
        l2 <- this_row$locus2
        w <- this_row$D
        if (w > t){
          mat[l1,l2] <- (w) 
          mat[l2,l1] <- (w) 
        }
      }
      
      
      g <- graph_from_adjacency_matrix(mat, weighted = TRUE, mode="undirected")
      
      cm <- cluster_fast_greedy(g)
      mean_deg <- mean(degree(mat))
      mod <- modularity(cm)
      #num_cm <- length(unique(cm$membership))
      data[ct,] = c(as.numeric(gen), mod, mean_deg, as.numeric(t))
      ct = ct +1
      
      net <- network(mat, ignore.eval = FALSE, names.eval = "weights")
      coul = distinctColorPalette(length(unique(cm$membership)))
      net %v% "col" = coul[cm$membership]
      
      
      ggnet2(net, label=TRUE, mode='circle', color =  "col",  palette = coul) 
      #  ggsave(paste('gen',gen,'.png'), plot = last_plot()) 
      
      
    }
  }
  
  # how does modularity change with evolving threshold , how does avg degree
  
  ggplot(global_linkage, aes(D)) + geom_histogram() + facet_wrap(. ~ generation) 
  
  post_burn_in <- subset(data, as.numeric(gen) > 0)
  
  ggplot(post_burn_in, aes(thr, mod, color = gen, group = gen)) + geom_point() + geom_line() + xlab("LD Threshold")+ ylab("Modularity")
  
  ggplot(post_burn_in, aes(thr, mean_deg, color = gen, group = gen)) + geom_point() + geom_line() + xlab("LD Threshold")+ ylab("avg deg")
  ggsave(paste('all',id,'.png'), plot = last_plot()) 
  
  
  mean_d <- aggregate(mod ~ thr , data = post_burn_in, FUN = mean)
  
  ggplot(mean_d, aes(thr, mod)) + geom_line() + geom_point()  + xlab("LD Threshold")+ ylab("Modularity") + geom_point(data=post_burn_in, alpha=0.2, aes(color = gen, group = gen)) + geom_line(data=post_burn_in, alpha=0.2,aes(color = gen, group = gen))
  
  
  ggsave(paste('mean',id,'.png'), plot = last_plot()) 
  
}

i = 0
setwd("~/jan20_data")
for (dir in list.dirs()){
  if (dir != "."){
    setwd(dir)
    get_mod_curve(i)
    setwd("~/jan20_data")
    i = i + 1
  }
}


