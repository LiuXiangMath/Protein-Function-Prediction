# Protein Function Prediction

## Installation (only for linux x86_64)
1. create environment

```
conda create -n mvtdl python=3.10 -y
conda activate mvtdl
```

2. install required packages

```
pip install -r requirements.txt
```

3. You need to install Interproscan in your server and make it a global call, refer to (https://interproscan-docs.readthedocs.io/en/v5/HowToDownload.html)


## Usage
run the following code to get predictions, input your sequence to the parameter --seq
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

