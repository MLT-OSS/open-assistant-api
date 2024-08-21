from typing import Type, List

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.tools.base_tool import BaseTool
from app.models.run import Run
from app.services.file.file import FileService


class FileSearchToolInput(BaseModel):
    indexes: List[int] = Field(..., description="file index list to look up in retrieval")
    query: str = Field(..., description="query to look up in retrieval")


class FileSearchTool(BaseTool):
    name: str = "file_search"
    description: str = (
        "Can be used to look up information that was uploaded to this assistant."
        "If the user is referencing particular files, that is often a good hint that information may be here."
    )

    args_schema: Type[BaseModel] = FileSearchToolInput

    def __init__(self) -> None:
        super().__init__()
        self.__filenames = []
        self.__keys = []

    def configure(self, session: Session, run: Run, **kwargs):
        """
        置当前 Retrieval 涉及文件信息
        """
        files = FileService.get_file_list_by_ids(session=session, file_ids=run.file_ids)
        # pre-cache data to prevent thread conflicts that may occur later on.
        for file in files:
            self.__filenames.append(file.filename)
            self.__keys.append(file.key)

    def run(self, indexes: List[int], query: str) -> dict:
        file_keys = []
        for index in indexes:
            file_key = self.__keys[index]
            file_keys.append(file_key)

        files = FileService.search_in_files(query=query, file_keys=file_keys)
        return files

    def instruction_supplement(self) -> str:
        """
        为 Retrieval 提供文件选择信息，用于 llm 调用抉择
        """
        if len(self.__filenames) == 0:
            return ""
        else:
            filenames_info = [f"({index}){filename}" for index, filename in enumerate(self.__filenames)]
            return (
                'You can use the "retrieval" tool to retrieve relevant context from the following attached files. '
                + 'Each line represents a file in the format "(index)filename":\n'
                + "\n".join(filenames_info)
                + "\nMake sure to be extremely concise when using attached files. "
            )
