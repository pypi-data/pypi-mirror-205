import spacy

nlp = spacy.load("en_core_web_sm")


def process_natural_language_input(sentence):
    doc = nlp(sentence)

    # Extract relevant information from the sentence
    command, target, details = extract_command_target_details(doc)

    # Perform the appropriate action based on the extracted information
    perform_action(command, target, details)


def extract_command_target_details(doc):
    command = None
    target = None
    details = {}

    for token in doc:
        # Extract command
        if token.dep_ == "ROOT":
            command = token.lemma_

        # Extract target
        if token.dep_ in ["dobj", "attr"]:
            target = token.lemma_

        # Extract additional details (e.g., adjectives, compound nouns)
        if token.dep_ in ["amod", "compound"]:
            if token.head.lemma_ not in details:
                details[token.head.lemma_] = []
            details[token.head.lemma_].append(token.lemma_)

    return command, target, details


def perform_action(command, target, details):
    if command == "initialize":
        if target == "project":
            project_name = details.get("name", [None])[0]
            if project_name:
                generator.init_project(project_name)
            else:
                print("Please specify a project name.")
        else:
            print(f"Unsupported target for command '{command}': {target}")

    elif command == "add" or command == "update" or command == "remove":
        if target == "schema" or target == "parameter":
            component_name = details.get("name", [None])[0]
            property_name = details.get("property", [None])[0]
            value = details.get("value", [None])[0]

            if component_name and property_name:
                if command == "add":
                    generator.add_component_property(target, component_name, property_name, value)
                elif command == "update":
                    generator.update_component_property(target, component_name, property_name, value)
                elif command == "remove":
                    generator.remove_component_property(target, component_name, property_name)
            else:
                print("Please specify both the component name and property name.")
        else:
            print(f"Unsupported target for command '{command}': {target}")

    else:
        print(f"Unsupported command: {command}")
