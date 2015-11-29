#/usr/bin/bash

run_eval() {
  rm -f data/centers.txt
  rm -f data/for_reducer.txt
  time make run
  make eval
  echo '--------------------------'
}

export mapper__n_clusters=200; run_eval
export mapper__n_clusters=200; run_eval

export mapper__n_clusters=300; run_eval
export mapper__n_clusters=300; run_eval

export mapper__n_clusters=400; run_eval
export mapper__n_clusters=400; run_eval

export mapper__n_clusters=500; run_eval
