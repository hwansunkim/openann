for i in {0..9}
do
	python training.py file=full_data_signif_over_dt/ALL_S6_full_set_${i}_training.ann $1 $2 $3&	
done



