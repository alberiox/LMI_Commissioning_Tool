from PySide6 import QtCore

class TagStore(QtCore.QObject):
    updated = QtCore.Signal(dict)  # emits full dict snapshot

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tags = {}

    def set_many(self, updates: dict):
        self._tags.update(updates)
        self.updated.emit(dict(self._tags))

    def get(self, key: str, default=None):
        return self._tags.get(key, default)