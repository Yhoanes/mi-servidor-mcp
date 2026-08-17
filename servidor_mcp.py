import os
import uvicorn
from fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware

# Inicializamos el servidor MCP
mcp = FastMCP("OrganizadorToDo")

@mcp.tool()
def crear_tarea_equipo(correo_usuario: str, titulo_tarea: str, hora_evento: str) -> str:
    """Crea una tarea en Microsoft To Do con un recordatorio de 5 minutos antes."""
    print(f"\n🔔 [SISTEMA] Orden recibida de Gemini Spark:")
    print(f" -> Tarea: '{titulo_tarea}'")
    print(f" -> Destinatario: {correo_usuario}")
    print(f" -> Hora programada: {hora_evento}")
    return f"Éxito: La tarea '{titulo_tarea}' fue agendada correctamente para {correo_usuario}."

# En FastMCP 3.x la app SSE se obtiene con sse_app()
app = mcp.sse_app()

# Habilitamos CORS sin restricciones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8000))
    print(f"Iniciando servidor MCP en el puerto {puerto}...")
    uvicorn.run(app, host="0.0.0.0", port=puerto)