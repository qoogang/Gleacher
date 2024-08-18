import yaml

def load_openai_config(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)
        
    organization = config['openai']['organization']
    project_id = config['openai']['project_id']
    secret_id = config['openai']['secret_id']
    
    return organization, project_id, secret_id

if __name__ == "__main__":
    yaml_file = 'config.yaml'
    organization, PROJECT_ID, OPENAI_API_KEY = load_openai_config(yaml_file)
    if os.environ.get("OPENAI_API_KEY") is None:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY