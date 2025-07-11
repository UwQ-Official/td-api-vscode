import xml.etree.ElementTree as ET
import json

xml_file = 'api.xml'  # Replace with your XML file
output_file = 'api.code-snippets'

tree = ET.parse(xml_file)
root = tree.getroot()

snippets = {}

for function in root.findall('function'):
    name = function.get('name')
    inputs = function.findall('input')
    outputs = function.findall('output')

    prefix = f"{name}"
    body = [f"{name}("]
    description = f"{name}("

    for i, input_param in enumerate(inputs):
        param_name = input_param.get('name')
        param_type = input_param.get('type')
        param_optional = input_param.get('optional')
        param_desc = input_param.get('desc')

        # Extract and increment the number within the placeholder
        placeholder_num = int(i) + 1  # Increment by 1
        body.append(f"${{{placeholder_num}:{param_name}}}")
        description += f"{param_name}: {param_type}"

        if i < len(inputs) - 1:
            body.append(", ")
            description += ", "

    body.append(")")
    description += ")"

    if outputs:
        body[0] = f"${{0:" + body[0] + "}}"

    snippets[name] = {
        "prefix": prefix,
        "body": ["".join(body)],
        "description": description,
    }

with open(output_file, 'w') as f:
    json.dump(snippets, f, indent=4)
    
print(f"Code snippets with incremented placeholders saved to {output_file}")
