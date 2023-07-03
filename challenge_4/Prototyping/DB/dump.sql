-- Drop existing tables (if they exist)
DROP TABLE IF EXISTS Trips;
DROP TABLE IF EXISTS Outage;
DROP TABLE IF EXISTS Schedule;
DROP TABLE IF EXISTS WaterLevel;
DROP TABLE IF EXISTS Captain;
DROP TABLE IF EXISTS Ferry;


-- Create Ferry table
CREATE TABLE IF NOT EXISTS Ferry (
  ID INT PRIMARY KEY,
  Name TEXT,
  Availability BOOLEAN
);

-- Create Captain table
CREATE TABLE IF NOT EXISTS Captain (
  ID INT PRIMARY KEY,
  Name TEXT,
  Availability BOOLEAN,
  FerryID INT,
  FOREIGN KEY (FerryID) REFERENCES Ferry(ID)
);

-- Create Outage table
CREATE TABLE IF NOT EXISTS Outage (
  ID INT PRIMARY KEY,
  FerryID INT,
  OutageDate DATE,
  FOREIGN KEY (FerryID) REFERENCES Ferry(ID)
);

-- Create Trips table
CREATE TABLE IF NOT EXISTS Trips (
  ID INT PRIMARY KEY,
  FerryID INT,
  CaptainID INT,
  DepartureTime TIME,
  FOREIGN KEY (FerryID) REFERENCES Ferry(ID),
  FOREIGN KEY (CaptainID) REFERENCES Captain(ID)
);

-- Create WaterLevel table
CREATE TABLE IF NOT EXISTS WaterLevel (
  ID INT PRIMARY KEY,
  Timestamp DATETIME,
  WaterLevel FLOAT
);

-- Create Schedule table
CREATE TABLE IF NOT EXISTS Schedule (
  ID INT PRIMARY KEY,
  FerryID INT,
  DepartureTime TIME,
  FOREIGN KEY (FerryID) REFERENCES Ferry(ID)
);
