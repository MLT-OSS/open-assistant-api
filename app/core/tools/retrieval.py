from typing import Type, List

from pydantic import BaseModel, Field
from sqlmodel import Session

from app.core.doc_loaders import doc_loader
from app.core.tools.base_tool import BaseTool
from app.models.run import Run
from app.providers.storage import storage
from app.services.file.file import FileService


class RetrievalToolInput(BaseModel):
    file_keys: List[str] = Field(..., description="file key list to look up in retrieval")
    query: str = Field(..., description="query to look up in retrieval")


class RetrievalTool(BaseTool):
    name: str = "retrieval"
    description: str = (
        "Can be used to look up information that was uploaded to this assistant."
        "If the user is referencing particular files, that is often a good hint that information may be here."
    )

    args_schema: Type[BaseModel] = RetrievalToolInput

    def __init__(self) -> None:
        super().__init__()
        self.__files = []

    def configure(self, session: Session, run: Run, **kwargs):
        """
        置当前 Retrieval 涉及文件信息
        """
        self.__files = FileService.get_file_list_by_ids(session=session, file_ids=run.file_ids)

    def run(self, file_keys: List[str], query: str) -> dict:
        # TODO: 实现真正的 retrieval
        files = {}
        for file_key in file_keys:
            file_data = storage.load(file_key)
            # 截取前 1000 字符，防止超出 LLM 最大上下文限制
            files[file_key] = doc_loader.load(file_data)[:1000]

        return files

    def instruction_supplement(self) -> str:
        """
        为 Retrieval 提供文件选择信息，用于 llm 调用抉择
        """
        if len(self.__files) == 0:
            return ""
        else:
            filenames_info = [f"{file.filename}({file.key})" for file in self.__files]
            return (
                'You can use the "retrieval" tool to retrieve relevant context from the following attached files. '
                + 'Each line represents a file in the format "filename(file key)":\n'
                + "\n".join(filenames_info)
                + "\nMake sure to be extremely concise when using attached files. "
            )
