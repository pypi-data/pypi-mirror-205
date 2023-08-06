import wheatly.cli as cli
from wheatly.errors import TestError
from wheatly.nlp import parser
from wheatly.runner import runner

from cartils.logger import Logger
from aphelper import core

import os
import sys
import json
import yaml


class CLI:
    def __init__(self):
        global data
        ah = core.ArgparseHelper(def_data=cli.data, parent=self)
        ah.execute()

    def import_plugins(self, path: str) -> dict:
        sys.path.append(path)
        self.plugins = {}

        for file in os.listdir(path):
            mod_name = file[:-3]  # strip .py at the end
            if mod_name.startswith("__"):
                continue
            exec("import " + mod_name)
            globals()[mod_name] = locals()[mod_name]
            self.plugins[mod_name] = locals()[mod_name]

    def build_objects(self):
        for key in config.lexicon:
            val = config.lexicon[key]
            module = globals()[key]
            cls = getattr(module, val["class"])
            obj = cls()
            self.objects = {key: obj}

    def generate(self, args):
        self.import_plugins(args.plugins)
        self.build_objects()

        logger = Logger(args.log_level)
        logger.INFO("Generating test JSON")
        logger.DEBUG(f"Input arg: {args.input}")
        logger.DEBUG(f"Output arg: {args.output}")

        if args.input.endswith(".yaml") or args.input.endswith(".yml"):
            with open(args.input) as f:
                data = yaml.safe_load(f)
        elif args.input.endswith(".json"):
            with open(args.input) as f:
                data = json.load(f)
        else:
            raise TestError(
                "Input files only of type .yml, .yaml, and .json are accepted "
            )

        processed = {}

        for name in data["tests"]:
            logger.DEBUG(f"Processing test {name}")

            test = data["tests"][name]
            processed_test = []
            index = 1

            for instruction in test:
                logger.DEBUG(f"Processing instruction {instruction}")

                if type(instruction) == str:
                    res = parser.process_raw_text(instruction, self.objects, index)
                    processed_test.append(res)

                elif type(instruction) == dict:
                    if "score" in instruction.keys():
                        res = parser.process_score(instruction, index)
                        processed_test.append(res)

                    elif "wait" in instruction.keys():
                        res = parser.process_wait(instruction)
                        processed_test.append(res)

                    elif "action" in instruction.keys():
                        res = parser.process_action(instruction)
                        processed_test.append(res)

                    elif "curl" in instruction.keys():
                        res = parser.process_curl(instruction, index)
                        processed_test.append(res)

                    else:
                        res = parser.process_text(instruction, self.objects, index)
                        processed_test.append(res)
                else:
                    raise TestError(f"Instruction {index} is not valid")
                index += 1

            processed[name] = processed_test

        with open(args.output, "w") as f:
            json.dump(processed, f, indent=4)

        logger.SUCCESS("Done!")

    def run(self, args):
        self.import_plugins(args.plugins)
        self.build_objects()

        def reset_context(context):
            for k in context:
                if k != "conn":
                    context[k] = None
            return context

        # setup logger
        logger = Logger(args.log_level)

        logger.DEBUG(f"Input arg: {args.input}")

        results = {}
        context = {}

        with open(args.input, "r", encoding="utf-8") as test_file:
            data = yaml.safe_load(test_file)

        for test in data:
            logger.INFO(f"Running test {test}")

            context = reset_context(context)
            did_succeed = True

            for statement in data[test]:
                if statement["type"] == "text":
                    success, context = runner.run_text(
                        logger, statement, context, self.objects
                    )
                    if not success:
                        did_succeed = False
                elif statement["type"] == "wait":
                    runner.run_wait(logger, statement)
                elif statement["type"] == "action":
                    success, context = runner.run_action(logger, statement, context)
                    if not success:
                        did_succeed = False
                elif statement["type"] == "curl":
                    success = runner.run_curl(logger, statement)
                    if not success:
                        did_succeed = False

            results[test] = did_succeed
            if did_succeed:
                logger.SUCCESS(f"Test {test} passed")
            else:
                logger.FAILURE(f"Test {test} failed")

        logger.SUCCESS("Done!")

        failed = [r for r in results if not results[r]]
        passed = [r for r in results if results[r]]

        if len(failed) == 0:
            logger.SUCCESS("All tests passed")
            if args.dump:
                with open("out.txt", "w") as f:
                    f.write(f"Passed: {passed}\nFailed: {failed}")
            exit(0)

        logger.FAILURE("The following tests failed:")
        logger.FAILURE(str(failed))

        if args.dump:
            with open("out.txt", "w") as f:
                f.write(f"Passed: {passed}\nFailed: {failed}")

        exit(1)


def main():
    CLI()


if __name__ == "__main__":
    main()
