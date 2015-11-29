#/usr/bin/bash

run_eval() {
  rm -f data/centers.txt
  rm -f data/for_reducer.txt
  make run eval
  echo '--------------------------'
}

export mapper__n_clusters=80
run_eval

export mapper__n_clusters=100
run_eval

export mapper__n_clusters=120
run_eval

export mapper__n_clusters=150
run_eval

export mapper__n_clusters=200
run_eval
