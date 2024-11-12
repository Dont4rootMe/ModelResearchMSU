import json
import os
from tqdm import tqdm
from itertools import count
from typing import Callable
from math import ceil


def get_span_tags(ds_path: str) -> list[str]:
    """
    Get all tags used in dataset

    Args:
        ds_path (str): path to json file with dataset

    Returns:
        (list[str]): list of all tags in dataset
    """
    # check if dataset file exists
    assert os.path.exists(ds_path), f'no such file: "{ds_path}"'

    # open file with dataset
    with open(ds_path, 'r') as ds:
        dataset = json.load(ds)['dataset']

    return dataset['span_tags']


def tokenize_entities(tokens: list, entities: list, tag_list: list[str] | None, default_label: str = 'NER') -> list[int, int, str]:
    """
    Combine all entity tokens from entities

    Args:
        tokens (list): list of tokens (text, ind_start, ind_end)
        entities (list): list of entities (ind_start, ind_end, label)
        tag_list (list[str] | None): defined tags in dataset
        default_label (str): default label for unspecified tagging

    Returns:
        list[ind_start, ind_end, label]
    """
    new_entities = set()

    for pos, token in enumerate(tokens):
        for ent in entities:
            if ent['begin'] <= token[1] <= ent['end'] or ent['begin'] <= token[2] <= ent['end']:
                for tag in ent['tags']:
                    new_entities.add((pos, pos, tag_list[tag] if tag_list else default_label))

    return list(new_entities)


def construct_dataset(
    ds_path: str,
    max_tokens: int,
    token_parser_func: Callable,
    *,
    max_labels: int = None,
    default_label: str = 'NER',
    verbose: bool = False
) -> list[dict[str, int]]:
    """
    Creates dataset appropriate for GLINER-like models fine-tune. Takes in account max context window of model,
    splitting each text by max_tokens with shift of max_tokens // 2 on each step

    Args:
        ds_path (str): path to json file with dataset
        max_tokens (int): count of tokens in model context
        token_parser_func (Callable): function with signature
            (str) -> list[(token, token_start, token_end))
        max_labels (str): count of labels to append to each text
        default_label (str): default label for unspecified tagging
        verbose (bool): wether to show progress bar on proccessing dataset

    Returns:
        dataset (list[dict]):
    {
        "tokenized_text" (list[str]): appropriate tokenization of text chunk \\
        "ner" (list[tuple(int, int, str)]): list of tuples (token_start, token_end, entity_label)
    }
    """
    # check if dataset file exists
    assert os.path.exists(ds_path), f'no such file: "{ds_path}"'

    # open file with dataset
    with open(ds_path, 'r') as ds:
        dataset = json.load(ds)['dataset']

    new_dataset = []
    half_token_window = max_tokens // 2

    # get all tags used in dataset
    tags = dataset['span_tags']

    # create tag subsets to append at each sentece
    if max_labels is not None:
        tags_subsets = [tags[i*max_labels:(i+1)*max_labels] for i in range(ceil(len(tags) / max_labels))]
    else:
        tags_subsets = [tags]

    # dataset converter
    prbr = tqdm(dataset['markups'], desc='dataset proccessing: ') if verbose else dataset['markups']
    for obj in prbr:
        # get tokenized reprezentation of input string
        tokens = [*token_parser_func(obj['text'])]

        # get all entities in current object
        entities = obj['spans']

        for substr_idx in count():
            # get context window of max len for specified model
            working_tokens = tokens[half_token_window * substr_idx: half_token_window * (substr_idx + 2)]

            # sanity check
            assert len(working_tokens) <= max_tokens, 'something is wrong with "working_tokens"'

            # create object for current max len context window
            for tsbs in tags_subsets:
                new_object = {
                    'tokenized_text': [tpl[0] for tpl in working_tokens],
                    'ner':  tokenize_entities(working_tokens, entities, tsbs, default_label),
                }

                # add all new object to pool
                new_dataset.append(new_object)

            # if it was last context window => break
            if half_token_window * (substr_idx + 2) + 1 > len(tokens):
                break

    return new_dataset
