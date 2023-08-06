import argparse
import os
import sys
import json
from generator import init_project, generate_openapi_spec, demo, render_template
from spec_parser import process_natural_language_input
from validator import vacuum


def main():
    parser = argparse.ArgumentParser(description="Spec-Pilot: Generate OpenAPI specifications using natural language")
    parser.add_argument("--init", metavar="project_name",
                        help="Initialize a new OpenAPI project with the specified project name")
    parser.add_argument("-g", "--generate", metavar="project_name",
                        help="Generate the OpenAPI specification for the specified project")
    parser.add_argument("--demo", help="Demonstration project",
                        action="store_true")
    parser.add_argument("--nlp", metavar="input_text",
                        help="Process a natural language input to modify the OpenAPI specification")
    parser.add_argument("-v", "--validate", metavar="spec_file",
                        help="Validate the provided OpenAPI specification file")
    parser.add_argument("-c", "--create", nargs=3, metavar=("template", "asset_name", "output_path"),
                        help="Create a new OpenAPI asset from the specified template with the given asset_name and save it to the output_path")

    args = parser.parse_args()

    if args.init:
        init_project(args.init)
    elif args.generate:
        generate_openapi_spec(args.generate)
    elif args.demo:
        demo()
    elif args.create:
        template, asset_name, output_path = args.create
        render_template(template, asset_name, output_path)
    elif args.nlp:
        if not os.path.exists("openapi_spec.json"):
            sys.exit("Error: openapi_spec.json not found. Please provide an existing OpenAPI specification to modify.")

        with open("openapi_spec.json", "r") as f:
            openapi_spec = json.load(f)

        modified_openapi_spec = process_natural_language_input(args.nlp, openapi_spec)

        if modified_openapi_spec:
            with open("openapi_spec.json", "w") as f:
                json.dump(modified_openapi_spec, f, indent=2)
        else:
            print("Error: Unable to process the provided natural language input.")
    elif args.validate:
        vacuum(["validate", args.validate])


if __name__ == "__main__":
    main()
