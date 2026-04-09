from .prepare_raw import read_seq_info
from .topo import get_topo
from .model import MVTDL
from .data import get_dataloader
from .utils import normalize,index2go





def get_data(seq,folder):
    pdb,esm,prottrans,domain = read_seq_info(seq,folder)
    topo = get_topo(pdb,seq,esm,prottrans)
    topo.set_domain(domain)
    cc,bp,mf = normalize(topo.pl)
    dataloader = get_dataloader(topo,cc,bp,mf)
    return dataloader


def get_prediction(model_folder,dataloader,device):
    model = MVTDL(model_folder,device)
    model.predict(dataloader)
    res = index2go('CC',model.pred['CC']) + index2go('MF',model.pred['MF']) + index2go('BP',model.pred['BP'])
    return res
    