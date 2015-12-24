"""
(C) Casey Greene based on code by Irene Song.

This python script generates long format table with performance information
for GWAS runs (VEGAS format) and NetWAS runs (SVMperfer format) for later
visualization.
"""
import pandas as pd
from sklearn.metrics import roc_auc_score

# header on the first line, gene name in the second col
vegas_ad1 = pd.read_excel('data/vegas_adni1.xls', header=0, index_col=1)
vegas_ad2 = pd.read_excel('data/vegas_adni2.xls', header=0, index_col=1)

# clean up elements we don't use before combining
vegas_ad1.drop(['Chr', 'nSNPs', 'nSims', 'Start', 'Stop', 'Test'],
               inplace=True, axis=1)
vegas_ad1.rename(columns={'Pvalue': 'VEGAS_AD1'}, inplace=True)
vegas_ad2.drop(['Chr', 'nSNPs', 'nSims', 'Start', 'Stop', 'Test'],
               inplace=True, axis=1)
vegas_ad2.rename(columns={'Pvalue': 'VEGAS_AD2'}, inplace=True)

vegas = pd.merge(vegas_ad1, vegas_ad2, left_index=True, right_index=True,
                 how='outer')

vegas = vegas.reset_index()  # Unindex by gene so that we can go entrez later

# Map to Entrez
symbol_entrez = pd.read_csv('data/symbol_entrez.txt', sep='\t', header=None,
                            index_col=0)
d_se = symbol_entrez.to_dict(orient='dict')[1]
vegas['Entrez'] = vegas['Gene'].map(d_se)
vegas = vegas.dropna(axis=0, how='any')  # Drop anything that lacked entrez
vegas = vegas.set_index('Gene')

# Load AD associated genes
do_status = pd.read_csv('data/tribe_ad_list.csv', index_col=0)
full_status = pd.merge(vegas, do_status, left_index=True, right_index=True,
                       how='outer')
# Set NAs in Tribe-AD-Status equal to zero
full_status['Tribe-DO-Status'].loc[full_status['Tribe-DO-Status'] != 1] = 0

full_status = full_status.reset_index()

# Index on Entrez again
full_status = full_status.set_index('Entrez')

# no header, gene name in the first col
netwas_ad1 = pd.read_csv('results/vegas_ad1/0', sep='\t', header=None,
                         index_col=0, names=["Entrez", "Standard", "NETWAS"])

# Keep only genes in the NetWAS also
new_status = pd.merge(full_status, netwas_ad1, left_index=True,
                      right_index=True, how='inner')

o_fh = open('results-proc.txt', 'w')
o_fh.write('GWAS\tMethod\tAUC\n')

a1_do = roc_auc_score(new_status['Tribe-DO-Status'], 1-new_status['VEGAS_AD1'])
o_fh.write('AD1\tGWAS\t' + str(a1_do) + '\n')
a2_do = roc_auc_score(new_status['Tribe-DO-Status'], 1-new_status['VEGAS_AD2'])
o_fh.write('AD2\tGWAS\t' + str(a2_do) + '\n')

gwases = ['AD1', 'AD2']
num = 1000

for gwas in gwases:
    gwas_fname = 'vegas_' + gwas.lower()
    new_status[gwas + '-NetWAS-RankSum'] = 0
    for i in xrange(num):
        netwas = pd.read_csv('results/' + gwas_fname + '/' + str(i),
                             sep='\t', header=None, index_col=0,
                             names=["Entrez", "Standard", "NETWAS"])
        net_status = pd.merge(full_status, netwas, left_index=True,
                              right_index=True, how='inner')
        new_status[gwas + '-NetWAS-RankSum'] = \
            new_status[gwas + '-NetWAS-RankSum'] + \
            net_status['NETWAS'].rank()
        score = roc_auc_score(net_status['Tribe-DO-Status'],
                              net_status['NETWAS'])
        o_fh.write('\t'.join((gwas, 'NETWAS', str(score))) + '\n')
    # merge_auc = roc_auc_score(new_status['Tribe-DO-Status'],
    #                           new_status[gwas + '-NetWAS-RankSum'])
    # We don't want to plot the rank sum, we just want to have the rank
    # combined list available for the paper.
    # auc was similar to or slightly above what we observed for the individual
    # runs.
    # o_fh.write('\t'.join((gwas, 'NETWAS-RankSum', str(merge_auc))) + '\n')

    # processed permed files
    for i in xrange(num):
        netwas = pd.read_csv('results/p_' + gwas_fname + '/' + str(i),
                             sep='\t', header=None, index_col=0,
                             names=["Entrez", "Standard", "NETWAS"])
        net_status = pd.merge(full_status, netwas, left_index=True,
                              right_index=True, how='inner')
        score = roc_auc_score(net_status['Tribe-DO-Status'],
                              net_status['NETWAS'])
        o_fh.write('\t'.join((gwas, 'Permuted-NETWAS', str(score))) + '\n')

o_fh.close()

new_status.drop(['Standard', 'NETWAS'], inplace=True, axis=1)
new_status.to_csv('combined-results.csv')
