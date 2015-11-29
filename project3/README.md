# Large Scale K-Means
Data Mining - Project 3: <http://las.ethz.ch/courses/datamining-f15/>

**Warning:** the training and result data must not be checked into this repo (ETH Copyright).

For running locally, you need GNU parallel:

    brew install parallel

To run:

    make run eval

# Set up on Euler

    mkdir -p $HOME/python/lib64/python2.7/site-packages
    export PYTHONPATH=$HOME/python/lib64/python2.7/site-packages:$PYTHONPATH
    module load python/2.7
    python -m pip install sklearn numpy

## Running on Euler

    scp -r . euler:dm-project3
    ssh euler
    cd dm-project3
    export PYTHONPATH=$HOME/python/lib64/python2.7/site-packages:$PYTHONPATH
    module load python/2.7
    bsub -n 24 ./gridsearch.py
    bjobs
    bpeek
