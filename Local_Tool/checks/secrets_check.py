import os
import yaml
from detect_secrets.plugins.high_entropy_strings import HexHighEntropyString, Base64HighEntropyString
from detect_secrets.plugins.keyword import KeywordDetector

def load_config():
    """
    Loads the configuration file.
    """

    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yml')
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Konfigurationsdatei nicht gefunden: {config_path}")
    
    # read config file
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def check_credentials(files):
    errors = []

    config = load_config()

    # initialise plugins
    plugins = []
    if "HexHighEntropyString" in config["plugins"]:
        plugins.append(HexHighEntropyString())
    if "Base64HighEntropyString" in config["plugins"]:
        plugins.append(Base64HighEntropyString())
    if "KeywordDetector" in config["plugins"]:
        plugins.append(KeywordDetector())

    # Check each file for secrets
    for file in files:
        if not os.path.isfile(file):
            continue

        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    for plugin in plugins:
                        potential_secret = plugin.analyze_line(filename=file, line=line, line_number=line_num)
                        if potential_secret:
                            errors.append({
                                'file': file,
                                'line': line_num,
                                'message': f"Potenzielles Secret gefunden: {potential_secret}",
                            })
        except Exception as e:
            errors.append({
                'file': file,
                'message': f"Fehler beim Lesen der Datei: {str(e)}"
            })

    return errors
