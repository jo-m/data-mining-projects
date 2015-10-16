.PHONY: run map run_para

run: mapper.py reducer.py data/training.txt
	python mapper.py < data/training.txt \
		| sort \
		| python reducer.py > reported_duplicates
	python check.py reported_duplicates data/duplicates.txt

map: mapper.py data/training.txt
	python mapper.py < data/training.txt | sort > mapped_out.txt

run_para: mapper.py reducer.py data/training.txt
	parallel --pipe python mapper.py < data/training.txt \
		| sort \
		| python reducer.py > reported_duplicates
	python check.py reported_duplicates data/duplicates.txt

test:
	egrep '(0000149|0000186)' data/training.txt \
		| python mapper.py
	egrep '(0000827|0001108)' data/training.txt \
		| python mapper.py
	egrep '(0000594|0001036)' data/training.txt \
		| python mapper.py

max:
	python maxval.py < data/training.txt | sort -r | head -n 1
