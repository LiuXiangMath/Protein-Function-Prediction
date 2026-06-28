# Protein Function Prediction

## Installation (Linux x86_64 only)
1. Create the environment

```
conda create -n mvtdl python=3.10 -y
conda activate mvtdl
```

2. Install required packages

```
pip install -r requirements.txt
```

3. Download the pretrained models from [here](https://weilab.math.msu.edu/Downloads/MVTDL/model/models.zip). After downloading, extract the archive and move the three model files into `src/checkpoint/`

4. You need to install Interproscan on your server and make it available as a global command. Please refer to [here](https://interproscan-docs.readthedocs.io/en/v5/HowToDownload.html)
   


## Usage
Run the following command to get predictions. Replace `YourProteinSeq` with your protein sequence.
```
python prediction.py --seq YourProteinSeq
```

## Example
If you run:
```
python prediction.py GEYFTLQIRGRERFEMFRELNEALELKDAQAG
```
The output is 
```
Input sequence: GEYFTLQIRGRERFEMFRELNEALELKDAQAG
Predicted functions are: ['cytoplasm', 'metal ion binding']
```

