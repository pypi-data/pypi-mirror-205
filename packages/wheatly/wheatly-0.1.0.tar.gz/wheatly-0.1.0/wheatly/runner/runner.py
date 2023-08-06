import json
import time
import requests
import wheatly.utils as utils


def run_text(logger, statement, context, objects):
    logger.INFO(statement["text"])
    full_success = True

    # loop through the objects
    for object_name in statement["objects"]:
        obj = objects[object_name]

        # loop through the actions
        for action_name in statement["actions"]:
            # does the action function exist
            try:
                function = getattr(obj, "action_" + action_name)
            except:
                logger.ERROR(
                    f"No method found for {object_name} with name action_{action_name}"
                )
                full_success = False
                continue
            print(context)
            # run the action function
            context, success = function(
                context, logger, statement["args"], statement["modifiers"]
            )
            if not success:
                full_success = False
    return full_success, context


def run_wait(logger, statement):
    # wait for the specified amount of time
    duration = statement["duration"]
    logger.INFO(f"Waiting for {duration} seconds")
    time.sleep(duration)


def run_curl(logger, statement):
    # build the connection
    path = statement["path"]
    method = statement["method"]
    host = statement["host"]
    logger.INFO(f"performing {method} request at {host}{path}")

    if method == "get":
        res = requests.get(f"{host}/{path}")
    # TODO: Add other HTTP methods here

    # load the object it it succeeded
    object = {}
    if res.status_code < 400 and statement["response_type"] == "json":
        object = json.loads(res.content)

    # load the object if it succeeded
    object["__success__"] = res.status_code < 400
    logger.INFO(object)

    # check any assertions that may have been specified
    success = utils.check_assert(logger, object, statement["args"])
    return success
