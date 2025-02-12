from fastapi import FastAPI
from app.routes import router  # Importación relativa (asegúrate de que el proyecto esté correctamente configurado)
from app.database import create_pool  # Importa la función create_pool desde el módulo database
#from  routes import router  # Importación para docker
#from  database import create_pool  # importacion para docker 

# Crear la aplicación FastAPI
app = FastAPI()

# Incluir el router

app.include_router(router)

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    await create_pool()  # Asegúrate de que create_pool esté definida en database.py

# Ruta de inicio
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)