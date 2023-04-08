from pathlib import Path


def get_upload_to_path(instance, filename, field_name='username'):
    return Path(str(getattr(instance, field_name, instance.id))) / filename
