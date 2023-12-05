from pathlib import Path
#from kiesraad
import parse_eml

source = Path('../data/tk2021/Gemeente tellingen')
dfs = parse_eml.parse_eml(source, per_candidate=True)
target = Path('../data/tk2021/') / 'csv'
target.mkdir(exist_ok=True)
for name, df in dfs.items():
    path = target / f'{name}.csv'
    df.to_csv(path, index=False)
