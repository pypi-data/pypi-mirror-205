import subprocess
import sys
from checkov.terraform.runner import Runner as TerraformRunner
import uuid
import json
import os
from pathlib import Path


class PingSafeCli:
    def __init__(self) -> None:
        pass
    def run(self, repo_path, rego_file_path) -> None:
        print (repo_path, rego_file_path)
        terraform_runner = TerraformRunner()
        graph = terraform_runner.generate_graph(repo_path)
        input_json_dir = os.getcwd() + "/input_json/"
        if os.path.exists(input_json_dir) == False:
            os.mkdir(input_json_dir)
        try:
            for node in graph["nodes"]:
                input_json_path = f"{input_json_dir}{uuid.uuid4()}.json"
                with open(input_json_path, "w") as f:
                    json.dump(node, f)
                # output = subprocess.check_output(["./go-rego-evaluator", input_json_path, rego_file_path])
                # print(output)
                # print (f".{Path(__file__).parent}/go-rego-evaluator")
                subprocess.run([f"{Path(__file__).parent}/go-rego-evaluator", input_json_path, rego_file_path])
                # os.remove(input_json_path)
        except Exception as e:
            print(e)
        finally:
            files = os.listdir(input_json_dir)
            for file in files:
                file_path = os.path.join(input_json_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)




if __name__ == '__main__':
    ckv = PingSafeCli()
    print ("world")
    sys.exit(ckv.run("a", "b"))



