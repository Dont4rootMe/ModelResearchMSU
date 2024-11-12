def merge_entities(predicted_entities, text):
    """
    Merge all neighbour entities

    Args:
        predicted_entities (list[entity]): list of all predicted entities
        text (str): sentence of model input

    Returns:
        (list[entity]): list of merged entities
        (str): inputed sentence
    """
    # check if there is no entities
    if not predicted_entities:
        return []

    merge = []
    indexes = [*range(len(predicted_entities))]

    while indexes:
        curr_ind = indexes.pop(0)
        curr_ent = predicted_entities[curr_ind]

        indexes_to_remove = []
        for next_ind in indexes:
            next_ent = predicted_entities[next_ind]

            if curr_ent['end'] + 1 < next_ent['start']:
                break

            if curr_ent['label'] == next_ent['label']:
                curr_ent['text'] = text[curr_ent['start']: next_ent['end']].strip()
                curr_ent['end'] = next_ent['end']
                indexes_to_remove.append(next_ind)

        for ind_rem in indexes_to_remove:
            indexes.remove(ind_rem)

        merge.append(curr_ent)

    return merge, text


def wrap_unifed_dataset(model, labels, sents):
    """
    Combine model output into unifide dataset

    Args:
        model (Any): model with callable function "batch_predict_entities"
        labels (list[str]): labels to find in sentences
        sents (list[str]): list of sentences to parse

    Returns:
        (dict): unified dataset
    """
    output = model.batch_predict_entities(sents, labels=labels)
    predictions = list(map(lambda x: merge_entities(x[0], x[1]), zip(output, sents)))

    dataset = {
        "assessors": ['model'],
        "dataset": {
            "span_tags": labels,
            "relation_tags": [],
            "markups": [
                {
                    "assessor": 0,
                    "text": text,
                    "relations": [],
                    "spans": [
                        {
                            "begin": ent['start'],
                            "end": ent['end'],
                            "id": i,
                            "tags": [labels.index(ent['label'])]
                        } for i, ent in enumerate(entities)
                    ]
                } for entities, text in predictions
            ]
        }
    }

    return dataset
