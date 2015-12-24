"""
(C) Casey Greene.

This python script generates a number of different files that serve as
standards for NetWAS analysis from a GWAS. These files differ only in their
gene ordering to evaluate the effects of multiple cross validation intervals
on the results.
"""
import os

import pandas as pd
import numpy as np

np.random.seed(42)

# header on the first line, gene name in the second col
vegas_ad1 = pd.read_excel('data/vegas_adni1.xls', header=0)
vegas_ad2 = pd.read_excel('data/vegas_adni2.xls', header=0)

entrez_symbol = pd.read_csv('data/symbol_entrez.txt', sep='\t', header=None,
                            index_col=1)
symbol_entrez = pd.read_csv('data/symbol_entrez.txt', sep='\t', header=None,
                            index_col=0)

d_se = symbol_entrez.to_dict(orient='dict')[1]

vegas_ad1['Entrez'] = vegas_ad1['Gene'].map(d_se)
vegas_ad2['Entrez'] = vegas_ad2['Gene'].map(d_se)

vegas_ad1 = vegas_ad1.dropna(how='any')
vegas_ad2 = vegas_ad2.dropna(how='any')

vegas_ad1['nw_std'] = vegas_ad1['Pvalue'].map(lambda x: 1 if x < 0.01 else 0)
vegas_ad2['nw_std'] = vegas_ad2['Pvalue'].map(lambda x: 1 if x < 0.01 else 0)

if not os.path.exists('standards'):
    os.mkdir('standards')

if not os.path.exists('standards/vegas_ad1'):
    os.mkdir('standards/vegas_ad1')

if not os.path.exists('standards/vegas_ad2'):
    os.mkdir('standards/vegas_ad2')

for i in xrange(1000):
    vg_perm = vegas_ad1.reindex(np.random.permutation(vegas_ad1.index))
    vg_perm['Entrez'] = vg_perm['Entrez'].astype(int)
    vg_perm.to_csv('standards/vegas_ad1/' + str(i), sep="\t",
                   columns=['Entrez', 'nw_std'], header=False, index=False)

for i in xrange(1000):
    vg_perm = vegas_ad2.reindex(np.random.permutation(vegas_ad2.index))
    vg_perm['Entrez'] = vg_perm['Entrez'].astype(int)
    vg_perm.to_csv('standards/vegas_ad2/' + str(i), sep="\t",
                   columns=['Entrez', 'nw_std'], header=False, index=False)
