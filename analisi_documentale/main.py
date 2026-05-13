import asyncio
import os

from fastmcp import FastMCP
from ai_system import AISystem, SystemConfig


MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

mcp = FastMCP("ChatAgent")

chat_agent = None


@mcp.tool()
def ask_agent(query: str) -> str:
    """
    Agente alimentato da sistema RAG che risponde alle domande riguardo alle richieste evolutive sui seguenti progetti:
        - Consulcesi
    """
    if not chat_agent:
        raise RuntimeError("ChatAgent non inizializzato")
    return chat_agent.ask_agent(query)


if __name__ == '__main__':

    urls = [
        "test_files/DataTrust_Solutions_Report_Finanziario_2025.pdf",
        "test_files/DataTrust_Solutions_Report_Finanziario_2026.pdf",
        "test_files/Report_Finanziario_DataTrust_Solutions.pdf",
        "test_files/Raccolta-Requisiti-Evolutive-AdServer_v0.6.docx",
    ]
    tmp_dir = "temp_downloads"

    config = SystemConfig(
        repo_urls=urls,
        temp_download_dir=tmp_dir,
        enable_rag=True,
        max_input_tokens=20000,
        load_from_persist=False
    )
    ai_system = AISystem(config)

    async def setup():
        await ai_system.init_rag()
        global chat_agent
        from chat.agent import ChatAgent
        chat_agent = ChatAgent(rag_system=ai_system.rag_system, max_input_tokens=config.max_input_tokens)

    asyncio.run(setup())

    print(f"Starting MCP server on {MCP_HOST}:{MCP_PORT}")
    mcp.run(transport="sse", host=MCP_HOST, port=MCP_PORT)
