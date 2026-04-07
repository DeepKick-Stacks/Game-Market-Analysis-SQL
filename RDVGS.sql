-- 1. Create the Master Metadata Table
CREATE TABLE Game_Master_List (
    GameID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Platform VARCHAR(50),
    ReleaseYear INT,
    Genre VARCHAR(50),
    Publisher VARCHAR(100)
);

-- 2. Create the Sales Transaction Table
CREATE TABLE Sales_Transactions (
    SaleID INT PRIMARY KEY,
    GameID INT,
    UnitsSold INT,
    SaleDate DATE,
    FOREIGN KEY (GameID) REFERENCES Game_Master_List(GameID)
);

-- 3. Analysis: Categorizing Sales Performance (2010-2020)
SELECT 
    G.Title,
    G.ReleaseYear,
    T.UnitsSold,
    CASE 
        WHEN T.UnitsSold > 1000 THEN 'High Success'
        WHEN T.UnitsSold BETWEEN 1 AND 100 THEN 'Low Sales'
        ELSE 'Niche / Initial Launch'
    END AS Performance_Category
FROM Game_Master_List G
JOIN Sales_Transactions T ON G.GameID = T.GameID
WHERE G.ReleaseYear BETWEEN 2010 AND 2020
ORDER BY T.UnitsSold DESC;
CREATE TABLE 10yr_Video_Game_Sales (
GameID int PRIMARY KEY,
Title varchar(255) NOT NULL,
Platform varchar(50),
Releaseyear int,
Genre varchar(50),
Publisher varchar(100)
);

--2.creates the Sales tracking table
CREATE TABLE Transactions (
    SaleID int PRIMARY KEY,
    GameID int,
    UnitsSold int,
    SaleDate date,
    FOREIGN KEY (GameID) REFERENCES 10yr_Video_Game_Sales(GameID)
);

SELECT 
  G.Title,
  T.UnitsSold,
 CASE
   WHEN T.UnitsSold > 1000 THEN 'High Success'
   WHEN T.UnitsSold BETWEEN 1 AND 100 THEN 'Low Sales'
   ELSE 'No Sales / Flop'
  END AS 10yr_Video_Game_Sales G
  JOIN Transactions T ON G.GameID = T.GameID
  WHERE G.Releaseyear BETWEEN 2010 AND 2020;
