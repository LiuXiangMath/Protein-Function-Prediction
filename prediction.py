import torch
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import argparse
from src import get_data,get_prediction,check_input



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seq", type=str, required=True, help="Protein sequence",default='GEYFTLQIRGRERFEMFRELNEALELKDAQAG')

    args = parser.parse_args()

    

    seq = check_input(args.seq)
    
    # create folder for temp data
    folder = './temp-data/'
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # prepare files
    dataloader = get_data(seq,folder)
    
    
    # model folder
    model_folder = './src/checkpoint/'
    
    # prediction
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    prediction = get_prediction(model_folder,dataloader,device)
    
    print("Input sequence:", args.seq)
    print(f'Predicted functions are: {prediction}')
    

if __name__ == "__main__":
    main()
