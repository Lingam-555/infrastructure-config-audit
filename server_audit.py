import json
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASELINE_FILE = os.path.join(BASE_DIR,"baseline.json")
SERVER_FILE = os.path.join(BASE_DIR,"servers.json")
LOG_FILE = os.path.join(BASE_DIR,"server_audit.log")
logging.basicConfig(
    filename = LOG_FILE,
    level = logging.INFO,
    format = "%(asctime)s %(levelname)-8s %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S"
)

def load_baseline():
        try:
            with open(BASELINE_FILE,"r") as file:
                data = json.load(file)
                if not isinstance(data,dict):
                    logging.error("Baseline file must be a dict")
                    return None
                if not data:
                    logging.error("Baseline file is empty")
                    return None
                return data
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON format: {e}")
            return None
        except FileNotFoundError as e:
            logging.error(f"Baseline file not found: {e}")
            return None
        
def load_servers():

    try:
        with open(SERVER_FILE,"r") as file:
            data = json.load(file)
            if not isinstance(data,dict):
                logging.error("server file must be a dict")
                return None
            if not data:
                logging.error("server file is empty")
                return None
            for server_name, actual_config in data.items():
                if not isinstance(actual_config,dict):
                    logging.error(f"Invalid server configuration: {server_name}")
                    return None
                if not actual_config:
                    logging.error(f"No config in {server_name}")
                    return None
            return data
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format: {e}")
        return None
    except FileNotFoundError as e:
        logging.error(f"server file doesn't exist: {e}")
        return None

def audit_server(actual_config,baseline):

    mismatches = []
    baseline_keys = set(baseline.keys())
    actual_keys = set(actual_config.keys())
    extra_settings = actual_keys - baseline_keys
    

    for setting,expected_value in baseline.items():

        actual_value = actual_config.get(setting)

        if setting not in actual_config:
            mismatches.append({
                "type": "MISSING",
                "setting": setting,
                "expected": expected_value
            })
            continue

        elif actual_value != expected_value:
            mismatches.append({
                "type": "MISMATCH",
                "setting": setting,
                "expected": expected_value,
                "actual": actual_value
            })

    for setting in extra_settings:
        actual_value = actual_config.get(setting)
        mismatches.append({
            "type": "EXTRA",
            "setting": setting,
            "actual": actual_value
        })

    return mismatches

def process_servers(servers,baseline):

    total_servers = 0
    compliant_count = 0
    non_compliant_count = 0
    results = []

    for server_name, actual_config in servers.items():

        total_servers += 1
        mismatches = audit_server(actual_config, baseline)

        if mismatches:
            status = "NON-COMPLIANT"
            non_compliant_count += 1
            results.append({
                "server": server_name,
                "status": status,
                "mismatches": mismatches
            })

        else:
            compliant_count += 1
            status = "COMPLIANT"
            results.append({
                "server": server_name,
                "status": status,
                "mismatches": []
            })

    final_result = {
        "total_servers": total_servers,
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "results": results
    }

    return final_result

def print_report(results):

    print("==== SERVER CONFIGURATION AUDIT ====")
    for result in results["results"]:
        if result["status"] == "NON-COMPLIANT":
            logging.warning(f"Server {result["server"]} is {result["status"]}")
            print(f"\nServer {result["server"]} is {result["status"]}")
        else:
            print(f"\nServer {result["server"]} is {result["status"]}")
        mismatches = result["mismatches"]
        if mismatches:
            for mismatch in mismatches:
                if mismatch["type"] == "MISMATCH":
                    logging.warning(f"{mismatch["type"]} : {mismatch['setting']}: expected={mismatch['expected']} actual={mismatch['actual']}")
                    print(f"{mismatch["type"]} : {mismatch['setting']}: expected={mismatch['expected']} actual={mismatch['actual']}")
                elif mismatch["type"] == "MISSING":
                    logging.warning(f"{mismatch["type"]} : {mismatch['setting']}: expected={mismatch['expected']}")
                    print(f"{mismatch["type"]} : {mismatch['setting']}: expected={mismatch['expected']}")
                else:
                    logging.warning(f"{mismatch["type"]} : {mismatch['setting']}: actual={mismatch['actual']}")
                    print(f"{mismatch["type"]} : {mismatch['setting']}: actual={mismatch['actual']}")

    print("\n==== SUMMARY ====")
    print(f"Total Servers: {results['total_servers']}")
    print(f"Compliant:{results['compliant_count']}")
    print(f"Non-Compliant: {results['non_compliant_count']}")

def main():

    baseline = load_baseline()
    servers = load_servers()

    if servers is None or baseline is None:
        raise SystemExit(1)

    result = process_servers(servers,baseline)
    print_report(result)
    
if __name__=="__main__":
    main()

