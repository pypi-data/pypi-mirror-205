import torch
from transformers import BertTokenizer, AlbertModel
from transformers import AutoModelForSequenceClassification



class Evaluator:
    def __init__(self, tokenizer=None, model=None, threshold=0.7, cuda="cpu"):
        self.device = torch.device(cuda if torch.cuda.is_available() else "cpu")
        self.tokenizer =tokenizer
        self.model=model
        self.threshold = threshold
        if not self.tokenizer:
            self.tokenizer = BertTokenizer.from_pretrained("uer/albert-large-chinese-cluecorpussmall")
        if not self.model:
            self.model = AutoModelForSequenceClassification.from_pretrained("uer/albert-large-chinese-cluecorpussmall", num_labels=2)
            self.model.load_state_dict(torch.load("./large.pt",map_location=self.device))
            self.model.to(self.device)

    def predict(self,text1,text2=None):
        self.model.eval()
        
        encoded_input = self.tokenizer(text1[-32:],text2[:32], padding=True ,return_tensors='pt').to(self.device) \
    if text2 else self.tokenizer(text1[:64], padding=True ,return_tensors='pt').to(self.device)
        
        output = self.model(**encoded_input)
        prob = torch.softmax(output.logits,-1)
        p = prob[0][1].item()
        return p
    
    
    def is_good(self,text):
        return self.predict(text)>self.threshold
    
    def is_continuous(self,text1, text2):
        return self.predict(text1,text2)>self.threshold
    
    # def __call__(self,text1,text2):
    #     return self.predict(text1,text2)>self.threshold
    