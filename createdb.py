
# Generate a CSV file with 2 million users, connected according to the rules below
#
#connect each prime number P to 3 users (P+1,P+2,P+3)
## connect each (P+1 to P+7)
### connect each (P+7 to P+9, P+11)

#Hence we know for sure
#P has got a fof P+7
#P has got a fof2 P+9, P+11

# a bunch of more connections we can predict
# connect each mod 99 user U to U+2,U+3
# connect each U+2 to U+4,U+5 (fof)
# connect each U+3 to U+4,U+6 (fof, with a shared user)
# connect each U+4 to U+7 (fofof)

# for each user U, randomly connect it to 0..10 other users


from collections import defaultdict
import csv
import numpy
import random

#http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188
def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n/3 + (n%6==2), dtype=numpy.bool)
    for i in xrange(1,int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k/3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)/3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]

def getDict():

    MAXID = 2000000
    primes = primesfrom2to(MAXID)

    conns = defaultdict(set)

    for p in primes:
        if p + 11 > MAXID:
            # just ignore the last ones
            break

        conns[p].update([p +1, p+2, p+3])
        conns[p+1].update([p+7])
        conns[p+7].update([p+9, p+11])

    u=0
    while u < MAXID:

        if u % 99 == 0:
            if u + 7 > MAXID:
                # just ignore the last ones
                break

            conns[u].update([u+2, u+3])
            conns[u+2].update([u+4, u+5])
            conns[u+3].update([u+4, u+6])
            conns[u+4].update([u+7])

        how_many = random.randint(0, 10)

        connto = []
        while how_many > 0:
            rand_user = random.randrange(0, MAXID)
            how_many -= 1

            if rand_user == u:
                # don't connect to yourself
                continue

            connto.append( random.randrange(0, MAXID) )

        conns[u].update(connto)

        u += 1

    return conns


def dumpCsv(dictWithSets):
    with open('fullset.csv', 'w') as csvfile:
        fieldnames = ['user', 'friends']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for k,v in dictWithSets.iteritems():
            friends = ',' . join(map(str,v))
            writer.writerow({'user': k, 'friends': friends})



if __name__ == "__main__":

    dictWithSets = getDict()

    dumpCsv(dictWithSets)



