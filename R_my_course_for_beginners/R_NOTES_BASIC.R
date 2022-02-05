

######################################################################
#########################################################################################
#################################################################################################################
###
## ---------   -1- HELP, DIR and WORKING SPACE 
###
#################################################################################################################
#########################################################################################
######################################################################
			 -1-
			 -1-
			 -1-
		  *|||||||*
		   *|||||*
			*|||*
			 *|*
			  *
--------------------------------------------------
----------------------------------------------------------------------

 1. help
 2. directory
 3. cleaning
 4. working space 

----------------------------------------------------------------------
--------------------------------------------------






--------------------
###              #################################################################
### --- HELP --- ###
###              #################################################################
--------------------
	
> Basic
	version
	help()
	?_Function_Name
	?plot

> Help
	help.start()
		# redirection - internet
	> Rinferno :)
	> help for pg,s
		help(package="foreign")
		help(package="XML")

> BOOKs:
	"R programmin for Bioinformatics"
	- nicely writen book
	- nice for also nonprogrammers	

> Internet:
	>> Rseek the google for R :
	www.rseek.org/
	>> R help
	http://cran.r-project.org/manuals.html

    help(options) # learn about available options
    options() # view current option settings
    options(digits=3) # number of digits to print on output



---------------------
###               #################################################################
### - DIRECTORY - ###
###               #################################################################
---------------------

getwd()
setwd("/Users/prosikie/Desktop/R_TRAINING")
dir()
dir.create("new_directory")

setwd("c:/docs/mydir")  # note / instead of \ in windows
setwd("/usr/rob/mydir") # on linux

> IMPORTANT NOTE FOR WINDOWS USERS:
    # R gets confused if you use a path in your code like
    c:\mydocuments\myfile.txt
    #This is because R sees "\" as an escape character. Instead, use
    c:\\my documents\\myfile.txt
    c:/mydocuments/myfile.txt


---------------------
###               #################################################################
### - CLEANING  - ###
###               #################################################################
---------------------

ls()
# a list of what i put into R working space
rm(list=ls())






--------------------------
###				       #################################################################
### ---   WORKING  --- ###
### ---    SPACE   --- ###
###				       #################################################################
--------------------------
# - commands 
	- search 
	- ls
	- attach
--------------------------

	atache()
		# (nay_list_or _data_frame)
	detach()	
		
	search()
		search()
 			[1] ".GlobalEnv"
			# its a working space 
			# including packages
	ls(2)
		# for each variable we put into 

    # save the workspace to the file .RData in the cwd
        save.image()

    # save specific objects to a file
    # if you don't specify the path, the cwd is assumed
        save(object list,file="myfile.RData")

    # load a workspace into the current session
    # if you don't specify the path, the cwd is assumed
        load("myfile.RData")



---------------------
###               #################################################################
### -  HISTORY  - ###
###               #################################################################
---------------------



# work with your previous commands
history() # display last 25 commands
history(max.show=Inf) # display all previous commands

# save your command history
savehistory(file="myfile") # default is ".Rhistory"

# recall your command history
loadhistory(file="myfile") # default is ".Rhistory"








######################################################################
#########################################################################################
#################################################################################################################
###
## ---------   -2- R ECOSYSTEM
###
#################################################################################################################
#########################################################################################
######################################################################
			 -2-
			 -2-
			 -2-
		  *|||||||*
		   *|||||*
			*|||*
			 *|*
			  *
--------------------------------------------------
----------------------------------------------------------------------

 1. Pg Installation and downloading
 2. Data Import
 3. Data Export
 4. R data structures 
  	- vectors
	- matrix
	- data Frame
	- list
 5. Sequnce of Numbers
 6. Data exploring and transformation
 7. Subsetting data
 8. RAM PROBLEM
 9. Connecting to DataBase
10. Importing raw Microarray data - CEL file

----------------------------------------------------------------------
--------------------------------------------------







##########################################################################################
------------------------------------------------------------------------------------------
1. Pg Installation and downloading
------------------------------------------------------------------------------------------
##########################################################################################


	> Packages (Pg)
	--------------------------------------------------------------------------------------
		# CRAN - main R site
		# and
		# bioconductor - biomedical specialized
		installed.packages()
			#
	
	> from CRAN
	--------------------------------------------------------------------------------------
		install.packages('ggplot2')
        install.packages("PACKAGE_NAME", dependencies=TRUE)
	
		
	> Pg inst. from biocoductor	
	--------------------------------------------------------------------------------------
		source("http://bioconductor.org/biocLite.R")
		biocLite()
		biocLite("ArrayExpress")
	
	
	> pg Update:
	--------------------------------------------------------------------------------------
 		update.packages(checkBuilt=TRUE, ask=FALSE)
 			# R
 		biocLite(character(), ask=FALSE)	
			# bioconductor






########################################################################################## 
------------------------------------------------------------------------------------------
2. Data Import																					
------------------------------------------------------------------------------------------	
##########################################################################################


										     read.table
								RRR	<<<< ---------------
										   "xlsx"  	    |		
					RRRRR <<<< ---------------------- MEMORY
								    "foreign"		    |	
						RRRR <<< -----------------------
								  		      read.csv

	> R can take
	---------------------------------------------------------------------------------------
	
		# text files
		# proprietary formats (such as SAS, SPSS, Stata, Excel....)
		# databases (Oracle, MySQL, CouchDB, SQLite...)
		# WEKA
			# data mining mashine
			# very powerful !
			# a popular softwear (in Java) of mashine learning
			# tools for data anaylysis and predictive modelling
		# Rand S  data 
		# XLM and HTML tables
		# more ...
		
		
	> read.table
	---------------------------------------------------------------------------------------
		# importing a text file 
		# using path
			URL <- "http://www.stanford.edu/~druau/pivot_table.csv"
				# this is not working any more
				# pivot_table is also a function in a pg reshape
			pivot <- read.table(URL, sep=',', header=TRUE)
			head(pivot)
			class(pivot)
			
			
	> read.csv
	---------------------------------------------------------------------------------------
		data<-read.csv("NHIS 2007 data.csv",header=T)
		data2<-read.table("NHIS 2007 data.csv",header=T,sep=',')
			# - the same  
			# - read.csv have many variants
	
		command	  separator	  decimal (i.e. 1,245556...)
		---------------------------------------------------
		# csv 		','			'.'
		# csv2 		';'			','
		# delim		'\t'		'.'
		# delim2	'\t'		','
		----------------------------------------------------
		
		# DO NOT Forget about quotes '\' 
		# which can disable all these special char. 
		# but they works only in rows








			
	> Multiple files at one - from Tomek
	---------------------------------------------------------------------------------------	
			
		lf <- list.files()
		df <- lapply(lf, read.table, header = T)
		sp_names <- lapply(strsplit(lf, ".", fixed = TRUE), function(x) x[1])
		names(df) <- unlist(sp_names)	
		
			
	> Pg,s specialized to import data:
	---------------------------------------------------------------------------------------
		library("foreign")
		help(package="foreign")
			# one of the key pg,s !!!!
			# help - for different types of data which it can read
			# SAS, SPSS and many many more...
		
		library("xlsx")
		? read.xlsx
			# Very powerfull
			# reads EXCEL FILE
	
		library("XML")
		help(package="XML")
			# very usefull then i  need to take a data from a table on internet site
			# without i would have to copy and past every single value
			#one of the key pg's
			# example
				eq <- readHTMLTable("http://www.iris.edu/seismon/last30.html")
				eq
				dim(eq)
				class(eq)	
		
		help.start()
 			# more options for import/export data !!!






##########################################################################################		
------------------------------------------------------------------------------------------			
3. Data Export																									
------------------------------------------------------------------------------------------
##########################################################################################				

							
							RRRR ----->>>>> SAVE
										
											RRRR ----->>>>> SAVE
								
									RRRR ----->>>>> SAVE



			[here I have --------------------------------------------------]
				save(foo,file="foo.Rda")			/load("foo.Rda")
				dump(foo,file="foo")				/source("dumpdata.R")
				pdf(file="foo.pdf")//dev.off()
				write.table(foo, file="foo.txt")	/read.table("foo.txt")
				create.dir()
			[--------------------------------------------------------------]




	> save and load
	---------------------------------------------------------------------------------------
		# for whatever I have in R
		# Example:
			# Playground :
				source("http://www.r-statistics.com/wp-content/uploads/2012/01/source_https.r.txt")
				setwd("/Users/prosikie/Desktop/R_TRAINING")
				data<-read.csv("NHIS 2007 data.csv",header=T)	
			# save data.frame
				> One File:
					iris
					save(iris,file='iris_Rda')
					dir()
					load('iris_Rda')
				> more than one file:			
					aaa<-1:40
					iris
					data
					save(list=c('aaa', 'iris', 'data'), file="data_export.Rda")
					dir()
					ls()
					rm(list=ls())
					load('data_export.Rda')
						# Rda - a classic extension for R
						# i can put wahtever i want, but it can make a problem for relowding
						# Remember "data_frame_name" or 'data_frame_name'


            ## save all data
                --------------------------------------------------

                xx <- pi # to ensure there is some data
                save(list = ls(all = TRUE), file= "all.RData")
                rm(xx)

            ## restore the saved values to the current environment
                local({
                    load("all.RData")
                    ls()
                })
            ## restore the saved values to the user's workspace
                load("all.RData", .GlobalEnv)

                unlink("all.RData")






	> dump / sourced
	---------------------------------------------------------------------------------------
		# i think here the data.frame structure is not saved!
		# probably just plain text 
		# with commands
			dump('iris')
			dir()
			ls()
			rm(list=ls())
			source("dumpdata.R")
				
				
	
	
	> write.table
	---------------------------------------------------------------------------------------
		# gives output in a text format
		# many programmes can take it after
		
		iris
		write.table(iris, file="iris_table.txt")	
		dir()
		iris2 <- read.table("iris_table.txt")
		iris2
		
		# MacOS vs Windows
				# OS
				write.table(foo, file="/users/name/folder/filename.ext")
				# Windows
				write.table(foo, file="C:/users/name/folder/filename.ext")
        # interesting script which was made to chnage names of subVCF files inside the file (each row, 1st column)
        # and the file names itself
        # in order to save new file in the same format i hade to explore row.names=FALSE and quote=FALSE !!!!
setwd("/Users/prosikie/Desktop/NEW_theory/test")
dir()
subVCF_names<-read.csv("New_and_Old_names.csv", header=TRUE)
subVCF_names<-as.matrix(subVCF_names)
sorted_subVCF_names<-subVCF_names
sorted_subVCF_names[,1]<-sort(subVCF_names[,1])
sorted_subVCF_names[,2]<-sort(subVCF_names[,2])

old_names<-sorted_subVCF_names[,1]	# change
new_names<-sorted_subVCF_names[,2]	# change

for(sample_name in 1:length(old_names)){
	###########
	one_subVCF		<-read.csv(old_names[sample_name], sep="\t", header=TRUE)
	one_subVCF		<-as.matrix(one_subVCF)
	###########
	new_file_name	<-new_names[sample_name]
	splitted_name	<-strsplit(new_file_name, split="_")
	splitted_name	<-splitted_name[[1]]
	new_isolate_name<-splitted_name[1]
	###########
	one_subVCF[,1]	<-new_isolate_name
	one_subVCF		<-as.data.frame(one_subVCF)
	write.table(one_subVCF,file=new_file_name,sep="\t", row.names=FALSE, quote=FALSE)
}














	
	> dir.create()
	---------------------------------------------------------------------------------------
		dir.create("new_directory")		
		dir()
	
	
	> pdf
	---------------------------------------------------------------------------------------
		# a code with results and multiple graphs:
			pdf(file="File_name.pdf")
					code
					code
					code
					code
					code
					code
			dev.off()	
			
				[Desriptions ---------------------------------------------------------------]
				   par(mfrow=c(1,1)) 
					plot(0:10, type = "n", xaxt="n", yaxt="n", bty="n", xlab = "", ylab = "")	
					text(5, 9, "Step 1")
				 [Desriptions ------------------------------------------------------------END]
		
	> capture.output  - very usefull for table print, spy protocol
	---------------------------------------------------------------------------------------
		
		# put the table in pdf
		# or into new txt file
		# Table
			cc<-c(NA,1,2,4,NA)
			dd<-1:100
			m2<-matrix(data=cbind(dd, rnorm(100,0), rnorm(100,2), rnorm(100,5), rep(cc,20)), nrow=100, ncol=5)
			long_names<-c(rep(c("long_names_nr_one", "long_name_TWO", "a_generaly_long_name", "unsusual_log_name"),25))
			short_names<-c("NR","group1","group2","group3","group4")
			colnames(m2)<-short_names
			rownames(m2)<-long_names
		# in pdf
			pdf(file="file_name")
			capture.output(m2)
			dev.off()
		# in separate txt file
			capture.output(m2, file="file_name")



##########################################################################################
------------------------------------------------------------------------------------------
4. R data structures
------------------------------------------------------------------------------------------
##########################################################################################		
		
		
	[Four classes ---------]	
		> 4.1 Vector
		> 4.2 Matrix
		> 4.3 Data.frame
		> 4.4 list
	[----------------------]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	> 4.1 Vectors																	VECTOR	
	---------------------------------------------------------------------------------------		
	#######################################################################################	
	
	
				vec <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
					vec <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
						vec <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19)
	
	
	
	
	
		# Vector of strings
 			x <- c("Lincoln", "Roosevelt", "Jackson")
 		# Replace the second element of the vector
 			x[2] <- NA
 			x
 		# serching NA 
 			x[is.na(x)]
 			x[!is.na(x)]
 			
 		>>>Four Types of Vectors:
 		-----------------------------------
 			# Character
 			# Numerical
 			# Integrer
 			# Logical
 			# Ex:
	  		## Character Vectors
 				x <- c("Lincoln", "Roosevelt", "Jackson"); 
 				class(x)
			## Numeric Vector
			 	x <- c(1.2, 1.5); 
 				class(x)
 			## Integrer Vector
 				x <- 1:4; 
				class(x)
			 ## Logical Vector	
				x <- x>2; 
				x
				class(x)
		
		>>> Creating vectors:
		--------------------------------
			x = c(1, 2, 3, 4) ; 
			x = 1:4
			x
			x+10 # R is vectorized
			x[4] # Accessing the fourth element	

		>>> Logical functions: 
		---------------------------------
			# False/True question
			x>2
			# Selection of elements
			x[x>2]
			# hifgher in value than 2 !
				aa<-c(4,5,8,9)
				aa
				aa[aa>4]
				x[1:3]
			#3 elemets:)
				is.na(x)
				sum(x)
				cumsum(x)
			# CUMULATIVE sum!
				summary(x)
				
		>>> Basic mathematical functions:
		---------------------------------
			> structure
				Funtion_name()
			>Examples	
				x <-c(rnorm(1000,5))
				mean(x)
				median(x)
				sd(x)
				sum(x)
				str(x)
				sqrt(x[1:5])
				plot(x)
				hist(x)
				summary(x)
	
	
		>>> Converting vectors
		---------------------------------
			-> Factors vs numeric
				- factor  == nonlevel value	  => works with characters
				- numeric == levels	    	  => to work with numbers

			-> factor vector -> intergreter/numeric
				- no loss of information
				- it is better to not convert it one into another categorry if I dont have to 
	
			-> Examples:
			# vec with Charakters
			-----------------		
				blah<-c("1","2","6","5")
				blah
				summary(blah)
				# no data => class = character
				dim(blah)
				# mean, sum etc... --- not working ---
				#
			# vec with Numbers
			-----------------	
				blam<-c(1,2,6,5)
				blam
				summary(blam)
				# full data, i.e. min, max, median etc..
				dim(blam)
				mean(blam)
				# mean, sum etc... --- works !!!  ----
			-> Conversions
			# -1- # Vect. with numbers => Vect. with Factors
			-------------------------------------------------
				blah
				blah.factor<-as.factor(blah)
				blah.factor
				summary(blah.factor) 
				# the result is different form the numeric, 
				# is a vector with factors, not a numbers
				dim(blah.factor)	
				mean(blah.factor)
				# mean, sum etc... --- not working ---
			# -2- # Vect. with numbers => Numeric Vect.
			-------------------------------------------
				blah
				blah.numeric1<-as.numeric(blah)
				blah.numeric1
				summary(blah.numeric1)
				# as with blam vector
				sum(blah.numeric1)  
				mean(blah.numeric1)
				# mean, sum etc... --- works !!! ---
			# -3- # V. with char, as charakter into numeric  - RISKY
			-----------------------------------------------			
				blah
				blah.numeric2<-as.numeric(as.character(blah))		
				blah.numeric2
				# looks the same sa blah.numeric1				
				summary(blah.numeric2)
				sum(blah.numeric2)
				mean(blah.numeric2)
				# mean, sum etc... --- works !!! ---
			# AND the DANGER is here !!!!!
			-----------------------------
				blah.extra<-as.numeric(blah.factor)
				blah.extra
				# here I took only the levels !!!!!!
				# not the values 				!!!!!!
		












	> 4.2 matrix (mx)																MATRIX
	---------------------------------------------------------------------------------------
	#######################################################################################	 							  
			
			
			
			
			  			  [,1] [,2] [,3] [,4]																							  
			#		[1,]    3    1    1    1
			#		[2,]    1    3    1    1		
			#		[3,]    1    1    3    1	
			#		[4,]    1    1    1    3
			
			
					!!!! --  [ROW,COLUMN] -- !!!!															
											 !!!! --  [ROW,COLUMN] -- !!!!									
					!!!! --  [ROW,COLUMN] -- !!!!															
        									 !!!! --  [ROW,COLUMN] -- !!!!









		>> Characteristics:
		-----------------------------------
        # one type of data !
		# it is just a twisted vector or many added vectors
		
		
		>> Creating a matrix:
		-----------------------------------
		# manual build matrix
			 m<-matrix(1:10, ncol=2)
			  	# filled naturally by COLUMN
			m<- matrix(1:10, nrow=2, byrow=TRUE)
			m
			dim(m) 
		# by adding vectors:
			m<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5)), nrow=30, ncol=3)
			
			
			# with NAs
			cc<-c(NA,1,2)
			m2<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5), rep(cc,10)), nrow=30, ncol=4)
			m2
			
		
			
		# colnames
			colnames(m) <- c('method1', 'method2', 'method3')
			head(m) 
			m
			
		    dim(xmat)     # dimensions (rows & columns) of a matrix
		 ncol(xmat)    # number of columns in matrix
          nrow(xmat)    # number of rows
          t(xmat)       # transpose a matrix
			
			
			
		>> Joining the matrices
		-----------------------------------
			rbind(m1,m2)
				#by ROW
			cbind(m1,m2)
				#by COLUMN


        >> Selective access:
        ---------------------------
            # by row and by col:
                m1[1,]
                m1[,1]
            # remove one columnt
                m1[-1,]
                m1
                m1[,-1]
                #removing one row [-1,] or a column[,-1]
                # [-2,] - the second row will be removed
                m1
		
		
		>>removing NA
		--------------------------------------------------------
			# matrix with NA:
				cc<-c(NA,1,2)
				m2<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5), rep(cc,10)), nrow=30, ncol=4)
				m2
			
			
			>>> with little control over row/columns set up!!
			------------------------------------------------- 
				
				complete.cases
				--------------
				m3<- matrix(m2[complete.cases(m2),])
				m3
					# it is a VECTOR now !!!!
					# stange output - this is no more matrix
				
				TRUE / FALSE 
				------------
				# Find NA
					m2
					row.has.na <- apply(m2,1,function(x){any(is.na(x))})
					row.has.na
				# see how many they are
					sum(row.has.na)			
				# remove them :
					m2_filtered <- m2[!row.has.na]
					m2_filtered
					dim(m2_filtered) 
					# it is a VECTOR now !!!!
					
					
			>>> with MORE CONTROL over row/columns set up!!
			------------------------------------------------- 
				
				library(functional)
				-------------------
				# only when working with numbers:
					m2[apply(m2, 1, Compose(is.finite, all)),]
					m3 <- m2[apply(m2, 1, Compose(is.finite, all)),]
					m3
					ls()
					# Compose(is.finite, all) is equivalent to function(x) all(is.finite(x))
				# or
				# also only for numbers
				# but i am sure that the structure is ok
					m2[apply(m2, 1, Compose(is.finite, all)), , drop=FALSE]
				
			
				# put 0 ZERO intead of NA
					# this doesnt work but it is a right direction:
					m4 <- m2[!is.finite(m2)] <- 0
				
				
				m2[complete.cases(m2 * 0), , drop=FALSE]
				m2[complete.cases(m2),]
			
			
			
				snp_matrix_filtered<-snp_matrix(complete.cases(snp_matrix * 0), , drop=FALSE)
				snp_matrix(complete.cases(snp_matrix), , drop=FALSE)
				
				head(snp_matrix)
				head(snp_matrix_filtered)

            >>> Count NA
            ------------------------------------------------------------

                cc<-c(NA,1,2)
                m2<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5), rep(cc,10)), nrow=30, ncol=4)
                m2

                apply(m2,2,function(x){sum(is.na(x))})







		>> Elements modiffication
		----------------------------
		m1[1,]<-NA
    		# to chnage all the elemnts in row 1 [1,] to NA :):)
   			# in data frame we can just call for the column with the
    		# header data_frame$category[1:20]<-what_I want _to _do
   			# and it can be order using more than one variable
		m1*m2
		m1 %*% t(m2)
		t(m1) %*% (m2)
    		# t == transpose
    		# i dont know?



		>>SOME NICE THINGS
		---------------------------
		# A nice matrix
			m<-matrix(c(3,rep(c(rep(1,4),3),3)),nrow=4)
			#gives 	
  			#			 [,1] [,2] [,3] [,4]
			#		[1,]    3    1    1    1
			#		[2,]    1    3    1    1
			#		[3,]    1    1    3    1
			#		[4,]    1    1    1    3
			#
		# Solving a calculation with Matrix 
 			#	  2x + 3y - z = 4
    		#	  5x - 10y + 2z = 0
    		#	  x + y - 4z = 5
			# you have to		
				M1<-matrix(c(2,5,1,3,-10,1,-1,2,-4),nrow=3)
				v<-c(4,0,5)
				sol<-solve(M1,v)
				sol
				?solve














	> 4.3 data Frame (df)														DATA FRAME								
	---------------------------------------------------------------------------------------								
	#######################################################################################	 


							H	.	.	.	F
							e	T	.	D	r
							l	h	I	a	a
							l	i	s	t	m
							o	s	.	a	e
							w	.	.	.	.
						 	.  .	.	.	.
			#		[1,]    na  na  na  na  0
			#		[2,]    na  na  na  na  0
			#		[3,]    na  na  na  na  0
			#		[4,]    na  na  na  na  0
		
		
		
		
		
		
		
		
		>> Characteristic
		---------------------------------
		# different types of data !
		# the same lenght! 
		# header line :)
		# working on data frame is safer because you call for data string by name and there is no danger that you 
		# - would have any other organization of data(look especially for True/False)
		
		>> examples:
		----------------------------------
			>>> A)
			------------------------------
			df <- data.frame(
  			 patientID = c("001", "002", "003"), 
   			 treatment = c("drug", "placebo", "drug"),
   			 age = c(20, 30, 24)
 			 )
 			df
 			# subset  
 		 	?subset
 		 	df
 			subset(df, treatment=="drug")
			drug<-subset(df, treatment=="drug")
			drug
				# original positions are kept, but do not work when evoke in a command
					dim(drug)
					drug
					drug[1,]
			>>> B)
			------------------------------
			a<-1:12
			b<-12:1
			cc<-letters[1:12]
			d<-rep(c(T,F),each=6)
			dataf<-data.frame(rbind(a,b,cc,d))
			dataf
			dataff<-data.frame(cbind(a,b,cc,d))
			dataff
				# it doenst matter how you join it because Vectors Have NO DIM !!!!!
			summary(dataf)
			str(dataf)

		>> Selective access
		-----------------------------------
			dataff
			dim(dataff)
			dataff[1,]
				# 1st rwo
			dataff[,1]
				# 1st column
			dataff[1,2:4]
				# 1st row, elemnts only from columns 2 to 4
				# AND easier than in matrix :
			dataff$a
			dataff$b

		>>True/ False for elements
		------------------------------------
			dataff
			dataff[1,]
			(dataff[1,])==1
				#
				# can be use to select elements which we like to see
			dataff
			dataff$d
			dataff$a[dataff$d=="TRUE"]
				# all elemnts from a col with TRUE in d columnt :)
	
	
		>> REMOVE NA
		------------------------------------
			library(Hmisc) 
		  ?na.delete 












	> Lists (lt)																   	   LIST
	---------------------------------------------------------------------------------------
	#######################################################################################
	
	
	
		
		list blablablableblaeee
	
			[1] WHAEVER 1		
			1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19
																											
			[2] WHAEVER 2	
			#		[1,]    na  na  na  na  0
			#		[2,]    na  na  na  na  0
			#		[3,]    na  na  na  na  0
			#		[4,]    na  na  na  na  0
		
			[3] WHAEVER 3		
			a, b, c, d, e, f, g, h, i, j, k, l, m, n, o ,p
	
	
	
	
	
	
	
	
	
		>> Features:
 		-----------------------------------------------------------------------------------
		# in a list you can OTHER OBJECTS
			# vectors
			# matric
			# data.frame
			# and even list inside the list
		# different types of data !
		# different length !
 		
 		>>example:
 		------------------------------------------------------------------------------------
 			my.list <- list(
   			fruits = c("oranges", "bananas", "apples"), 
   			mat = matrix(1:10, nrow=2)
 			)
 			my.list
		
			test<-list("first_element"=a, "second_element"="cou", "third_element"=c(1:10))
			test
		
		>> selective access
		------------------------------------------------------------------------------------
			# One object:
				my.list[[1]]
				my.list[[2]]
				my.list$mat
				my.list$mat[1,]
			# More than one object
				my.list[1:2]








########################################################################################## 222222
------------------------------------------------------------------------------------------		
5. sequnce of numbers                                     11111111111			44444444444444444444
------------------------------------------------------------------------------------------		
######################################################################################	8888888888
														777777777777777777777777777777777777777
																								999
	#- Commands
		- rep 
		- seq 
		- sort 
		- order 
		- rank
	rep(1,10)
		# gives 1 1 1 1 1 1 1 1
	rep(1:3,3)
		# gives 123 123 123
	seq(1,22,0.5)
		# gives 1, 1.5 2 2.5 ...
		# generate a sequence from "a" to "b" (seq(a,b,c)) in INTERVALS "c"
	a<-c(rep(seq(1,22,0.5),2))
	a
	b<-sort(a)
	b
	c<-order(a)
	c
		#be careful !
	d<-rank(a)
	d
		# - RANK EXAMPLE:
	aa <- c(4.1, 3.2, 6.1, 3.1)
	aa
	bb <-rank(aa)
	bb
	plot(aa,rank((aa)/length(aa)))
	#or
	plot(aa,bb/length(aa))
	plot(aa,bb)
		# different description on my plot axis
		#nice plot of elemnts from "aa"
		# assigned accodring to its rank
	length(aa)
		#the lengh of a vector "a"
		# when i divided rank by length i got relative rank value with max = 1








##########################################################################################							
------------------------------------------------------------------------------------------							
6. Data explorring and transformation																						
------------------------------------------------------------------------------------------								
##########################################################################################									

- edit
- fix
- reshape



	> edit	
	---------------------------------------------------------------------------------------
		new_file <- edit(old_file)
			#safe mode, new copy, with chnages
	
	> fix
	---------------------------------------------------------------------------------------
		fix(old_file)
			#changes directly into old_file
		fix(a)
			#after just go uot and safe


 	> Playground - my own table with geneexpression values:
 	---------------------------------------------------------------------------------------
		setwd("/Users/prosikie/Desktop/R_TRAINING")
			# temporarly
		data<-read.csv("NHIS 2007 data.csv",header=T)
		data$BMI <- round(data$BMI, digits=3)
			# nothing really happens
		data
		?round
		pivot
		head(data, 3)
		class(data)
			# unfortunatelly my data.frame is already rehaped in  the way i wish
			# so the next clas is not aplieable
	
	> reshape	
	---------------------------------------------------------------------------------------
		install.packages("reshape")
		library("reshape")
		head((pivot <- cast(pivot, gene ~ condition)), 2)
			#
			# so this is for:
 			# it is a reorganization i.e. 
			# I had a table where I had 
				gene     condition    response
				------------------------------
 				gene I	    a			up
				gene I	    b			up
				gene I	    c		   down
				...			...			...
				
			# and i want to have now this :
				gene      condition a     condition b    condition c
				----------------------------------------------------
				gene I       up				up				down    
				gene II		 down			up				...	
				...			...				...				...	
			# OR 
			# we can simply subset some data
			head(subset(pivot, cheetos>=0.2), 2)


	> for data transformation this site can be useful
	---------------------------------------------------------------------------------------
		http://had.co.nz





##########################################################################################
------------------------------------------------------------------------------------------
7. Subsetting data - very basic
------------------------------------------------------------------------------------------
##########################################################################################			
			
			
		>SQL (with "sqldf" pg)
		----------------------------------------------------------------------------------
			install.packages("sqldf")
				# many dependancies	
			library(sqldf)
			
			# example	
				setwd("/Users/prosikie/Desktop/R_TRAINING")
				data<-read.csv("NHIS 2007 data.csv",header=T)
				head(sqldf('SELECT * FROM data WHERE educ <= 14'), 10)
					# head is together with last standing number 10 !
				subset<-data.frame(sqldf('SELECT * FROM data WHERE educ <= 14'))
				head(subset)
				head(data)
				
				
			[SQL language ----------------------------------------]
				3rd generation language
				it is a language use for database
				make a quary to your database
				select a data in your database
				and extract them			
				sql can be use in r
				and applied for data.frame
				In R you dont need to build sql database ( which is
				normally required), R will do it for you.
				=> look at mp4 movie Performing SQL queries in R
				=>	in additional materials
			[--------------------------------------------------END]
			
				
		> doBy pg
		-----------------------------------------------------------------------------------
			# makes a summary commands for you
			# summary of my data done just oin one command
			# look at the help - many many fucnctions
			# even more complex function than in sql

			# Example
				library(doBy)
					help(package="doBy")
					?summaryBy
				source("http://www.r-statistics.com/wp-content/uploads/2012/01/source_https.r.txt")
					data(iris)
					iris
					Sepal.Width
				summaryBy(Sepal.Width + Petal.Width ~ Species, data=iris, FUN=c(mean))
			
			[IRIS dataset -------------------------------------------------------------]
			 	favourritte dataset for R bloggers
			 	github:
			 	source("http://www.r-statistics.com/wp-content/uploads/2012/01/source_https.r.txt")
				data(iris)
				and from html:
				"https://raw.github.com/talgalili/R-code-snippets/master/clustergram.r")
				data(iris)
			[IRIS dataset ----------------------------------------------------------END]






##########################################################################################
------------------------------------------------------------------------------------------			
8. RAM PROBLEM
------------------------------------------------------------------------------------------
##########################################################################################
																	
																		MEMMORY LIMIT !! 
																		ERROR !!!!!!!!
																	    MEMMORY LIMIT !! 
																		ERROR !!!!!!!!
	<<< when I reach the R limits >>>
	
	
	> Build a Data Base with:
	--------------------------------------------------------------------------------------		
		#languages:
			# such as MySQL
			# SQLite
		#Pg,s
			library("ff")
				http://cran.r-project.org/web/packages/ff/index.html
			library("bigmemory")
				http://cran.r-project.org/web/packages/bigmemory/index.html			


	> Use other programming language
	--------------------------------------------------------------------------------------		
		# PYTHON
			www.scipy.org/
				# many different entities
				# plauing with big datasets
				# Very Nice
		# RUBY
		# gsl  
		# gnuplot gems







##########################################################################################
------------------------------------------------------------------------------------------
9. Connecting to DataBase
------------------------------------------------------------------------------------------
##########################################################################################

	# very often the data are NOT as TEXT files
	# you need to write QSL query to extract the infromation from database
	# here we connect to MySQL DB
	# Example
		require("RMySQL")
 		con <- dbConnect(MySQL(), user="david", password="will_not_tell_you", 
 		dbname="db_name", host="mysql_server.stanford.edu")
 		results <- dbGetQuery(con, "SELECT * FROM pat_table LIMIT 5")
			# NOT working :):):)












##########################################################################################
------------------------------------------------------------------------------------------			
10. Importing raw Microarray data - cell file
------------------------------------------------------------------------------------------
##########################################################################################			
				
																		 ------------------
											CEL		CEL					|*...*...***..*...|
												CEL		CEL				|...*......*.*.*..|
													CEL		CEL			|....*..........**|
							GEO							CEL		CEL		|..***...**.*..**.|
								ArrayExpress				CEL			|...*......*..****|
																CEL		|.*....*..........|
																		|..*.*...***...*..|
																		|...*......*..**.*|
																		|...**..*....****.|
																		 ------------------
				
	> GEO database NCBI - CEL file
	--------------------------------------------------------------------------------------
	######################################################################################	
		
		# Before I start
			source("http://bioconductor.org/biocLite.R")
			biocLite()
			biocLite("affy")
			biocLite("GEOquery")
				# pg to make a query in GEO
			biocLite("mouse4302cdf")		
				# pg for mouse affy matrix 
	    	library(affy); library(GEOquery); library(mouse4302cdf)
	    # a query:
			getGEOSuppFiles("GSE12499")	
				# downl. a ZIP file to WORKING DIR
				# for getting GEO supplementary file
				# GSE - onli GEO identification number for your experriment
				# use in serching for dataset
				# works only with raw data
				# if not 
		# now my data are in a working directory
			getwd()
			dir()
		# unzip - a bit unclear
			system('tar -xf GSE12499/GSE12499_RAW.tar -C GSE12499/')
			system('rm GSE12499/*.CHP*; rm GSE12499/*.tar')
			dir()
		# we import the data
			da <- ReadAffy(celfile.path="./GSE12499/", compress=TRUE)
				# it is a directory what we are reading
				# Makeing a expression set - a beginning of all !!!
			da	
				# we have a set of 10 CEL files :)
		
		# NICE HEPL WITH R
			http://www.ncbi.nlm.nih.gov/geo/geo2r/
			# shows R script used to make a query and graphs
							
					
							
	
	> ArrayExpress EBI - CEL file
	--------------------------------------------------------------------------------------	
	######################################################################################
	
		# You serch a databse making a queries with a command lines
		# qery answer is downloaded into my R
		# I can do the same as in GEO
		# I need one package
			source("http://bioconductor.org/biocLite.R")
			biocLite()
			biocLite("ArrayExpress")
			library("ArrayExpress")
		# query
			 pneumoHS = queryAE(keywords = "pneumonia", species = "homo+sapiens")
			 pneumoHS[1:3, 1:3]

			movie 1 1h36-
					notes ~ 271 line


					[code chunk number 36: ArrayExpress1 (eval = FALSE) ---------------------------]

						pneumoHS = queryAE(keywords = "pneumonia", species = "homo+sapiens")
						pneumoHS[1:3, 1:3]
						
						# when I need already a processed data
						EGEOD1724 <- getAE("E-GEOD-1724", type='processed')
						cnames = getcolproc(EGEOD1724) # annotation
						EGEOD1724.da <- procset(EGEOD1724, cnames[2]) # build expression set
						EGEOD1724.da
						
					[-------------------------------------------------------------------------------]




##########################################################################################
------------------------------------------------------------------------------------------
11. Sliding window problem
------------------------------------------------------------------------------------------
##########################################################################################


	#>Zoo solution with line smooth
	-------------------------------------------------------------------------------------------

		library(zoo)


		#>> zoo - First way:
		#----------------------------------------------------------------------
		
			# Input Data
    		#------------------------------------------------------------------
    		mm<-c(rep(c(1,1,1,2,2,2,4,4,4,5,5,5,2,2,2,1,1,1,1,1,1,1,1,1),10))
   			mm
    		ml<-1:length(mm)  # just to have number 1 to 240 (the length of mm vector:)
			 ml
    		#------------------------------------------------------------------
			library(zoo)
		    k <- 10
    		slide<-c(rollapply(mm, 2*k-1, function(x) max(rollmean(x, k)), partial = TRUE))
    		slide
    		plot(rollmean(slide,10))
   			# or
    		library(zoo)
   			k <- 10
    		slide<-c(rollapply(mm, 2*k-1, function(x) max(rollmean(x, k)), partial = TRUE))
    		slide
			plot(ml,mm)
    		smooth = smooth.spline(ml,mm, spar=0.2)
    		plot(ml,mm)
			lines(smooth)										# here with smooth line :)
     
    
			# >> zoo - Second way - more elegant I think
			#----------------------------------------------------------------------
			
				# Input Data
    			#------------------------------------------------------------------
    			mm<-c(rep(c(1,1,1,2,2,2,4,4,4,5,5,5,2,2,2,1,1,1,1,1,1,1,1,1),10))
    			mm
    			#------------------------------------------------------------------

  				slide<-rollapply(mm, width = 10, by = 5, FUN = mean, align ="left")
    			slide
    			length(mm)
    			length(slide)
    			# the plot
    			plot(x,y, type="n", xlab="RAD_position",ylab="number of NA")



	#>TRR solution
	-------------------------------------------------------------------------------------------


			# TTR - sliding window
			# -------------------------------
			library(TTR)
				# Input Data
    			#------------------------------------------------------------------
    			mm<-c(rep(c(1,1,1,2,2,2,4,4,4,5,5,5,2,2,2,1,1,1,1,1,1,1,1,1),10))
    			mm
    			#------------------------------------------------------------------

				# TTR
				slide<-SMA(mm)
				plot(slide)
				
			# TTR has many commands giving different output
			# ------------------------------				

				par(mfrow=c(3,2))
				#-----------------
				slide<-SMA(mm,n=5)		# n=5	(there is no first 5 points on plot(NA))
				plot(slide)
				length(slide)
				slide<-SMA(mm,n=10)
				plot(slide)
				length(slide)
				slide<-SMA(mm,n=40)		# n=40 (there is no first 40 points on plot(NA))				
				plot(slide)
				length(slide)
				slide<-EMA(mm,n=5)
				plot(slide)
				length(slide)
				slide<-WMA(mm,n=5)
				plot(slide)
				length(slide)
				slide<-VWAP(mm,n=5)
				plot(slide)
				length(slide)



	#> Manual solution
	-----------------------------------------------------------------------------------------

    		((c(x,0,0) + c(0,x,0) + c(0,0,x))/3)[3:(length(x)-1)]
    		# or
    		(c(0,0,x)+c(0,x,0)+c(x,0,0))[1:(length(x)-3)*2+1]/3


















######################################################################
#########################################################################################
#################################################################################################################
###																											   IF
## ---------   -3- PROGRAMMING IN R
###																										   IFELSE
#################################################################################################################
#########################################################################################
######################################################################
			 -3-
			 -3-
			 -3-
		  *|||||||*
		   *|||||*
			*|||*
			 *|*
			  *
---------------------------------------------------
 1. IF ELSE (ifelse)
 2a. FOR loops (for do end for)
 2b. "apply" family - basic introduction
 3. While
 4. Assigments
 5. Efficient programming in R
 6. function
-----------------------------------------------------

##########################################################################################
------------------------------------------------------------------------------------------			
1. IF ELSE (ifelse)
------------------------------------------------------------------------------------------	
##########################################################################################

	> Example
	
		# some element
			i <- 1
			i <- 2
			
		# if loop
			if(i == 1){
  				print("i is equal 1")
				} else{
				print("i is NOT equal to 1")
			}

		# Shortcut Version
			ifelse(i == 1, "i is equal 1", "i is NOT equal to 1")
			



##########################################################################################
------------------------------------------------------------------------------------------			
2. FOR loops (for do end for)
------------------------------------------------------------------------------------------				
##########################################################################################
	
	> Function
		# to repeat our operation
		# simple in R
		# Explenation
		
			for i=1 -> 5 do
				doing 1
				doing 2
				doing 3
				doing 4
				doing 5					
			end for
			
		# you make it:
			for(i in 1:5){
			+	# do something
			+	print(i)	
			+}


##########################################################################################
------------------------------------------------------------------------------------------			
2B. "apply" family
------------------------------------------------------------------------------------------
##########################################################################################
				
	> apply is a "for" type loop
		# simpler
		# example
		
			 # matrix mat
			 	mat<-matrix(1:10,nrow=2, byrow=T)
		 		mat
		 		
			# SUMMING THE COLUMNS
				apply(mat, 2, sum)
				# or
				colSums(mat)
				
			# SUMMING THE ROWS
				apply(mat, 1, sum)
				# or
				rowSums(mat)
					
				
##########################################################################################
------------------------------------------------------------------------------------------			
3. While
------------------------------------------------------------------------------------------
##########################################################################################
				
	na
	na
	na
	na			
				
				
##########################################################################################
------------------------------------------------------------------------------------------			
4. Assigments
------------------------------------------------------------------------------------------
##########################################################################################				
	na
	na
	na
	na
				
				
				
##########################################################################################
------------------------------------------------------------------------------------------			
5. Efficient programming in R
------------------------------------------------------------------------------------------
##########################################################################################
				
	
	> Use many Cores in laptop
	--------------------------------------------------------------------------------------
	
		# foreach pg
		------------
		
			# I need:
				install.packages('doMC')
			
				library(foreach)
				library(doMC)
				
				
			# how many cores I have
				ncore = multicore:::detectCores()
				ncore
					# wow I have 8 !!!!!!
					
			# regiter number of avaibale cores for my work
				registerDoMC(cores = ncore)
				
			# for loop for dispaching a work among my cores	
				results <- foreach(i = 1:5, .combine=c) %dopar% {
				i+i
				}
				results							
		# multicore pg
		--------------	
					
			# I need:
				install.packages('rbenchmark')
			
				library(multicore)
				library(rbenchmark)
				
			# example
				# set of data:
					n <- rep(100, 100)
				
					benchmark(
    					x <- mclapply(n, rnorm, mc.cores=ncore),
    					x <- lapply(n, rnorm),
    					columns = c("test", "replications", "elapsed", "relative"),
   				 		order = "relative",
   				 		replications = 20
						)
						
			# when to use
				# multiple t-tets
				# linear regressions




##########################################################################################
------------------------------------------------------------------------------------------			
6. function
------------------------------------------------------------------------------------------				
##########################################################################################
 
 
 
 	> Example - basic:
 	---------------------------------------------------------------------------------------
 	#######################################################################################
	
 		# a function whichi is calcylating a distance between two points in a space
 		# euclidian distance	
 
		Mr.Euclide <- function(x, y){
					  dist <- sqrt(sum((x - y)^2))
					  return(dist)
						}
			# function (x, y)		- two arguments
			# dist <- 				- a vectore where I store my temp. results
 			# sqrt(sum((x-y)^2))	- my taks, equason
			# return(dist)			- return what i want
		
		# two points
			x <- c(1, 1)
			y <- c(2, 2)
		# run
			Mr.Euclide(x, y)
		# to see
			Mr.Euclide
		
		
	> S3 and S4 system - oriented programming (OOP) 
	---------------------------------------------------------------------------------------
	#######################################################################################
	
		# When i want to put something
		# so when someone want to run a function 
		# it checkes whether we have what the function needs
		
		# "x" and "y" wont be any more a vectors
		# it will be my object
		# and we will define it (e.x. as numeric here)
		
		# HERE IS WHAT WE DO:
		
			# 1. setting the object
				setClass("myObject", representation(vec = "numeric"), 
    					prototype = prototype(vec = 0))
    					
					# myObject							- FUNCTION NAME
					# representation(vec= "numeric")	- the object must be numeric
					# vec								- default argument = a name of it!
					# prototype 						- default value for vec
					# prototype(vec = 0)				- default value in my object is 0 !
						# why ?
			# 2. testing some object					
				(vectorA <- new("myObject", vec=c(1, 1, 1)))
				
					# new("", vec)				- it is how you make a new object
					# you cant store characters - it has to be numeric
					# 
				x<- new("myObject", vec=c(1,1,1))
 				x<- new("myObject", vec=c(1,1,1)))
		
			# Now we need to implement it in our function
				Mr.Euclide <- function(x, y){
    						if(class(x)!="myObject" & class(y)!="myObject") stop("error") 
    						dist <- sqrt(sum((x@vec - y@vec)^2))
    						return(dist)
							}
					# I use if loop
					# (x) and (y)							- two arguments to check
															- but here I will put names such as VectorA and VectorB
															- VectorA and VectorB will defined by my prevoius command
					# if(class(x)!="myObject"				- if the class of my object is not the same as in "myObject"
					# and class(y)! ="myObject"				- and the same
					# stop("error")							- stop everything and give error
					# if it is ....							- run the function and return dist
					# x@vec - y@vec							- @ is used
					#										- vec can't be acces by $ !!!!
					#										- we have only one slot whihc is call vec inside each obcject
					#										- if it would be multiple I woudl use $ !!!											
					
			# now we make two vectors
				vectorA <- new("myObject", vec=c(1, 1, 1))
				vectorB <- new("myObject", vec=c(2, 2, 2))	
			# and run it
				Mr.Euclide(vectorA, vectorB)
				
				
	> Pg for Euclidian distance 				
	---------------------------------------------------------------------------------------
	#######################################################################################
		# to cross check what we have done:
		
			install.packages("bioDist")
			library("bioDist")







######################################################################
#########################################################################################
#################################################################################################################
###																											APPLY
## ---------   -4- APPLY FAMILY
###																											APPLY
#################################################################################################################
#########################################################################################
######################################################################


 0. Playground
 1. apply
 2. when to use sapply or lapply?
 3. Optional argumens



##########################################################################################
------------------------------------------------------------------------------------------
0. Playground
------------------------------------------------------------------------------------------
##########################################################################################
	
		> Playground "m"
		-------------------	
			# to experriment with apply family I will create 3 data sets in a matrix "m"
			# each with normal distridution (sd+-1), and mean values 0, 2 and 5
			m<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5)), nrow=30, ncol=3)
			m
			# rnorm(30,0) - 30 randome numbers, heaving normal distrib, and mean = 0
			m[,1]
			mean(m[,1])
			mean(m[,2])
			mean(m[,3])
			plot(m[,1])
			hist(m[,1])		
			
			
			
			
			
#######################################################################################--##--##--##--##
------------------------------------------------------------------------------------------------------#
1. APPLY
------------------------------------------------------------------------------------------------------#		
#######################################################################################--##--##--##--##
	
	> basic use:
	------------------------------------------------------
	- we use when we have some structured blob of data :)
	- here in some sort of matrix
	- the operation can be
		- transformation
		- informational - getting some info as means, sum etc...
		- subsetting etc...
	
		
	> Be carefull with 
	------------------------------------------------------
	!! BETTER work on MATRIX , not on data frame !!
	!! all the DATA must be of the SAME TYPE	 !!
	!! if not the conversion will make a mess	 !!
	
	
	> ROOLs
	------------------------------------------------------
		>> Apply goes BY ROW
		>> Data needs a name
		>> The same type of data in the matrix !
		>> better use matrix
		
	
	> Apply work with rows and columns	
	------------------------------------------------------
		apply goes by ROW wise or COLUMN wise !
		[by row]
			apply(m, 1, mean)
		[by col]
			apply(m, 2, mean)


	> Subset of data needs a name or must be specify
	------------------------------------------------------
		i.e. 
		[make a subset of data (like using function((x)) ]
		or
		[create a function or a list before and give it to apply]
	
	
		apply(m,2, function(x) length(x[x<0])
						|		|
						|		NO COMA !!	
						|
						substracting all the values to x (function(x))
						here one column
						and than giving this (x) to length(x) but only when x<0
		
		Can be also:
			apply(m,2,function(x) mean(x[x>0]))
			apply(m, 2, function(y) is.matrix(y))	
				to chech whether it is a matrix (it isnt)
			apply(m, 2, function(aaa) is.vector(aaa))		
		
		
		
#######################################################################################--##--##--##--##
------------------------------------------------------------------------------------------------------#
2. when to use sapply or lapply
------------------------------------------------------------------------------------------------------#		
#######################################################################################--##--##--##--##		

		{they do:}
			traverse thrue the set of data
			use lists or vectors
		{the difference is }
			sapply	- return a vector
			lapply	- return a list
		{e.g}
		
			-- VECTOR:
			sapply(1:3, function(x) x^2)
			l<-c(1:3)
			sapply(l, function(x) (x+2)^3)
		
			--LIST:		
			lapply(l, function(x) x^2)
			
			-- WE CAN:
			-- VECTOR to LIST // LIST to VECTOR\
			simplify=F
			into list:
			sapply(l,function(x) x^2, simplify=F)	
											|
											make a list from my vector
			unlist
			into vector:
			unlist(lapply(l, function(x) x*8))	
	
	
#######################################################################################--##--##--##--##
------------------------------------------------------------------------------------------------------#
3. Optional argumens
------------------------------------------------------------------------------------------------------#		
#######################################################################################--##--##--##--##

		{function(x)}
			x is whatever apply is curretly doing
			however sometimes is not enought
			e.g. in matrix m we have 3 columns
				if we are interested only in 1st and 3rd column we need to play a bit
				and give some additional info
				such as that these numbers are from matrix m
				and apply will use it as it goes thrue column or rows 
		{e.g}
			dirty way:
			sapply(1:3, function(x) mean(m[,x]))
			
			nice way:
			sapply(1:3, function(x, y) mean(y[,x]), y=m)
			l<-c(1:3)
			l
			ll<-as.factor(l)
			ll
			sapply(ll,funxtion(x, y) mean(y[,x]), y=m)
		
		
		
		
		
		
		
		
		
		
		
######################################################################
#########################################################################################
#################################################################################################################
###																											   
## --------- -5- REGULAR EXPRESSIONS in R
###																										   
#################################################################################################################
#########################################################################################
######################################################################
			 -5-
			 -5-
			 -5-
		  *|||||||*
		   *|||||*
			*|||*
			 *|*
			  *
---------------------------------------------------
 1. Basic differencess	
 2. grep,		 grepl
 3. regeexpr,	 gregexpr,
 4. sub, 		 gsub
 5.	regexec
-----------------------------------------------------


##########################################################################################
------------------------------------------------------------------------------------------			
0. Examples to be use in point 5
------------------------------------------------------------------------------------------				
##########################################################################################
 	# matrix with NA:
		cc<-c(NA,1,2)
		m2<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5), rep(cc,10)), nrow=30, ncol=4)
		m2
		
	# NIHT data.frame 
		setwd("/Users/prosikie/Desktop/R_examples")
		dir()
		nhis<-read.csv("NHIS 2007 data.csv",header=T)
		head(nhis)
		
	# iris
		source("http://www.r-statistics.com/wp-content/uploads/2012/01/source_https.r.txt")
		data(iris)
		head(iris)
		class(iris)
			#data.frame
		
	# list_test
		aa<-letters[1:30]
		aa
		list_test<-list("first_element"=aa, "second_element"="cou", "third_element"=c(1:10))	
		list_test
		
			
##########################################################################################
------------------------------------------------------------------------------------------			
1. Basic differencess
------------------------------------------------------------------------------------------				
##########################################################################################			
 
 
 1. grep / grepl		- FOR 	-> mach with pattern/expression
 	------------	 	-  IN 	-> character vector
 						- Return:
 							- indices which match to pattern (grep) 
 							- string which match 
 							- TRUE/False vector (grepl)
 							 
 2. regeexpr/gregexpr	- FOR 	-> regular expressions 
 	-----------------	-  IN 	-> character vectors
 						- Return:
 							- indices of a string where the match begins and
 							the LENGH of the match


 3. sub / gsub			- FOR	-> regular expressions 
	---------- 			- IN	-> character vector
 						- DO:	
 							- Replace match with another string
 								  		
 4.	regexec				- difficult to say
 	-------
 


##########################################################################################
------------------------------------------------------------------------------------------			
2. GREP, GREPL -------  grep, grepl
------------------------------------------------------------------------------------------				
##########################################################################################	
	
	> my elemnts
		m2
		test_list
		iris
		nhis
	> grep
		?grep
		aaa<-m2[,4]
		aaa
		grepl(1,aaa)
		
		ddd<-c(grep(1,aaa))
		ddd
		bbb<-m2[ddd,]
		bbb
		
		grepl("NA",aaa)
		
		is.na(aaa)

		aa
		long_mat<-matrix(c(rep(aa,5)),nrow=25)
		long_mat
		colnames(long_mat) <-c("one","two","three","four","five","six")
		colnames(long_mat)
		names<-c(colnames(long_mat))
		names
		one<-c(grep("one",names))
		long_mat[,one]
		is.na(long)
			
			

		aa
		bb<-grep("NA",aa)	
		bb
		is.na(aa)

		grep(NA,aa)
		aaa
		
		sum(aaa=="na")
		
		cc<-c()


		NA_positions <- c(apply(MOJ_Obiekt,1,function(x){any(is.na(x))}))
		NApositions
		NApositions[NApositions==FALSE]
	
	
	
	
		
######################################################################
#########################################################################################
#################################################################################################################
###																											   
## ------- 6 Graphic in R  
###																										   
#################################################################################################################
#########################################################################################
######################################################################


##########################################################################################
------------------------------------------------------------------------------------------			
1. mfrow, par
------------------------------------------------------------------------------------------				
##########################################################################################

	par(mfrow=c(1,1))
#		  		| |
#				| COLUMNS
#				ROWS
			
			
			
				
			


























######################################################################
#########################################################################################
#################################################################################################################
###																											   
## ------- 7 RScripts  
###																										   
#################################################################################################################
#########################################################################################
######################################################################




##########################################################################################
------------------------------------------------------------------------------------------			
1. Run R.script form UNIX command line
------------------------------------------------------------------------------------------				
##########################################################################################

R CMD BATCH --vanilla  script.R
	# vanilla option blocks to load saved R sessions
	# very important !!!!
	
	
	
	
	
	
	
	
	
	
##########################################################################################
------------------------------------------------------------------------------------------			
2. text, table to pdf, graphic :)
------------------------------------------------------------------------------------------				
##########################################################################################

# look at the pg:
	PerformanceAnalytics
		?textplot
# grid.table in pg gridExtra
# addtable2plot function in pg plotrix

# textplot function in gplots





##########################################################################################
------------------------------------------------------------------------------------------			
3. Give the same names to all your output files 
------------------------------------------------------------------------------------------				
##########################################################################################

	> 















######################################################################
#########################################################################################
#################################################################################################################
###																											   
## ------- -LAST-     Examples used to learn R  
###																										   
#################################################################################################################
#########################################################################################
######################################################################
			 -l-
			 -l-
			 -l-
		  *|||||||*
		   *|||||*
			*|||*
			 *|*
			  *

#### [Vector]
#### ---------------------------------------------
	
	# (1)
	blah<-c("1","2","6","5")
	
	# (2)
	x<-c(1,2,3,4)
	x = c(1, 2, 3, 4) ; 
	x = 1:4
	
	# (3)
	x <-c(rnorm(1000,5))
	
	# (4)
	a<-c(rep(seq(1,22,0.5),2))


#### [Matrix]
#### -----------------------------------------------
	
	# (1)
	m1<-matrix(1:12,nrow=3)
 	
 	# (2)
 	mat<-matrix(1:10,nrow=2, byrow=T)
 	mat
 
 	# (3)
	m<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5)), nrow=30, ncol=3)
	colnames(m) <- c('method1', 'method2', 'method3')

	# (4)
	# matrix with NA:
	cc<-c(NA,1,2)
	m2<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5), rep(cc,10)), nrow=30, ncol=4)
	m2

	# (5)
	# long_mat with NAs
	aa<-letters[1:30]
	long_mat<-matrix(c(rep(aa,5)),nrow=25)
	long_mat
	colnames(long_mat) <-c("one","two","three","four","five","six")





#### [Data Frame]
#### ----------------------------------------------

	# (1)	
	#data_frame
		a<-1:12
		b<-12:1
		cc<-letters[1:12]
		d<-rep(c(T,F),each=6)
		data_frame<-data.frame(rbind(a,b,cc,d))
	
	# (2)
	#NHIS 2007 data.csv
		setwd("/Users/prosikie/Desktop/R_TRAINING")
		data<-read.csv("NHIS 2007 data.csv",header=T)


#### [List]
#### -------------------------------------------------


	# (1)
	list_test<-list("first_element"=a, "second_element"="cou", "third_element"=c(1:10))


	# (2)
	my.list <- list(
   			fruits = c("oranges", "bananas", "apples"), 
   			mat = matrix(1:10, nrow=2)
 			)


#### [Specific datasets]
-------------------------------------------------------


			[IRIS dataset -------------------------------------------------------------]
			 	favourritte dataset for R bloggers
			 	github:
			 	source("http://www.r-statistics.com/wp-content/uploads/2012/01/source_https.r.txt")
				data(iris)
				and from html:
				"https://raw.github.com/talgalili/R-code-snippets/master/clustergram.r")
				data(iris)
			[IRIS dataset ----------------------------------------------------------END]













#########################################################################################
#########################################################################################
#########################################################################################
###				   		###
###   --- Stanford --- 	###
###      University     ###
###       R course      ###
###				   		###
#########################################################################################
#########################################################################################
#########################################################################################




 				----------------- <<<< DAY 1 >>>> ---------------------- 
 
------------------------------------------------------------------------------------------
Basic info:
------------------------------------------------------------------------------------------

Before you start StC

install.packages("xlsx")
	# many dependancies
install.packages("foreign")
install.packages("foreach")
install.packages("multicore")
install.packages("XML")
install.packages("googleVis")
install.packages("reshape")
	# many dependancies
#And
library("xlsx")
library("foreign")
library("foreach")
	#interesting info:
	#foreach: simple, scalable parallel programming from Revolution Analytics
	#Use Revolution R for scalability, fault tolerance and more.
	#http://www.revolutionanalytics.com
library("multicore")
library("XML")
library("googleVis")
	# it will use my standard browser as output !
library ("reshape")
library("ggplot2")
# AND my Dependacies:
library("plyr")
library("rJava")
library("xlsxjars")
.packages()

# IN Addition
# I have all the code provided by the lecturer in my folder R_examples
# as Stanford_R_Course_Day1



------------------------------------------------------------------------------------------
R studio - description
------------------------------------------------------------------------------------------

	# RStudio
	www.rstudio.org

------------------------------------------------------------------------------------------
Some usefull sites:
------------------------------------------------------------------------------------------

R on Amazon EC2
	# in shell command line
	# there is a bioconductor immage
	# bioconductor immage
	
Ron EBI
	http://www.ebi.ac.uk/Tools/rcloud/
	# they are providing you acces to huge amount of computing power for free
	# packages are preinstalled !!!!


<<<<<<<<< HOMEWORK DAY 1 >>>>>>>>>>>>>

------------------------------------
R classes - Stanford - 2014_02_21
day1
-------------------------------------

Task 1.
Make a fibonacci sequence 
long for 50 numbers
it is 1,1,2,3,5,8,13,21,etc...

	F[i] = F[1-1] + F[i-2]				
				
Task 2.
Make it using  multicore
-------------------------------------	
<<<<<<<<<<<<<<< --- >>>>>>>>>>>>>>>>>










#########################################################################################
#########################################################################################
#########################################################################################
###
### R COURSE - LAUSANNE
###
#########################################################################################
#########################################################################################
#########################################################################################



---------------------
###               ###
### -  Example  - #################################################################
### -   File    - ###
###               ###
---------------------
# - NHIS 2007 data.csv from online course in youtube
# - it is in a folder R_examples together with my movies
# - Elements
	A. Data frame dowload and structure
	B. Selective access to elemts in my data frame:
	

A. Data frame dowload and structure
-----------------------------------
setwd("/Users/prosikie/Desktop/R_TRAINING")
	# temporarly
data<-read.csv("NHIS 2007 data.csv",header=T)
head(data)
tail(data)
str(data)
summary(data)
data
attach(data)
detach(data)
HHX
dim(data)

B. Selective access to elemts in my data frame:
-----------------------------------------------
# - [ROW,COLUMN]
data[1,]
	# first row !
data[,1]
	# first column
	# and for more:
data[1:3,]
data[,1:3]
mean(data[,1])
sum(data[,1])
max(data[,1])
min(data[,1])
prod(data[,1])
	#gives a product from the multiplication of all the elements
	#e.x
print(prod(1:4)) 
print(1:10)
# - other type of a selective access
mean(data$HHX)
median(data$FMX)
# - and now
attach(data)
var(HHX)
sd(FMX)	


---------------------
###               ###
### -  Example  - #################################################################
### -   File    - ###
###               ###
---------------------



	[5.Density plots from our matrix]
		
		[5.1. names for columns in m matrix]
		
		m<-matrix(data=cbind(rnorm(30,0), rnorm(30,2), rnorm(30,5)), nrow=30, ncol=3)
		colnames(m) <- c('method1', 'method2', 'method3')
		head(m) 
		
		[5.2. we make a data.frame  --- as.data.frame --- ]
		df<- as.data.frame(m)
		df
		
		[5.3. one col for data and second for method --- stack --- ]
		dfstack<-stack(df)
		dfstack
			- values and ind columns only !!
		is.factor(dfstack[,2])
		
					--- unstack ---
					in case
					dfunstack<-unstack(dfstack)
					dfunstack
		
		[5.4. Density plot with ggplot ---  ]	
		
			{all data together}
				ggplot(dfstack, aes(x=values)) +geom_density()
				~ what it is:
				~ x is a stacked data frame (values)
				~ aes function chnage whatever, in ind as an expressable value (here i dont understand how???)
		
			{to group the data according to the method}
				ggplot(dfstack, aes(x=values)) +geom_density(aes(group=ind))
				
				~and with the colours
				ggplot(dfstack, aes(x=values)) +geom_density(aes(group=ind, colour=ind))
				
				~plus fill the region
				~alpha=0.3 -- trnasparency
				ggplot(dfstack, aes(x=values)) +geom_density(aes(group=ind, colous=ind, fill=ind), alpha=0.4)
				
			{what we get:}
			"x" - vaslues which are plot from our stacked data frame (df)
			"y" - values of an aes function















#########################################################################################
#########################################################################################
#####################################################
#########################
###
### --- R Topics:
###
#########################
#####################################################
#########################################################################################
#########################################################################################



#########################################################################################
1. PASS-by-VALUE




	[PASS-by-VALUE ---------------------------------------------------------]
		R is using PASS-BY-VALUE not pass by reference\
		> PASS-by-VALUE
			actions done on reference variable do not chnage this variable
			you need to chnage it or make any other variable to safe results 
			of your action!
		
		> Example
			x <- 1:10
			x
			x * 2
				# the value way not chnage in reference not by 
			x
			y <- x *2
			x * 2
			y
		> If i wish to use pass-by-reference
			look for packages
				"R.oo"
				"mutar"
				"proto"
		[PASS-by-VALUE ------------------------------------------------------ END]



#########################################################################################
