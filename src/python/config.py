import os
import configparser

# Create config parser and expected path of config.cfg
config = configparser.ConfigParser()
filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.cfg")
logpath = os.path.join(os.path.dirname(filepath), "logs")

# Logs path
if not os.path.exists(logpath):
    os.makedirs(logpath)

# Create config file, write basic contents, set globals
if not os.path.exists(filepath):
    print("Path: {}".format(filepath))
    config["default"] = {
        "logpath" : r"{}".format(os.path.join(os.path.dirname(filepath), "logs"))
    }
    with open(filepath, "w") as fout:
        config.write(fout)

_ = config.read(filepath)

for i in config["default"]:
    print("global {} = {}".format(i, config["default"][i]))
    globals()[i] = config["default"][i]

if __name__ == "__main__":
    print("config.cfg configured")
