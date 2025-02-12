
CREATE DATABASE WalletDB;
GO


USE WalletDB;
GO

-- 3. Crear la tabla de usuarios
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    UserName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(256) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- 4. Crear la tabla de Wallets (Carteras de los usuarios)
CREATE TABLE Wallets (
    WalletID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    Balance DECIMAL(18,2) DEFAULT 0.00,
    Currency NVARCHAR(10) DEFAULT 'USD',
    CreatedAt DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Wallets_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
GO

-- 5. Crear la tabla de Transacciones
CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),
    WalletID INT NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    TransactionType NVARCHAR(50) NOT NULL, -- "Deposit", "Withdrawal", etc.
    Timestamp DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Transactions_Wallets FOREIGN KEY (WalletID) REFERENCES Wallets(WalletID) ON DELETE CASCADE
);
GO

-- 6. Crear la tabla de Métodos de Pago
CREATE TABLE PaymentMethods (
    PaymentMethodID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    MethodName NVARCHAR(50) NOT NULL, -- "Tarjeta de Crédito", "PayPal", etc.
    AccountNumber NVARCHAR(50) NOT NULL, -- Número de tarjeta o cuenta
    ExpiryDate DATE NOT NULL,
    IsDefault BIT DEFAULT 0, -- Indica si es el método de pago principal
    CreatedAt DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_PaymentMethods_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);
GO

-- 7. Crear la tabla de Categorías de Transacciones
CREATE TABLE TransactionCategories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(100) NOT NULL, -- "Compras", "Servicios", etc.
    Description NVARCHAR(255) NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);
GO

-- 8. Crear la tabla de Detalles de Transacciones
CREATE TABLE TransactionDetails (
    DetailID INT PRIMARY KEY IDENTITY(1,1),
    TransactionID INT NOT NULL,
    CategoryID INT NOT NULL,
    SubAmount DECIMAL(18,2) NOT NULL, -- Monto específico de esta categoría dentro de la transacción
    Note NVARCHAR(255) NULL, -- Nota o comentario sobre el detalle
    CreatedAt DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_TransactionDetails_Transactions FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID) ON DELETE CASCADE,
    CONSTRAINT FK_TransactionDetails_Categories FOREIGN KEY (CategoryID) REFERENCES TransactionCategories(CategoryID) ON DELETE CASCADE
);
GO

