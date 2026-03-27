import json
import urllib.request
import sys
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dingtalk-table-webhooks.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_webhook_url(config, table_key="share_records"):
    tables = config.get("tables", {})
    table = tables.get(table_key)
    if not table:
        raise ValueError(f"Table '{table_key}' not found in config")
    
    webhook = table.get("webhook", {})
    env_key = webhook.get("env")
    if env_key:
        env_url = os.environ.get(env_key)
        if env_url:
            return env_url
    
    url = webhook.get("url")
    if url:
        return url
    
    raise ValueError(f"No webhook URL found for table '{table_key}'")

def send_webhook(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode("utf-8")
            return {"status": response.status, "body": json.loads(result)}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": json.loads(e.read().decode("utf-8"))}

def main():
    if len(sys.argv) < 2:
        print("Usage: python send_webhook.py <payload.json> [table_key]")
        print("Example: python send_webhook.py payload.json share_records")
        sys.exit(1)
    
    payload_path = sys.argv[1]
    table_key = sys.argv[2] if len(sys.argv) > 2 else "share_records"
    
    with open(payload_path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    
    config = load_config()
    webhook_url = get_webhook_url(config, table_key)
    
    print(f"Sending to table: {table_key}")
    print(f"Webhook URL: {webhook_url[:50]}...")
    
    result = send_webhook(webhook_url, payload)
    print(f"HTTP Status: {result['status']}")
    print(f"Response: {json.dumps(result['body'], ensure_ascii=False)}")
    
    if result['status'] == 200 and result['body'].get('success'):
        print("Success!")
    else:
        print("Failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
