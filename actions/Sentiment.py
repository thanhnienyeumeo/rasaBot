
from transformers import AutoTokenizer, RobertaForSequenceClassification, RobertaConfig

import numpy as np
import math
import warnings

warnings.filterwarnings("ignore")


def softmax(arr, label):
    e = math.e
    return (e ** arr[label]) / (e ** arr[0] + e ** arr[1])

tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')

config = RobertaConfig.from_pretrained(
        "actions/PhoBERT_base_transformers/config.json", from_tf=False, num_labels = 2, output_hidden_states=False,
    )
model = RobertaForSequenceClassification.from_pretrained(
        "actions/model/Model",
        config=config
    )

#tokenizer input
def get(input):
    
    #tokenizer and return a tensor -> model
    d = tokenizer(input, truncation=True, padding = True, return_tensors = 'pt')

    outputs = model(d['input_ids'], token_type_ids=None, 
                attention_mask= d['attention_mask'])

    logits = outputs[0]

    logits = logits.detach().cpu().numpy()

    label = np.argmax(logits).item()

    print('do tu tin', round(softmax(logits[0], label), 3))

    return label
print(get('tôi rất tự tin'))


