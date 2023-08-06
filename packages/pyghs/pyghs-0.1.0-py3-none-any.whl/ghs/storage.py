import base64
import io
import json

import aiohttp
import pandas as pd


class GHS:
    def __init__(
        self,
        access_token: str,
        repository: str,
    ) -> None:
        self.repository = repository
        self._session = self._get_session(access_token)

    async def create(self, path: str, df: pd.DataFrame) -> None:
        csv = df.to_csv(index=False)
        payload = {
            "message": "Create",
            "content": base64.b64encode(csv.encode()).decode(),
        }
        async with self._session.put(
            f"/repos/{self.repository}/contents/{path}", data=json.dumps(payload)
        ) as r:
            try:
                r.raise_for_status()
            except aiohttp.ClientResponseError as e:
                if e.status == 422:
                    raise FileExistsError(
                        f"File {path} already exists in repository {self.repository}"
                    )
                raise

    async def get(self, path: str) -> pd.DataFrame:
        async with self._session.get(f"/repos/{self.repository}/contents/{path}") as r:
            r.raise_for_status()
            rv = await r.json()
            csv = base64.b64decode(rv["content"])
            return pd.read_csv(io.BytesIO(csv))

    async def update(self, path: str, df: pd.DataFrame, upsert: bool = True) -> None:
        try:
            sha = await self.get_sha(path)
        except FileNotFoundError:
            if upsert:
                await self.create(path, df)
                return
            raise
        csv = df.to_csv(index=False)
        payload = {
            "message": "Update",
            "sha": sha,
            "content": base64.b64encode(csv.encode()).decode(),
        }
        async with self._session.put(
            f"/repos/{self.repository}/contents/{path}", data=json.dumps(payload)
        ) as r:
            try:
                r.raise_for_status()
            except aiohttp.ClientResponseError as e:
                if e.status == 422:
                    raise FileNotFoundError(
                        f"File {path} does not exist in repository {self.repository}"
                    )
                raise

    async def delete(self, path: str) -> None:
        sha = await self.get_sha(path)
        async with self._session.delete(
            f"/repos/{self.repository}/contents/{path}",
            data=json.dumps({"message": "Delete", "sha": sha}),
        ) as r:
            try:
                r.raise_for_status()
            except aiohttp.ClientResponseError as e:
                if e.status == 404:
                    raise FileNotFoundError(
                        f"File {path} does not exist in repository {self.repository}"
                    )
                raise

    async def objects(self) -> list[str]:
        async with self._session.get(f"/repos/{self.repository}/contents") as r:
            r.raise_for_status()
            return [item["name"] for item in await r.json()]

    async def get_sha(self, path: str) -> str:
        async with self._session.get(f"/repos/{self.repository}/contents/{path}") as r:
            try:
                r.raise_for_status()
            except aiohttp.ClientResponseError as e:
                if e.status == 404:
                    raise FileNotFoundError(
                        f"File {path} does not exist in repository {self.repository}"
                    )
                raise
            rv = await r.json()
            return rv["sha"]

    @staticmethod
    def _get_session(access_token: str) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {access_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            base_url="https://api.github.com",
        )

    async def close(self) -> None:
        await self._session.close()

    async def __aenter__(self) -> "GHS":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()
