import os
import pandas as pd
import numpy as np
import pickle

def check_input(seq):
    if not isinstance(seq, str):
        raise TypeError("Input must be a string.")
    
    seq = seq.strip().upper()
    
    if not seq:
        raise ValueError("Input sequence is empty.")
    
    
    if len(seq) < 10 or len(seq) > 5000:
        raise ValueError(
            f"Protein sequence length must be between 10 and 5000, but got {len(seq)}."
        )
        
    if not seq.isalpha():
        invalid_chars = sorted(set(c for c in seq if not c.isalpha()))
        raise ValueError(
            f"Sequence contains invalid character(s): {', '.join(invalid_chars)}"
        )
    return seq

def normalize(fea):
    fea = fea.reshape(7*40*7)
    mean = np.load('./config/CC-mean.npy')
    std = np.load('./config/CC-std.npy')
    cc = (fea-mean)/(std+1e-8)
    cc = cc.reshape(7,40,7)
    
    mean = np.load('./config/BP-mean.npy')
    std = np.load('./config/BP-std.npy')
    bp = (fea-mean)/(std+1e-8)
    bp = bp.reshape(7,40,7)
    
    mean = np.load('./config/MF-mean.npy')
    std = np.load('./config/MF-std.npy')
    mf = (fea-mean)/(std+1e-8)
    mf = mf.reshape(7,40,7)
    return cc,bp,mf




def read_domain(filename):
    if os.path.getsize(filename) == 0:
        return []
    df = pd.read_csv(filename, sep="\t", comment="#", header=None)
    info = {}
    for j in range(len(df)):
        n = int(df[2][j])
        typ = df[3][j].strip()
        start = int(df[6][j])
        end = int(df[7][j])
        status = df[9][j].strip()
        domain = df[11][j].strip()
        if status=='T' and len(domain)==9 and domain[0:3]=='IPR':
            info[domain] = [n]
    #print(info)
    
    with open('./config/domain.pkl','rb') as f:
        domain_index = pickle.load(f)
    res = set()
    for k in info:
        if k in domain_index:
            idx = domain_index[k]
            res.add(idx)
    return list(res)
    
    
def index2go(typ,idx):
    with open('./config/'+typ+'-go-index.pkl','rb') as f:
        go2index = pickle.load(f)
    index2go = {}
    for go in go2index:
        idx2 = go2index[go]
        index2go[idx2] = go
    with open('./config/go-name.pkl','rb') as f:
        go2name = pickle.load(f)
    res = [go2name[index2go[i]][0] for i in idx ]
    return res
    