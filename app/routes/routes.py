from fastapi import APIRouter, Query, HTTPException
from multiprocessing import Process, Manager
import asyncio
import time
import random 
from app.controllers.controllers import (
    get_users, get_wallets, get_transactions, 
    get_payment_methods, get_transaction_categories, 
    get_transaction_details, fetch_all_data, get_full_financial_info, 
)

router = APIRouter()

@router.get("/users")
def read_users():
    return get_users()

@router.get("/wallets")
def read_wallets():
    return get_wallets()

@router.get("/transactions")
def read_transactions():
    return get_transactions()

@router.get("/payment-methods")
def read_payment_methods():
    return get_payment_methods()

@router.get("/transaction-categories")
def read_transaction_categories():
    return get_transaction_categories()

@router.get("/transaction-details")
def read_transaction_details():
    return get_transaction_details()

@router.get("/fetch-all-data")
def read_all_data():
    data = fetch_all_data()
    return {"data": data}
##nuevooo
@router.get("/user/{user_id}/full-financial-info")
async def read_full_financial_info(user_id: int, skip: int = Query(0), limit: int = Query(10000)):
    return await get_full_financial_info(user_id, skip, limit)

async def measure_time_async(func, func_name, *args, **kwargs):
    start_time = time.perf_counter()  # Captura el tiempo de inicio
    result = await func(*args, **kwargs)  # Ejecuta la función asincrónicamente
    end_time = time.perf_counter()  # Captura el tiempo de fin
    execution_time = end_time - start_time  # Calcula el tiempo de ejecución
    print(f"tiempo de ejecucion {func_name}: {execution_time:.4f} segundos")  # Muestra el tiempo de ejecución
    return result

# Función auxiliar para agregar un retraso
async def delayed_function(func, delay, *args, **kwargs):
    await asyncio.sleep(delay)  # Aplica el retraso
    return await func(*args, **kwargs)  # Llama a la función original

@router.get("/consolidated-data/{user_id}")
async def get_consolidated_data(user_id: int, skip: int = 0, limit: int = 100):
    try:
        # Tiempo de inicio total
        start_time = time.perf_counter()

        # Llamar a todas las APIs en paralelo con tiempo de ejecución medido y un retraso
        results = await asyncio.gather(
          measure_time_async(delayed_function, "get_users", get_users, random.randint(1,10), user_id),  # Retraso de 2 segundos
         measure_time_async(delayed_function, "get_wallets", get_wallets, random.randint(1,10), user_id, skip, limit),  # Retraso de 3 segundos
         measure_time_async(delayed_function, "get_transactions", get_transactions, random.randint(1,10), user_id, skip, limit),  # Retraso de 1 segundo
         measure_time_async(delayed_function, "get_payment_methods", get_payment_methods, random.randint(1,10), user_id, skip, limit),  # Retraso de 2 segundos
         measure_time_async(delayed_function, "get_transaction_categories", get_transaction_categories, random.randint(1,10), skip, limit),  # Retraso de 1 segundo
         measure_time_async(delayed_function, "fetch_all_data", fetch_all_data, random.randint(1,10), skip, limit)  # Retraso de 1 segundo
        )

        # Tiempo de fin total
        end_time = time.perf_counter()
        total_execution_time = end_time - start_time

        print(f"Tiempo total de ejecución (asíncrono): {total_execution_time:.4f} segundos")

        # Procesar y devolver los resultados
        consolidated_data = {
            "user": results[0],
            "wallets": results[1],
            "transactions": results[2],
            "payment_methods": results[3],
            "transaction_categories": results[4],
            "all_data": results[5],
        }
        return consolidated_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consolidating data: {str(e)}")

# Multiprocessing
def get_data_in_process(func, params, result_dict, key):
    try:
        result_dict[key] = func(*params)  # Llamamos a la función y almacenamos el resultado en el diccionario
    except Exception as e:
        result_dict[key] = str(e)  # Si hay un error, almacenamos el error como string

@router.get("/consolidated-data1/{user_id}")
def get_consolidated_data(user_id: int, skip: int = 0, limit: int = 100):
    manager = Manager()
    result_dict = manager.dict()  # Usamos un diccionario compartido entre procesos
    processes = []

    try:
        # Crear y lanzar procesos para cada API
        processes.append(Process(target=get_data_in_process, args=(get_users, [user_id], result_dict, 'user')))
        processes.append(Process(target=get_data_in_process, args=(get_wallets, [user_id, skip, limit], result_dict, 'wallets')))
        processes.append(Process(target=get_data_in_process, args=(get_transactions, [user_id, skip, limit], result_dict, 'transactions')))
        processes.append(Process(target=get_data_in_process, args=(get_payment_methods, [user_id, skip, limit], result_dict, 'payment_methods')))
        processes.append(Process(target=get_data_in_process, args=(get_transaction_categories, [skip, limit], result_dict, 'transaction_categories')))
        processes.append(Process(target=get_data_in_process, args=(fetch_all_data, [skip, limit], result_dict, 'all_data')))

        # Iniciar todos los procesos
        for p in processes:
            p.start()

        # Esperar a que todos los procesos terminen
        for p in processes:
            p.join()

        # Consolidar los resultados
        consolidated_data = dict(result_dict)

        return consolidated_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consolidating data: {str(e)}")