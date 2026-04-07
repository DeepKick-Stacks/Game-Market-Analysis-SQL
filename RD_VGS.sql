-- Creates the master list of video games
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
