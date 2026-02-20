import os
import tempfile
import asyncio
import aiohttp

from utils import clean_directory


class DocumentRepositoryClient():
    """
    Classe per la gestione del download dei file. Vengono salvati in file
    temporanei e poi eliminati dopo l'ingestione del RAG
    """

    def __init__(self, urls, temp_dir="temp_downloads"):
        self.urls = urls
        self.download_dir = temp_dir
        self.downloaded_files = []
        os.makedirs(self.download_dir, exist_ok=True)

    async def load_repository(self,):
        try:
            tasks = [self.get_file(url) for url in self.urls]
            documents = await asyncio.gather(*tasks)
            return self.downloaded_files

        except Exception as e:
            clean_directory(self.download_dir)
            raise Exception(f"Error loading repository: {e}")

    async def get_file(self, url):
        assert len(url) > 0, "url must not be empty"
        print(f"Start download: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.content.read()

                tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=self.download_dir)
                tmp_path = tmp_file.name

                tmp_file.write(content)
                tmp_file.close()

                self.downloaded_files.append(tmp_path)
                print(f"Document downloaded: {url}")
                return tmp_path

    def cleanup_temp_files(self):
        for file in self.downloaded_files:
            if os.path.exists(file):
                os.remove(file)
