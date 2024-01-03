from typing import Type
from config.storage import settings
from app.libs.class_loader import load_class
from app.services.file.impl.base import BaseFileService

FileService: Type[BaseFileService] = load_class(name=settings.FILE_SERVICE_MODULE)
