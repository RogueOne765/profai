import asyncio
from ai_system import AiSystem, SystemConfig


if __name__ == '__main__':

    urls = [
        "https://backoffice.lumsa.it/sites/default/files/file/3564/2024-06/Guida-per-lo-studente_12giugno_WEB_240612_113324.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/4252/2025-03/Linee%20guida%20prova%20finale%20LMG-01%20febbraio%202025.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/6/2023-07/Indicazioni%20tirocinio%20LM%2059.pdf",
        "https://backoffice.lumsa.it/sites/default/files/file/3564/2025-07/ELENCO%20ENTI%20CONVENZIONATI%20TIROCINIO.pdf"
    ]
    tmp_dir = "temp_downloads"

    config = SystemConfig(
        repo_urls=urls,
        temp_download_dir=tmp_dir,
        enable_rag=False,
        max_input_tokens=100
    )
    ay_system = AiSystem(config)

    asyncio.run(ay_system.start())
