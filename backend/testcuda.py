
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

import torch

print(torch.__version__)       
print(torch.version.cuda)          
print(torch.cuda.is_available())  
print(torch.cuda.device_count())   