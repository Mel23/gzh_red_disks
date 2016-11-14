#!/bin/bash


for i in {0..7770}; do #terrible hardcode - have to know in advance how many files are in directory. 
	files=(V_files/*.fits)
	fname="${files[i]}"
	fname="${fname##*/}"
	fname="${fname%.fits*}" 
	#echo "SEx_output_V/$fname.cat"	
	/home/mel/sex ${files[$i]} -CATALOG_NAME="SEx_output_V/$fname.cat" 

done

