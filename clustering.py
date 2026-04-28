from datasets import load_dataset
from collections import Counter
from itertools import product
import numpy as np
import pandas as pd

ds = load_dataset("tattabio/mopb_clustering")["train"]
# print(ds)
# print(ds[0])
# print(len(ds))

def count_kmers(sequence, k):
    # extract all kmers
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    # count frequencies
    kmer_counts = Counter(kmers)
    return dict(kmer_counts)

# all possible kmers of length 3 (4^3)
#alphabet = 'ACGT'
alphabet = "ACDEFGHIKLMNPQRSTVWY"
k = 3
all_kmers = [''.join(kmer) for kmer in product(alphabet, repeat=k)]

sequences = ds["Sequence"]
print(f"number of sequences: {len(sequences)}")

# encoding for all sequences
kmer_matrix = []
for seq in sequences:
    counts = count_kmers(seq, k)
    vector = [counts.get(kmer, 0) for kmer in all_kmers]
    kmer_matrix.append(vector)

kmer_matrix = np.array(kmer_matrix)
print(f"Kmer matrix dims: {kmer_matrix.shape}")

# save to CSV
df = pd.DataFrame(kmer_matrix, columns=all_kmers)
df.to_csv('kmer_matrix.csv', index=False)

#print(kmer_matrix[:5])

