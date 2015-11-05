.PHONY: run

run:
	python mapper.py < data/training.txt \
		| sort \
		| python reducer.py \
		> data/weights.txt
		python evaluate.py data/weights.txt \
			visual_test/visual_test_set.csv visual_test/target.csv .
