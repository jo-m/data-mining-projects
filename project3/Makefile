.PHONY: test_map eval run

# evaluate on full data set
eval: data/centers.txt data/train.txt
	python evaluate.py data/centers.txt data/train.txt

# do map
# with n = 12500, we have exactly 8 jobs so we can use all our CPUs
data/for_reducer.txt: mapper.py
	parallel --pipe -N12500 --blocksize 100M \
		python mapper.py \
		< data/train.txt \
		> data/for_reducer.txt

# do reduce
data/centers.txt: data/for_reducer.txt reducer.py
	python reducer.py \
		< data/for_reducer.txt \
		> data/centers.txt

# do all
run: data/centers.txt
