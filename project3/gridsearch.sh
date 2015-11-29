#/usr/bin/bash

run_eval() {
  rm -f data/centers.txt
  rm -f data/for_reducer.txt
  time make run
  make eval
  echo '--------------------------'
}

export mapper__n_clusters=500 mapper__n_init=10; run_eval
export mapper__n_clusters=500 mapper__n_init=10; run_eval
export mapper__n_clusters=500 mapper__n_init=15; run_eval
export mapper__n_clusters=500 mapper__n_init=15; run_eval
export mapper__n_clusters=600 mapper__n_init=10; run_eval
export mapper__n_clusters=600 mapper__n_init=10; run_eval
export mapper__n_clusters=600 mapper__n_init=15; run_eval
export mapper__n_clusters=600 mapper__n_init=15; run_eval
export mapper__n_clusters=800 mapper__n_init=10; run_eval
export mapper__n_clusters=800 mapper__n_init=10; run_eval
export mapper__n_clusters=800 mapper__n_init=15; run_eval
export mapper__n_clusters=800 mapper__n_init=15; run_eval
export mapper__n_clusters=1000 mapper__n_init=10; run_eval
export mapper__n_clusters=1000 mapper__n_init=10; run_eval
export mapper__n_clusters=1000 mapper__n_init=15; run_eval
export mapper__n_clusters=1000 mapper__n_init=15; run_eval
export mapper__n_clusters=1500 mapper__n_init=10; run_eval
export mapper__n_clusters=1500 mapper__n_init=10; run_eval
export mapper__n_clusters=1500 mapper__n_init=15; run_eval
export mapper__n_clusters=1500 mapper__n_init=15; run_eval
export mapper__n_clusters=2000 mapper__n_init=10; run_eval
export mapper__n_clusters=2000 mapper__n_init=10; run_eval
export mapper__n_clusters=2000 mapper__n_init=15; run_eval
export mapper__n_clusters=2000 mapper__n_init=15; run_eval
