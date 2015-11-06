.PHONY: run map quicktest

run: data/weights.txt data/split_test.txt
	python evaluate.py data/weights.txt \
		data/split_test.txt .

data/mapped_out.txt: mapper.py data/split_train.txt
	head -n 5000 data/split_train.txt | python mapper.py > data/mapped_out.txt
	tail -n +5000 data/split_train.txt | python mapper.py >> data/mapped_out.txt

data/weights.txt: reducer.py data/mapped_out.txt
	python reducer.py < data/mapped_out.txt > data/weights.txt

# only for testing
map: data/training_sub.txt
	python mapper.py < data/training_sub.txt

quicktest: data/split_test.txt data/training_sub.txt
	python mapper.py < data/training_sub.txt \
		| python reducer.py \
		> data/weights_test.txt
	python evaluate.py data/weights_test.txt \
		data/split_test.txt .

data/training_sub.txt:
	head -n 10000 data/training.txt > data/training_sub.txt

data/split_train.txt:
	head -n 10000 data/training.txt > data/split_train.txt

data/split_test.txt:
	tail -n 10000 data/training.txt > data/split_test.txt
