# Spec-Pilot

Spec-Pilot is a command-line tool that simplifies the creation and management of OpenAPI specifications using natural language processing (NLP). With Spec-Pilot, you can easily generate, modify, and validate OpenAPI specifications without the need for complex manual editing.

- [Spec-Pilot](#spec-pilot)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Initialize a new OpenAPI project](#initialize-a-new-openapi-project)
    - [Generate OpenAPI specifications](#generate-openapi-specifications)
    - [Run a demo](#run-a-demo)
    - [Modify OpenAPI specifications using natural language input](#modify-openapi-specifications-using-natural-language-input)
    - [Validate OpenAPI specification files](#validate-openapi-specification-files)
  - [License](#license)
  - [Contributing](#contributing)
  - [Support](#support)

## Features

- Initialize a new OpenAPI project with a given project name.
- Generate OpenAPI specifications for a specified project.
- Modify OpenAPI specifications using natural language input.
- Validate OpenAPI specifications using the integrated validator.
- Simple command-line interface.

## Requirements

- Python 3.6 or higher

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/jmfwolf/spec-pilot.git
cd spec-pilot
```

(Optional) Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To see the available options, run:

```bash
python spec_pilot.py --help
```

### Initialize a new OpenAPI project

```bash
python spec_pilot.py --init project_name
```

### Generate OpenAPI specifications

```bash
python spec_pilot.py --generate project_name
```

### Run a demo

```bash
python spec_pilot.py --demo
```

### Modify OpenAPI specifications using natural language input

```bash
python spec_pilot.py --nlp "Add a new endpoint /users that supports GET method"
```

### Validate OpenAPI specification files

```bash
python spec_pilot.py --validate openapi_spec.yaml
```

## License

Spec-Pilot is released under the GNU General Public License v3.0.

## Contributing

Contributions are welcome! Please read the contributing guidelines for more information.

## Support

If you have any questions, issues, or feature requests, please submit an issue.
