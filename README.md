# adni-netwas
This repository is associated with a Song et al. manuscript describing a Network-wide Association Study of ADNI Cohorts. Source code is licensed under the BSD 3-clause license. Data and results are licensed CC0.

There are a few steps associated with this analysis.

1. Standards for a NetWAS are generated (generate_standards.py), as are standards for permuted NetWAS (generate_perm_standard.py). The standards generated in the course of this analysis are provided (standards/)
2. The hippocampus.dab network is downloaded (download_hippo_net.sh) and the sha1sum is verified.
3. The analysis is run using a queue system (the analysis for this manuscript was run on DISCOVERY at Dartmouth). Scripts (run_netwas.py; run_perm_netwas.py) are used to generate and submit pbs jobs. For space, these pbs scripts were not included in the repository but can be regenerated with these python scripts. The output of these runs are provided (results/)
4. Results are collected across the multiple runs (generate_auc_comparison.py). Summarized results are provided (results-proc.txt; combined-results.csv).
5. Plotting is performed on these results (generate_qqs.R; plot_results.R). The output of these scripts is provided (figures/)

The final two steps are also implemented in process_results.sh.

There are some requirements. Python requirements are contained in the requirements.txt file. R requirements are "gap" and "ggplot2" libraries.
