from random import randint, seed
from bx.intervals.intersection import Intersecter, Interval

# the span of the generated intervals
SPAN = 10

# the size of the genome
SIZE = 5*10**4

# the number of intervals
N = 10**6

def generate(x):
    "Generates random interval over a size and span"
    lo = randint(10000, SIZE)
    hi = lo + randint(1, randint(1, 10**4))
    return (lo, hi)

def generate_point(x):
	lo = randint(10000, SIZE)
	return (lo, lo)

# use this to force both examples to generate the same data
seed(10)

# generate 10 thousand random intervals
data = map(generate, xrange(N))

# generate the intervals to query over
query = map(generate_point, xrange(1000))

# create the interval tree
tree = Intersecter()

# build an interval tree from the rest of the data
for start, end in data:
    tree.add_interval( Interval(start, end) )

# perform the query
for q, q in query:
    overlap = tree.find(q, q)
    out = [ (x.start, x.end) for x in overlap ]
    print '(%s) -> %s' % (q, out)