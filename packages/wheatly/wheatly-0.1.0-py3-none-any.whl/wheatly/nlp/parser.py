import wheatly.utils as utils
from wheatly.errors import TestError
import copy


def _get_object_matches(objects, text):
    # parse text to unigrams and bigrams
    unigrams = text.split(" ")
    bigrams = [
        (u, unigrams[i + 1]) for i, u in enumerate(unigrams) if i < len(unigrams) - 1
    ]
    out = []
    to_replace = []

    # give priority to bigrams
    # for example,
    # 'spark runtime' is more descriptive than
    # 'runtime'
    for b in bigrams:
        for o in objects:
            for x in objects[o].tokens:
                if x == b:
                    out.append(objects[o].name)
                    to_replace.append(" ".join(x))

    # remove all the bigrams we found
    # if we found 'sagemaker runtime'
    # we don't want that to trigger 'runtime' as well
    for tr in to_replace:
        text = text.replace(tr)

    unigrams = text.split(" ")

    # finally check the remaining text for single-word matches
    for o in objects:
        for x in objects[o].tokens:
            if x in unigrams:
                out.append(objects[o].name)
    return out


def _get_action_matches(objects, text):
    # parse text to unigrams and bigrams
    unigrams = text.split(" ")
    bigrams = [
        (u, unigrams[i + 1]) for i, u in enumerate(unigrams) if i < len(unigrams) - 1
    ]
    out = []
    to_replace = []

    # give priority to bigrams
    # for example,
    # 'spark runtime' is more descriptive than
    # 'runtime'
    for b in bigrams:
        for o in objects:
            for k in objects[o].actions:
                for x in objects[o].actions[k]:
                    if x == b:
                        out.append(k)
                        to_replace.append(" ".join(x))

    # remove all the bigrams we found
    # if we found 'sagemaker runtime'
    # we don't want that to trigger 'runtime' as well
    for tr in to_replace:
        text = text.replace(tr)

    unigrams = text.split(" ")

    # finally check the remaining text for single-word matches
    for o in objects:
        for k in objects[o].actions:
            for x in objects[o].actions[k]:
                if x in unigrams:
                    out.append(k)
    return out


def _get_modifier_matches(objects, text):
    # parse text to unigrams and bigrams
    unigrams = text.split(" ")
    bigrams = [
        (u, unigrams[i + 1]) for i, u in enumerate(unigrams) if i < len(unigrams) - 1
    ]
    out = []
    to_replace = []

    # give priority to bigrams
    # for example,
    # 'spark runtime' is more descriptive than
    # 'runtime'
    for b in bigrams:
        for o in objects:
            for k in objects[o].modifiers:
                for x in objects[o].modifiers[k]:
                    if x == b:
                        out.append(k)
                        to_replace.append(" ".join(x))

    # remove all the bigrams we found
    # if we found 'sagemaker runtime'
    # we don't want that to trigger 'runtime' as well
    for tr in to_replace:
        text = text.replace(tr)

    unigrams = text.split(" ")

    # finally check the remaining text for single-word matches
    for o in objects:
        for k in objects[o].modifiers:
            for x in objects[o].modifiers[k]:
                if x in unigrams:
                    out.append(k)
    return out


# parse text only text
def process_raw_text(instruction, objects, index):
    # clean the text
    clean_text = utils.clean_text(instruction)

    object_names = _get_object_matches(objects, clean_text)
    objs = {k: objects[k] for k in object_names}

    # parse it for everything we need
    out = {
        "actions": utils.dedupe_list(_get_action_matches(objs, clean_text)),
        "args": {},
        "modifiers": _get_modifier_matches(objs, clean_text),
        "objects": object_names,
        "text": instruction,
        "type": "text",
    }

    # check that we found something
    if len(out["objects"]) == 0:
        raise TestError(f"No objects found in instruction {index}")
    if len(out["actions"]) == 0:
        raise TestError(f"No actions found in instruction {index}")

    return copy.deepcopy(out)


# parse text with dictionary args
def process_text(instruction, objects, index):
    key = list(instruction.keys())[0]

    # clean the text
    clean_text = utils.clean_text(key)

    # parse it for everything we need
    out = {
        "actions": utils.dedupe_list(_get_action_matches(objects, clean_text)),
        "args": instruction[key],
        "modifiers": _get_modifier_matches(objects, clean_text),
        "objects": _get_object_matches(objects, clean_text),
        "text": key,
        "type": "text",
    }

    # check that we found something
    if len(out["objects"]) == 0:
        raise TestError(f"No objects found in instruction {index}")
    if len(out["actions"]) == 0:
        raise TestError(f"No actions found in instruction {index}")

    return copy.deepcopy(out)


# process wait action
def process_wait(instruction):
    out = {"duration": instruction["wait"], "type": "wait"}
    return copy.deepcopy(out)


def process_curl(instruction, index):
    required = ["data", "host", "method", "path"]
    utils.check_required(instruction["curl"], required, index)

    out = {
        "args": {"assert": utils.check_arg(instruction["curl"], "assert")},
        "data": utils.check_arg(instruction["curl"], "data"),
        "host": instruction["curl"]["host"],
        "method": instruction["curl"]["method"],
        "path": instruction["curl"]["path"],
        "type": "curl",
        "response_type": instruction["curl"]["response_type"],
    }
    if not out["args"]["assert"]:
        del out["args"]["assert"]
    return copy.deepcopy(out)


def process_conditional():
    pass
