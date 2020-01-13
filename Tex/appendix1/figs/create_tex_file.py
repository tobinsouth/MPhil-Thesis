
import pandas as pd

df = pd.read_csv('removed_accounts.csv')
gap = 40
for i, index in enumerate(range(0,len(df), gap)):
    with open(f'removed_accounts_{i}.tex', 'w') as f:
        df.iloc[index:index+gap].to_latex(f, index =  False)

with open(f'removed_accounts.tex', 'w') as f:
    df.to_latex(f, index =  False)



df = pd.read_csv('appendix_accounts.csv')
gap = 40
for i, index in enumerate(range(0,len(df), gap)):
    with open(f'appendix_accounts_{i}.tex', 'w') as f:
        df.iloc[index:index+gap].to_latex(f, index =  False)


with open(f'appendix_accounts.tex', 'w') as f:
    df.to_latex(f, index =  False)
