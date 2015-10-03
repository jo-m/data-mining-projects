.PHONY: check run map

reported_duplicates: mapper.py reducer.py data/training.txt
	python mapper.py < data/training.txt \
		| sort \
		| head -n 10 \
		| python reducer.py

check: check.py reported_duplicates
	python check.py reported_duplicates data/duplicates.txt

run: reported_duplicates

map: mapper.py data/training.txt
	python mapper.py < data/training.txt
