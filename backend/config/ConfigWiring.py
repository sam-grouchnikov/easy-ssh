import json
import os


class AppConfig:
    def __init__(self, filename="user_data.json"):
        self.filename = filename
        self.data = self.load_initial()  # Load once on startup

    def load_initial(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass  # Fall back to defaults if file is corrupted

        defaults =  {
            "user": "",
            "sshcon": "",
            "sshport": "",
            "sshpsw": "",
            "wandbapi": "",
            "wandbuser": "",
            "wandbproj": "",
            "giturl": "",
            "gituser": "",
            "gitpat": "",
            "lastrun": "",
            "recentruns": [],
        }

        self.data = defaults
        self.save()
        return defaults

    def is_complete(self):
        for key, value in self.data.items():
            if key != "recentruns" and value == "":
                return False

        return True

    def get(self, key):
        return self.data.get(key, "")

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_run(self, run):
        self.data["recentruns"].append(run)
        self.save()

    def set_gpu_count_and_type(self, raw_output):
        split = raw_output.split("\n")
        self.data["gpucount"] = len(split)
        self.data["gputype"] = split[0]
        self.save()
