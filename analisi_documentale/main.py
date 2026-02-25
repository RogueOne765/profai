import asyncio
import os

from ai_system import AISystem, SystemConfig


if __name__ == '__main__':

    urls = [
        "test_files/DataTrust_Solutions_Report_Finanziario_2025.pdf",
        "test_files/DataTrust_Solutions_Report_Finanziario_2026.pdf",
        "test_files/Report_Finanziario_DataTrust_Solutions.pdf",
    ]
    tmp_dir = "temp_downloads"

    config = SystemConfig(
        repo_urls=urls,
        temp_download_dir=tmp_dir,
        enable_rag=True,
        max_input_tokens=10000,
        load_from_persist=True
    )
    ay_system = AISystem(config)

    asyncio.run(ay_system.start())
