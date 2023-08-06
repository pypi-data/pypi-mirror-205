import toml

from xh_py_project_versioning.versioning import SemVer


class PyProject:
    def __init__(self, data: dict):
        self.data = data

    def get_dict(self):
        return self.data

    def get_project_name(self):
        return self.data["project"]["name"]

    def get_version(self):
        return self.data["project"]["version"]

    def update_version(self, sem_ver: SemVer) -> 'PyProject':
        self.data['project'].update({"version": str(sem_ver)})
        return self

    @staticmethod
    def from_toml(project_path: str) -> 'PyProject':
        d = toml.load(project_path)
        return PyProject(d)

    def persist(self, project_path: str) -> 'PyProject':
        with open(project_path, "w") as f:
            toml.dump(self.data, f)
        return self
