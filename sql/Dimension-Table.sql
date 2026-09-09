CREATE TABLE dimcurrency (
    CurrencyKey INT AUTO_INCREMENT PRIMARY KEY,
    Symbol VARCHAR(20),
    Name VARCHAR(100),
    Supply DECIMAL(20,4),
    MarketCap DECIMAL(20,4),
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE dimdate (
    DateKey INT PRIMARY KEY,
    FullDate DATE,
    Year INT,
    Quarter INT,
    Month INT,
    Day INT
);
CREATE TABLE dimplatform (
    PlatformKey INT AUTO_INCREMENT PRIMARY KEY,
    PlatformName VARCHAR(50)
);
