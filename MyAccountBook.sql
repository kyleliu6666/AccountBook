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

CREATE TABLE MyAccountBook.TransactionTemplates (
    TemplateID INT AUTO_INCREMENT PRIMARY KEY,
    TemplateName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL, 
    Description VARCHAR(255),
    Amount DECIMAL(10, 2),
    TransactionType ENUM('Income', 'Expense') NOT NULL,
    PaymentMethod VARCHAR(50),
    Merchant VARCHAR(100),
    Location VARCHAR(100),
    AdditionalNotes VARCHAR(255)
);

INSERT INTO MyAccountBook.TransactionTemplates (TemplateName,Category, Amount, Description,TransactionType,PaymentMethod,Merchant,Location)
VALUES ('早餐1號','Food', 30, '地瓜+荷包蛋x2','Expense','Mobile Payments','員工餐廳','信義園區');

