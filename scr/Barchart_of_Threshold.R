#This script is to generate the bar-chart of different threshold
library(tidyverse)
library(ggplot2)

library(readr)

#Import data and check
setwd("H:/Lund_Project/Fifth")

all_amino_acid <- read_tsv("Amino_Acid_Count.tsv",show_col_types = FALSE)


cavity_amino_acid_2 <- read_tsv("Cavity_Amino_acid_2.tsv",show_col_types = FALSE)
cavity_amino_acid_3 <- read_tsv("Cavity_Amino_acid_3.tsv",show_col_types = FALSE)
cavity_amino_acid_1 <- read_tsv("Cavity_Amino_acid_1.tsv",show_col_types = FALSE)

#the tables are good
#extract columns name
amino_acids<-c(colnames(all_amino_acid)[2:21])
print(amino_acids)
#sum(x,na.rm=TRUE)
#print(sum(all_amino_acid$ALA))

#data[,1:3]
#sum(all_amino_acid[[2]])



#write a loop to get the sum of columns 
sum_all_amino_acid<-c()
sum_cavity_amino_acid_1<-c()
sum_cavity_amino_acid_2<-c()
sum_cavity_amino_acid_3<-c()

for(Col in seq(2,21)) {
  #print(all_amino_acid[[Col]])
  sum_all<-sum(all_amino_acid[[Col]])  
  sum_all_amino_acid<-append(sum_all_amino_acid,sum_all)
  
  #symbol_id<-append(symbol_id,id_list[[1]][1])
  
  sum_cavity_1<-sum(cavity_amino_acid_1[[Col]])  
  sum_cavity_amino_acid_1<-append(sum_cavity_amino_acid_1,sum_cavity_1)
  
  sum_cavity_2<-sum(cavity_amino_acid_2[[Col]])  
  sum_cavity_amino_acid_2<-append(sum_cavity_amino_acid_2,sum_cavity_2)
   
  sum_cavity_3<-sum(cavity_amino_acid_3[[Col]])  
  sum_cavity_amino_acid_3<-append(sum_cavity_amino_acid_3,sum_cavity_3)
}   

sum_all_amino_acid
sum_cavity_amino_acid_1
sum_cavity_amino_acid_2
sum_cavity_amino_acid_3

#the percentage of cavity
Percent_1<-c()
Percent_2<-c()
Percent_3<-c()

for (i in seq(1,20)){
  per_1<-sum_cavity_amino_acid_1[i]/sum_all_amino_acid[i]
  per_2<-sum_cavity_amino_acid_2[i]/sum_all_amino_acid[i]
  per_3<-sum_cavity_amino_acid_3[i]/sum_all_amino_acid[i]
  #round(2119.1921, digits = 3)
  per_1<-round(per_1,digits = 2)
  per_2<-round(per_2,digits = 2)
  per_3<-round(per_3,digits = 2)
  
  Percent_1<-append(Percent_1,per_1)
  Percent_2<-append(Percent_2,per_2)
  Percent_3<-append(Percent_3,per_3)
}
Percent_1
Percent_2
Percent_3

#create a data_frame
#df <- data.frame(a,b,c,d)
amino_acids
sum_all_amino_acid
sum_cavity_amino_acid_1
sum_cavity_amino_acid_2
sum_cavity_amino_acid_3
Percent_1
Percent_2
Percent_3

sum_df<-data.frame()
sum_df<-data.frame(amino_acids,
                   sum_all_amino_acid,
                   sum_cavity_amino_acid_1,
                   sum_cavity_amino_acid_2,
                   sum_cavity_amino_acid_3,
                   Percent_1,
                   Percent_2,
                   Percent_3)

##
#plot threshold 1
ggplot(sum_df)+
  #all blue
  geom_bar(aes(x=amino_acids,y=sum_all_amino_acid),stat="identity",fill="blue")+
  #cavity red
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_1),stat="identity",fill="red")+
  
  #geom_text(aes(x=amino_acids,y=sum_all_amino_acid_2,label=Percent_2), check_overlap = TRUE)+
  ylim(0,max(sum_all_amino_acid)*1.2)



# Plot threshold 2
ggplot(sum_df)+
  #all blue
  geom_bar(aes(x=amino_acids,y=sum_all_amino_acid),stat="identity",fill="blue")+
  #cavity red
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_2),stat="identity",fill="red")+
  
  #geom_text(aes(x=amino_acids,y=sum_all_amino_acid_2,label=Percent_2), check_overlap = TRUE)+
  ylim(0,max(sum_all_amino_acid)*1.2)

# Plot threshold 3
ggplot(sum_df)+
  #all blue
  geom_bar(aes(x=amino_acids,y=sum_all_amino_acid),stat="identity",fill="blue")+
  #cavity red
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_3),stat="identity",fill="red")+
  
  #geom_text(aes(x=amino_acids,y=sum_all_amino_acid_3,label=Percent_3), check_overlap = TRUE)+
  ylim(0,max(sum_all_amino_acid)*1.2)

#summary
ggplot(sum_df)+
  #all blue
  geom_bar(aes(x=amino_acids,y=sum_all_amino_acid),stat="identity",fill="blue")+
  #threshold 1 red
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_1),stat="identity",fill="red")+
  #threshold 2 purple
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_2),stat="identity",fill="purple")+
  #threshold 3 green
  geom_bar(aes(x=amino_acids,y=sum_cavity_amino_acid_3),stat="identity",fill="green")+
  
  
  #geom_text(aes(x=amino_acids,y=sum_all_amino_acid_3,label=Percent_3), check_overlap = TRUE)+
  ylim(0,max(sum_all_amino_acid)*1.2)

###############doing paired t-test for cavity and protein
#sum(sum_cavity_amino_acid_1)

normalize_sum_cavity_amino_acid_1<-c()
normalize_sum_all_amino_acid<-c()
#modified_data <- append(data, 11)
for (i in 1:20)
{
  x<-sum_cavity_amino_acid_1[i]/sum(sum_cavity_amino_acid_1)#x is percent of amino acid
  #sum(sum_cavity_amino_acid_1)
  normalize_sum_cavity_amino_acid_1<-append(normalize_sum_cavity_amino_acid_1,x)
  normalize_sum_all_amino_acid<-append(normalize_sum_all_amino_acid,sum_all_amino_acid[i]/sum(sum_all_amino_acid))
}
# #### This is another way to calculate percent
# randome <- sum_cavity_amino_acid_1/sum(sum_cavity_amino_acid_1)
# randome
####
normalize_sum_cavity_amino_acid_1
normalize_sum_all_amino_acid

res <- t.test(normalize_sum_cavity_amino_acid_1, normalize_sum_all_amino_acid, paired = TRUE)
res
#wilcoxn
wilcox.test(normalize_sum_cavity_amino_acid_1, normalize_sum_all_amino_acid, paired=TRUE)# the order is settled

# sum(sum_cavity_amino_acid_1)
# sum(sum_all_amino_acid)
# sum_cavity_amino_acid_1
# sum_all_amino_acid

whole_entities<-normalize_sum_all_amino_acid
protein_cavities<-normalize_sum_cavity_amino_acid_1
percentage<- data.frame(whole_entities,protein_cavities)
rownames(percentage) <- amino_acids
percentage_new<-as.data.frame(t(percentage))
print (percentage_new)
