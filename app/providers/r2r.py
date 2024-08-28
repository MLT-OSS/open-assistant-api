from typing import Optional, Any

from r2r import R2RClient

from app.libs.util import verify_jwt_expiration
from config.llm import tool_settings


class R2R:
    client: R2RClient

    def init(self):
        self.client = R2RClient(tool_settings.R2R_BASE_URL)
        self.auth_enabled = tool_settings.R2R_USERNAME and tool_settings.R2R_PASSWORD
        self._login()

    def ingest_file(self, file_path: str, metadata: Optional[dict]):
        self._check_login()
        ingest_response = self.client.ingest_files(
            file_paths=[file_path],
            metadatas=[metadata] if metadata else None
        )
        return ingest_response.get("results")

    def search(self, query: str, filters: dict[str, Any]):
        self._check_login()
        search_response = self.client.search(
            query=query,
            vector_search_settings={
                "filters": filters,
                "search_limit": tool_settings.R2R_SEARCH_LIMIT,
                "do_hybrid_search": True
            },
        )
        return search_response.get("results").get("vector_search_results")

    def _login(self):
        if not self.auth_enabled:
            return
        self.client.login(tool_settings.R2R_USERNAME, tool_settings.R2R_PASSWORD)

    def _check_login(self):
        if not self.auth_enabled:
            return
        if verify_jwt_expiration(self.client.access_token):
            return
        if verify_jwt_expiration(self.client._refresh_token):
            self.client.refresh_access_token()
        else:
            self._login()


r2r = R2R()

r2r.init()
