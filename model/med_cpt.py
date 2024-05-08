import torch.nn as nn

from transformers import AutoModel, AutoTokenizer

class MedCPT(nn.Module):
    def __init__(self, cpt_checkpoint='/mnt/petrelfs/share_data/wuchaoyi/SAM/Knowledge_Data/MedCPT_Query_Encoder'):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(cpt_checkpoint)
        self.model = AutoModel.from_pretrained(cpt_checkpoint)
        self.modality_embed = nn.Embedding(4, 768)
        
    def forward(self, text, modality):
        encoded = self.tokenizer(
                text, 
                truncation=True, 
                padding=True, 
                return_tensors='pt', 
                max_length=64,
            )
        
        text_feature = self.model(**encoded).last_hidden_state[:, 0, :]
        modality_feature = self.modality_embed(modality)
        text_feature += modality_feature
        
        return text_feature
