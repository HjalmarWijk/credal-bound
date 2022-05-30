#!/bin/bash
for i in {0..49}
do
	new_dir="ACmodels/model_${i}"
	echo $new_dir
	#mkdir $new_dir
	uai="vmodels/vmodel${i}.uai"
	#bash convert_uai.sh -o $new_dir -m constraints.txt -u $uai
	python bound.py -in $new_dir -u $uai -o "bound_data/model${i}.pickle"

done
