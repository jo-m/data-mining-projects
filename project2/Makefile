.PHONY: run map

run: data/weights.txt
	python evaluate.py data/weights.txt \
		visual_test/visual_test_set.csv visual_test/target.csv .

data/mapped_out.txt: mapper.py data/training.txt
	python mapper.py < data/training.txt | sort > data/mapped_out.txt

data/weights.txt: reducer.py data/mapped_out.txt
	python reducer.py < data/mapped_out.txt | tee data/weights.txt

# only for testing
map:
	python mapper.py < data/training.txt | head -n 50
