import pystache
import os
import yaml
import re

def init_project(project_name):
    if project_name == "":
        project_name = input("Enter project name: ")
    os.mkdir(project_name)
    os.mkdir(os.path.join(project_name, "schemas"))
    os.mkdir(os.path.join(project_name, "paths"))
    os.mkdir(os.path.join(project_name, "parameters"))
    os.mkdir(os.path.join(project_name, "responses"))
    os.mkdir(os.path.join(project_name, "tags"))
    os.mkdir(os.path.join(project_name, "servers"))
    os.mkdir(os.path.join(project_name, "infos"))
    # openapi_file_path = os.path.join(project_name, "openapi.yml")
    # open(openapi_file_path, "w").close()


def render_template(asset_type, context, output_file, version="v3.0"):
    check_version(version)
    asset_types = ['schema', 'path', 'response', 'server', 'info', 'parameter']
    if asset_type not in asset_types:
        raise ValueError("asset type is not recognized")
    template_file = f"templates/{version}/{asset_type}.mustache"
    with open(template_file, 'r') as f:
        template = f.read()
    rendered = pystache.render(template, context)

    with open(output_file, 'w') as f:
        f.write(rendered)

def build_context(asset_type):
    required = check_requirements(asset_type)
    context = {}
    for requirement in required:
        value = input(f"Enter {requirement}: ")
        context[requirement] = value
    return context
    
def check_requirements(asset_type):
    requirements = {
        'schema': ['name', 'type'],
        'path': ['path', 'method', 'operationId'],
        'response': ['statusCode', 'description'],
        'server': ['url'],
        'info': ['title', 'version'],
        'parameter': ['name', 'in']
    }
    return requirements.get(asset_type, [])
    
def check_version(version):
    if version != 'v2.0' and version != 'v3.0':
        raise ValueError("Version must be either 'v2.0' or 'v3.0'")

def generate_openapi_spec(project_name, version='v3.0', output_file='openapi_spec.yaml'):
    check_version(version)

    openapi_spec = {
        'openapi': '3.0.0' if version == 'v3.0' else '2.0',
        'info': {},
        'paths': {},
        'components': {
            'schemas': {},
            'parameters': {},
            'responses': {},
            'headers': {},
            'requestBodies': {},
            'securitySchemes': {}
        },
        'tags': [],
        'servers': []
    }

    if os.path.exists(os.path.join(project_name, "info", "info.yaml")):
        with open(os.path.join(project_name, "info", "info.yaml"), 'r') as f:
            openapi_spec['info'] = yaml.safe_load(f)

    for subdir, dirs, files in os.walk(project_name):
        for file in files:
            if file.endswith(".yaml"):
                with open(os.path.join(subdir, file), 'r') as f:
                    content = yaml.safe_load(f)

                if subdir.endswith("schemas"):
                    openapi_spec['components']['schemas'][file[:-5]] = content
                elif subdir.endswith("paths"):
                    openapi_spec['paths'].update(content)
                elif subdir.endswith("parameters"):
                    openapi_spec['components']['parameters'][file[:-5]] = content
                elif subdir.endswith("responses"):
                    openapi_spec['components']['responses'][file[:-5]] = content
                elif subdir.endswith("tags"):
                    openapi_spec['tags'].append(content)
                elif subdir.endswith("servers"):
                    openapi_spec['servers'].append(content)
                elif subdir.endswith("contacts"):
                    openapi_spec['info']['contact'] = content
                elif subdir.endswith("licenses"):
                    openapi_spec['info']['license'] = content

    with open(os.path.join(project_name, output_file), 'w') as f:
        yaml.dump(openapi_spec, f, sort_keys=False, default_flow_style=False)

def demo():
    print("Initializing demo project...")
    project_name = "demo_project"
    init_project(project_name)

    asset_types = ['info', 'server', 'schema', 'path', 'parameter', 'response']

    print("\nCreating OpenAPI assets...")
    for asset_type in asset_types:
        print(f"\nCreating {asset_type}...")
        context = build_context(asset_type)
        name = context.get('name', context.get('title', asset_type))
        sanitized_name = re.sub(r'\W+', '_', name)
        output_file = os.path.join(project_name, asset_type + "s", f"{sanitized_name}.yaml")
        render_template(asset_type, context, output_file)

    print("\nGenerating OpenAPI specification...")
    generate_openapi_spec(project_name)

    print("\nDemo complete. OpenAPI specification generated in 'demo_project/openapi_spec.yaml'")
