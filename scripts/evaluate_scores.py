"""Recompute AP/AUROC from previously generated score CSVs; no model inference."""
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

METHODS = {"mean_nll":"Mean token NLL (baseline)","p90_nll":"90th percentile token NLL (proposed)","answer_token_length":"Answer length (control)"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data-dir',type=Path,default=Path('data'))
    parser.add_argument('--output',type=Path,default=Path('results/recomputed_results.csv'))
    args=parser.parse_args()
    frames={}
    for split,n in [('train',420),('validation',90),('test',90)]:
        frame=pd.read_csv(args.data_dir/f'{split}_scores.csv')
        assert len(frame)==n, f'{split}: unexpected row count'
        assert frame['ID'].is_unique and frame['status'].eq('ok').all()
        assert frame['label'].isin([0,1]).all()
        assert frame[list(METHODS)].notna().all().all()
        assert np.isfinite(frame[list(METHODS)].to_numpy(dtype=float)).all()
        frames[split]=frame
    assert pd.concat([d['ID'] for d in frames.values()]).is_unique
    rows=[]
    for split in ['validation','test']:
        df=frames[split]
        y=df.label.astype(int).to_numpy()
        assert len(np.unique(y))==2
        for col,method in METHODS.items():
            scores=df[col].to_numpy(dtype=float)
            rows.append(dict(method=method,column=col,split=split,n=len(y),positives=int(y.sum()),prevalence=float(y.mean()),average_precision=float(average_precision_score(y,scores)),auroc=float(roc_auc_score(y,scores))))
    out=pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(args.output,index=False)
    print(out[['split','column','average_precision','auroc']].to_string(index=False))
    print('RECOMPUTED METRICS: PASS')
    print('Saved:',args.output)

if __name__=='__main__': main()
