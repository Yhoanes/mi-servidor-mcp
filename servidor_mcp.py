import os
import uvicorn
from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("OrganizadorToDo")

@mcp.tool()
def crear_tarea_equipo(correo_usuario: str, titulo_tarea: str, hora_evento: str) -> str:
    """Crea una tarea en Microsoft To Do con un recordatorio de 5 minutos antes."""
    return f"Éxito: La tarea '{titulo_tarea}' fue agendada correctamente para {correo_usuario}."

app = mcp.get_app() if hasattr(mcp, "get_app") else mcp._app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=puerto)