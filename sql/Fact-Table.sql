CREATE TABLE factsocialengagement (
    EngagementKey INT AUTO_INCREMENT PRIMARY KEY,
    CurrencyKey INT,
    PlatformKey INT,
    DateKey INT,
    Likes INT,
    Comments INT,
    Retweets INT,
    Score DECIMAL(10,4),
    FOREIGN KEY (CurrencyKey) REFERENCES dimcurrency(CurrencyKey),
    FOREIGN KEY (PlatformKey) REFERENCES dimplatform(PlatformKey),
    FOREIGN KEY (DateKey) REFERENCES dimdate(DateKey)
);
