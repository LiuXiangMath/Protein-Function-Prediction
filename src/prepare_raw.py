import torch
from esm.models.esmc import ESMC
from esm.sdk.api import ESMProtein, LogitsConfig
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


from transformers import T5Tokenizer, T5EncoderModel
from transformers import logging
logging.set_verbosity_error()
import re
import numpy as np
import time
import os
from .utils import read_domain


def get_esmc(pdb,seq,folder):
    client = ESMC.from_pretrained("esmc_600m").to(device)
    
    protein = ESMProtein(sequence=seq)
    protein_tensor = client.encode(protein)
    logits_output = client.logits( protein_tensor, LogitsConfig(sequence=True, return_embeddings=True) )
    esm_embed = logits_output.embeddings.squeeze(0).cpu().numpy()
    esm = esm_embed[1:]
    torch.cuda.empty_cache()  
    return esm


def get_prottrans(pdb,seq,folder):
    tokenizer = T5Tokenizer.from_pretrained('Rostlab/prot_t5_xl_half_uniref50-enc', do_lower_case=False)
    model = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_half_uniref50-enc").to(device)

    sequence_examples = [seq]
    sequence_examples = [" ".join(list(re.sub(r"[UZOB]", "X", sequence))) for sequence in sequence_examples]
    ids = tokenizer(sequence_examples, add_special_tokens=True, padding="longest")
    input_ids = torch.tensor(ids['input_ids']).to(device)
    attention_mask = torch.tensor(ids['attention_mask']).to(device)
    with torch.no_grad():
        embedding_repr = model(input_ids=input_ids, attention_mask=attention_mask)
        emb_0 = embedding_repr.last_hidden_state[0,:len(seq)] 
    prottrans = emb_0.cpu().numpy()
    torch.cuda.empty_cache()  
    return prottrans



def read_seq_info(seq,folder):
    pdb = str(int(time.time() * 1000))
    f = open(folder+pdb+'.fasta','w')
    f.write('>'+pdb+'\n')
    f.write(seq)
    f.close()
    
    esm = get_esmc(pdb,seq,folder)
    prottrans = get_prottrans(pdb,seq,folder)
    os.system('interproscan.sh -i '+folder+pdb+'.fasta -f tsv -o '+folder+pdb+'-domain.tsv')
    domain = read_domain(folder+pdb+'-domain.tsv')
    os.remove(folder+pdb+'-domain.tsv')
    os.remove(folder+pdb+'.fasta')
    return pdb,esm,prottrans,domain

    