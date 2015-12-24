# assumes dependencies are installed.
# python depends: requirements.txt
# R depends: gap, ggplot2

mkdir -p figures

python generate_auc_comparison.py

R --no-save < generate_qqs.R
R --no-save < plot_results.R
