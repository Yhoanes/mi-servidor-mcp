import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("OrganizadorToDo")

# Pega aquí la URL exacta de Make
WEBHOOK_URL = "https://hook.us2.make.com/3nwwd709y0fb6a7s5ctifbxvvbh3bz7u"

@mcp.tool()
def crear_tarea_equipo(correo_usuario: str, titulo_tarea: str, hora_evento: str) -> str:
    """Crea una tarea en Microsoft To Do enviando los datos al webhook sincronizador."""
    payload = {
        "correo": correo_usuario,
        "titulo": titulo_tarea,
        "hora": hora_evento
    }
    
    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if resp.status_code in [200, 201, 204]:
            return f"✅ Tarea '{titulo_tarea}' creada y sincronizada exitosamente con Microsoft To Do."
        else:
            return f"Error al contactar webhook: {resp.text}"
    except Exception as e:
        return f"Error interno: {str(e)}"

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8000))
    print(f"Iniciando servidor MCP en el puerto {puerto}...")
    mcp.run(transport="http", host="0.0.0.0", port=puerto)