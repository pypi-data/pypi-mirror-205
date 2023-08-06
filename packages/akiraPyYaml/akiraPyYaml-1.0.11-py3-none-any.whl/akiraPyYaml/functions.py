def read_yaml_from_file(file: str):
    """Opens a file in yaml format and returns an object with the data.
        Args:
            file: (str)
        
        Returns:
            yaml data
    """

    with open(file, 'r') as o_file:
        import yaml
        yaml_data = yaml.safe_load(o_file)
    return yaml_data
