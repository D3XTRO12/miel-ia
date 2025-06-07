from ..dataclass.file_storage import FileStorage

class FileManagerBuilder:
    def __init__(self, filename: str, original_filename: str, file_type: str, file_size: int, description: str,
                 created_at: str, updated_at: str, user_id: str, session_id: str, tags: str, file_content_binary: bytes):
        self.file_storage = FileStorage()
        self.file_storage.filename = filename
        self.file_storage.original_filename = original_filename
        self.file_storage.file_type = file_type
        self.file_storage.file_size = file_size
        self.file_storage.description = description
        self.file_storage.created_at = created_at
        self.file_storage.updated_at = updated_at
        self.file_storage.user_id = user_id
        self.file_storage.session_id = session_id
        self.file_storage.tags = tags
        self.file_storage.file_content_binary = file_content_binary

    def build(self) -> FileStorage:
        """Construye y devuelve una instancia de FileStorage."""
        return self.file_storage