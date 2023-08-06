import re
from wheatly.errors import TestError


def clean_text(text):
    text = text.lower()
    regex_sub = re.sub(r"[,.;@#?!&$\'\"]+", " ", text)  # clean out punctuation
    regex_sub = re.sub(r"\s+", " ", regex_sub)  # replace multiple spaces with only one

    return regex_sub


def get_from_key_list(data, keys):
    if data == None:
        return None
    if len(keys) > 1:
        if type(data) != dict:
            return None

        # if the key doesn't exist then return None
        if not keys[0] in data.keys():
            return None
        # if we aren't at the last key then go a level deeper
        return get_from_key_list(data[keys[0]], keys[1:])
    else:
        # if the key doesn't exist then return None
        if not keys[0] in data.keys():
            return None
        # return the value we want
        return data[keys[0]]


def dedupe_list(data):
    tmp = []
    [tmp.append(x) for x in data if not x in tmp]
    return tmp


def check_assert(logger, res, args):
    did_succeed = True
    if "assert" in args:
        for k in args["assert"]:
            out_val = args["assert"][k]
            if get_from_key_list(res, k.split(".")) == out_val:
                logger.SUCCESS(f"Assertion passed for {k} == {out_val}")
            else:
                logger.FAILURE(f"Assertion failed for {k} == {out_val}")
                did_succeed = False
    else:
        did_succeed = res["__success__"]
        if not did_succeed:
            logger.FAILURE("Assertion failed for success == True")
    if not did_succeed:
        logger.ERROR(res)
    return did_succeed


def check_arg(args, key):
    if key in args.keys():
        return args[key]
    return None


def check_required(object, required, index):
    missing = []
    for k in required:
        if not k in object.keys():
            missing.append(k)
    if len(missing) > 0:
        raise TestError(f"Missing required keys {missing} in instruction {index}")
