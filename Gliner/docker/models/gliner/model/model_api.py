from gliner import GLiNER
from math import ceil
import os
from os.path import dirname
import sys

working_path = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
sys.path.append(dirname(os.path.join(working_path, 'model')))
sys.path.append(dirname(os.path.join(working_path, 'checkpoint')))


from model.tags import cult_tags
from model.utils import merge_entities


# upload model
gliner = GLiNER.from_pretrained(os.path.join(working_path, 'checkpoint'), load_tokenizer=True, local_files_only=True)
gliner.eval()


def model_api(text: str):
    total_markup = []
    for i in range(ceil(len(cult_tags) // 5)):
        tgs = cult_tags[i*5:(i+1)*5]
        entities = gliner.predict_entities(text, tgs)
        merged = merge_entities(text, entities)
        total_markup += merged

    return total_markup
