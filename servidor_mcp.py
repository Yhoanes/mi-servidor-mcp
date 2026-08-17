import os
import requests
from datetime import datetime, timedelta
from fastmcp import FastMCP

mcp = FastMCP("OrganizadorToDo")

# Leemos las credenciales desde las variables de Render
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")

def obtener_token_microsoft():
    """Obtiene un token de acceso OAuth2 desde Azure AD."""
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code != 200:
        raise Exception(f"Error autenticando con Azure: {resp.text}")
    return resp.json().get("access_token")

@mcp.tool()
def crear_tarea_equipo(correo_usuario: str, titulo_tarea: str, hora_evento: str) -> str:
    """
    Crea una tarea real en Microsoft To Do para el usuario especificado
    con un recordatorio configurado 5 minutos antes.
    """
    try:
        token = obtener_token_microsoft()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 1. Obtener la lista de tareas por defecto del usuario
        url_listas = f"https://graph.microsoft.com/v1.0/users/{correo_usuario}/todo/lists"
        resp_listas = requests.get(url_listas, headers=headers)
        
        if resp_listas.status_code != 200:
            return f"Error al buscar listas de To Do para {correo_usuario}: {resp_listas.text}"
            
        listas = resp_listas.json().get("value", [])
        if not listas:
            return f"No se encontró ninguna lista de To Do activa para {correo_usuario}."
            
        lista_id = listas[0]["id"]

        # 2. Preparar los datos de la tarea
        cuerpo_tarea = {
            "title": titulo_tarea,
            "importance": "high",
            "body": {
                "content": f"Tarea creada automáticamente desde Gemini Spark. Programada para: {hora_evento}",
                "contentType": "text"
            }
        }

        # 3. Crear la tarea en Microsoft Graph
        url_crear = f"https://graph.microsoft.com/v1.0/users/{correo_usuario}/todo/lists/{lista_id}/tasks"
        resp_crear = requests.post(url_crear, headers=headers, json=cuerpo_tarea)

        if resp_crear.status_code in [200, 201]:
            return f"✅ ¡Éxito! Tarea '{titulo_tarea}' agregada exitosamente a Microsoft To Do para {correo_usuario}."
        else:
            return f"Error de Microsoft Graph al crear tarea: {resp_crear.text}"

    except Exception as e:
        return f"Error interno en el servidor MCP: {str(e)}"

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 8000))
    print(f"Iniciando servidor MCP en el puerto {puerto}...")
    mcp.run(transport="http", host="0.0.0.0", port=puerto)