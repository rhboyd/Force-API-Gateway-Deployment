
def handle_transform(template):
    """
    Go through template and find API gateway Deployments.
    """
    resources = template['Resources']
    hash_str = ""
    replacements_to_make = {}

    for resource_name, resource in resources.items():
        if resource['Type'].startswith("AWS::ApiGateway::"):
            hash_str = hash_str + str(resource)
    for resource_name, resource in resources.items():
        if resource['Type'] == "AWS::ApiGateway::Deployment" and 'Deploy' in resource:
            resource.pop('Deploy')
            replacements_to_make.update({resource_name: {"deployment{}".format(str(hash(hash_str))[-10:]): resource}})

    for resource_name, resource in replacements_to_make.items():
        resources.pop(resource_name)
        resources.update(resource)
    return template


def lambda_handler(event, _context):

    """Handle invocation in Lambda (when CloudFormation processes the Macro)"""
    fragment = event["fragment"]
    print("Fragment: {}".format(fragment))
    status = "success"

    try:
        fragment = handle_transform(fragment)
    except Exception as e:
        status = "failure"
        print("FAILED: {}".format(e))

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }
