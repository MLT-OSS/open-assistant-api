from typing import Optional, Any

from r2r import R2RClient

from config.llm import tool_settings


class R2R:
    client: R2RClient

    def init(self):
        self.client = R2RClient(tool_settings.R2R_BASE_URL)
        # TODO: client login

    def ingest_file(self, file_path: str, metadata: Optional[dict]):
        ingest_response = self.client.ingest_files(
            file_paths=[file_path],
            metadatas=[metadata] if metadata else None
        )
        return ingest_response.get("results")

    def search(self, query: str, filters: dict[str, Any]):
        search_response = self.client.search(
            query=query,
            vector_search_settings={
                "filters": filters,
                "search_limit": 10,
                # TODO: support hybrid search
                # "do_hybrid_search": True
            },
            # TODO: support kg search
            # kg_search_settings={"use_kg_search": True}
        )
        return search_response.get("results").get("vector_search_results")


r2r = R2R()

r2r.init()
