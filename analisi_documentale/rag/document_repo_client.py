import os
import tempfile
import asyncio
import aiohttp
from app_logger import LoggerHandler
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

        self.app_logger = LoggerHandler().get_app_logger(__name__)

    async def load_repository(self, ):
        self.app_logger.debug(f"Loading repository from {self.urls}")
        try:
            tasks = [self.get_file(url) for url in self.urls]
            await asyncio.gather(*tasks)
            self.app_logger.info(f"Documents loaded from: {self.urls}")
            return self.downloaded_files

        except Exception as e:
            clean_directory(self.download_dir)
            self.app_logger.error(f"Error during repository load: {e}")
            raise Exception(f"Error loading repository: {e}")

    async def get_file(self, url, max_retries=3, retry_delay=2):
        assert len(url) > 0, "url must not be empty"
        self.app_logger.debug(f"Start download: {url}")

        for attempt in range(1, max_retries + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        content = await response.content.read()

                        tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=self.download_dir)
                        tmp_path = tmp_file.name

                        tmp_file.write(content)
                        tmp_file.close()

                        self.downloaded_files.append(tmp_path)
                        self.app_logger.debug(f"Document downloaded: {url}")
                        return tmp_path

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                self.app_logger.warning(f"Attempt {attempt}/{max_retries} failed for {url}: {e}")
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay * attempt)
                else:
                    self.app_logger.warning(f"All {max_retries} attempts failed for {url}")
                    raise Exception(f"All {max_retries} attempts failed for {url}")

    def cleanup_temp_files(self):
        self.app_logger.debug(f"Deleting temporary files: {self.downloaded_files}")
        try:
            for file in self.downloaded_files:
                if os.path.exists(file):
                    os.remove(file)
        except Exception as e:
            self.app_logger.error(f"Error during cleanup temporary files. Files: {self.downloaded_files}. Error:{e}")
