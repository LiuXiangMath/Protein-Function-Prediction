from .prepare_raw import read_seq_info
from .topo import get_topo
from .model import MVTDL,TDL
from .data import get_dataloader
from .utils import normalize,index2go
import torch
import numpy as np
import torch.nn as nn




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


def get_prediction_5fold(model_folder,dataloader,device):
    class_num = {'CC':2879,'MF':8110,'BP':17511}
    threshold = {'CC':[0.29,0.4,0.4,0.36,0.41,0.372],'MF':[0.32,0.44,0.38,0.5,0.46,0.42],'BP':[0.49,0.58,0.56,0.53,0.48,0.528]}
    pred = { 'CC':[], 'BP':[], 'MF':[] }
    for typ in ['CC','BP','MF']:
        pred5 = []
        for fold in [0,1,2,3,4]:
            model = TDL(class_num=class_num[typ]).to(device)
            modelname = model_folder+typ+'-fold-'+str(fold)+'.pt'
            state = torch.load(modelname, map_location='cpu',weights_only=False)
            model.load_state_dict(state['model'], strict=True)
        
            prediction = nn.Sigmoid()
            pred_list = []
            model.eval()
            with torch.no_grad():
                for batch_index, data in enumerate(dataloader):
                    data = data.to(device)
                    if typ=='CC':
                        y_pred = model.forward_cc(data)
                    elif typ=='BP':
                        y_pred = model.forward_bp(data)
                    elif typ=='MF':
                        y_pred = model.forward_mf(data)
                    outputs = prediction(y_pred)
                    pred_list.append(outputs.detach().cpu().numpy())
            tmp = (pred_list[0][0]>=threshold[typ][fold])
            idx = np.where(tmp == True)[0].tolist()
            pred[typ].extend(index2go(typ,idx))
        tmp2 = pred[typ]
        pred[typ] = list(set([x for x in tmp2 if tmp2.count(x) > 1]))
    
    torch.cuda.empty_cache()  
    
    
    return pred['CC']+pred['BP']+pred['MF']  
