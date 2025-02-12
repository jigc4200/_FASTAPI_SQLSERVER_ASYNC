from typing import List, Dict, Any
from fastapi import HTTPException
from app.database import get_db_connection, release_db_connection

async def fetch_data_async(query: str) -> List[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        cursor = await conn.cursor()
        await cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in await cursor.fetchall()]
        return results
    finally:
        await release_db_connection(conn)

async def fetch_all_data(skip: int = 0, limit: int = 10000):
    query = f"""
    SELECT 
        u.UserID, u.UserName, u.Email, u.CreatedAt AS UserCreatedAt,
        w.WalletID, w.Balance, w.Currency, w.CreatedAt AS WalletCreatedAt,
        t.TransactionID, t.Amount, t.TransactionType, t.Timestamp,
        pm.PaymentMethodID, pm.MethodName, pm.AccountNumber, pm.ExpiryDate, pm.IsDefault, pm.CreatedAt AS PaymentMethodCreatedAt,
        tc.CategoryID, tc.CategoryName, tc.Description, tc.CreatedAt AS CategoryCreatedAt,
        td.DetailID, td.SubAmount, td.Note, td.CreatedAt AS DetailCreatedAt
    FROM Users u
    LEFT JOIN Wallets w ON u.UserID = w.UserID
    LEFT JOIN Transactions t ON w.WalletID = t.WalletID
    LEFT JOIN PaymentMethods pm ON u.UserID = pm.UserID
    LEFT JOIN TransactionDetails td ON t.TransactionID = td.TransactionID
    LEFT JOIN TransactionCategories tc ON td.CategoryID = tc.CategoryID
    ORDER BY u.UserID
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY;
    """
    return await fetch_data_async(query)

# Individual queries
async def get_users(user_id: int):
    query = f"SELECT * FROM Users WHERE UserID = {user_id}"
    return await fetch_data_async(query)

async def get_wallets(user_id: int, skip: int = 0, limit: int = 100):
    query = f"""
    SELECT * FROM Wallets 
    WHERE UserID = {user_id} 
    ORDER BY WalletID 
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return await fetch_data_async(query)

async def get_transactions(user_id: int, skip: int = 0, limit: int = 100):
    query = f"""
    SELECT t.* FROM Transactions t
    JOIN Wallets w ON t.WalletID = w.WalletID
    WHERE w.UserID = {user_id}
    ORDER BY t.TransactionID
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return await fetch_data_async(query)

async def get_payment_methods(user_id: int, skip: int = 0, limit: int = 100):
    query = f"""
    SELECT * FROM PaymentMethods 
    WHERE UserID = {user_id} 
    ORDER BY PaymentMethodID 
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return await fetch_data_async(query)

async def get_transaction_categories(skip: int = 0, limit: int = 100):
    query = f"""
    SELECT * FROM TransactionCategories 
    ORDER BY CategoryID 
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return await fetch_data_async(query)

async def get_transaction_details(skip: int = 0, limit: int = 100):
    query = f"""
    SELECT * FROM TransactionDetails
    ORDER BY DetailID
    OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
    """
    return await fetch_data_async(query)

# Main function to fetch all data concurrently
async def get_full_financial_info(user_id: int, skip: int = 0, limit: int = 100):
    # Run all tasks concurrently
    results = await asyncio.gather(
        get_users(user_id),
        get_wallets(user_id, skip, limit),
        get_transactions(user_id, skip, limit),
        get_payment_methods(user_id, skip, limit),
        get_transaction_categories(skip, limit),
        return_exceptions=True  # Allow individual failures without stopping everything
    )

    # Handle errors individually
    if isinstance(results[0], Exception):
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": results[0],
        "wallets": results[1],
        "transactions": results[2],
        "payment_methods": results[3],
        "transaction_categories": results[4],
    }