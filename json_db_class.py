import json

class JSONTool():
    def load_db(self, url):
        with open(f"{url}", 'r') as f:
            try:
                db = json.load(f)
            except json.decoder.JSONDecodeError as e:
                return e, 'Empty JSON file'
        return db
    
    def save_db(self, url, db):
        with open(f"{url}", 'w') as f:
            f.write(json.dumps(db, indent=4, separators=(", ", " : "), ensure_ascii=False))