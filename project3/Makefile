.PHONY: test_map eval eval_sub run map

# just test the mapper for errors
test_map:
	head -n 100 data/train.txt | python mapper.py

# evaluate on full data set
eval: data/centers.txt data/train.txt
	python evaluate.py data/centers.txt data/train.txt

# eval on only a subset, because on full set needs > 1min
eval_sub: data/centers.txt
	head -n 3000 data/train.txt \
		> data/eval_sub.txt
	python evaluate.py data/centers.txt data/eval_sub.txt

# do map
data/for_reducer.txt: mapper.py
	# with n = 12500, we have exactly 8 jobs so we can use all our CPUs
	parallel --pipe -N12500 --blocksize 100M \
		python mapper.py \
		< data/train.txt \
		> data/for_reducer.txt

# do map
map: data/for_reducer.txt
	cat data/for_reducer.txt

# do reduce
data/centers.txt: data/for_reducer.txt reducer.py
	python reducer.py \
		< data/for_reducer.txt \
		> data/centers.txt

# do all
run: data/centers.txt
