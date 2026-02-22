import json

def main():
    with open("sample-data.json", "r") as f:
        data = json.load(f)

    interfaces = data["imdata"]

    print("Interface Status")
    print("=" * 90)
    print(f"{'DN':<55} {'Description':<15} {'Speed':<10} {'MTU':<5}")
    print("-" * 90)

    for item in interfaces:
        attributes = item["l1PhysIf"]["attributes"]

        dn = attributes["dn"]
        descr = attributes["descr"]
        speed = attributes["speed"]
        mtu = attributes["mtu"]

        print(f"{dn:<55} {descr:<15} {speed:<10} {mtu:<5}")

if __name__ == "__main__":
    main()