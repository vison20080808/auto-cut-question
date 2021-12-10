# usage

    cd OCRQUESSEG-SVR
    
# 安装pytorch

## 检查cuda 版本，根据对应cuda 版本安装pytorch 
- 详细介绍 https://pytorch.org/get-started/previous-versions/

- 若cuda 为10.1的，则 
    pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

    cd OCRQUESSEG-SVR
    
    pip install -e .

    pip install -e detectron2

    python predictor.py
