--MyAccountBook
CREATE SCHEMA `MyAccountBook` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;


CREATE TABLE MyAccountBook.Transactions (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    TransactionDate DATE NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Description VARCHAR(255),
    Amount DECIMAL(10, 2) NOT NULL,
    TransactionType ENUM('Income', 'Expense') NOT NULL,
    PaymentMethod VARCHAR(50),
    Merchant VARCHAR(100),
    Location VARCHAR(100),
    ReceiptImage VARCHAR(255)
);
