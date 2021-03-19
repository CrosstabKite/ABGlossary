
import yaml

with open("terminology.yaml", "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
