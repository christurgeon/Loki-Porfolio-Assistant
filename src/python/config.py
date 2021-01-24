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
    config["urls"] = {
        "arkk" : "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
        "arkq" : "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
        "arkw" : "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
        "arkg" : "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv",
        "arkf" : "https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv"
    }
    with open(filepath, "w") as fout:
        config.write(fout)

_ = config.read(filepath)

print("[default]")
for i in config["default"]:
    print("global {} = {}".format(i, config["default"][i]))
    globals()[i] = config["default"][i]
print("[urls]")
for i in config["urls"]:
    print("global {} = {}".format(i, config["urls"][i]))
    globals()[i] = config["urls"][i]

if __name__ == "__main__":
    print("config.cfg configured")
