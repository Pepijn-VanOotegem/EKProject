IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'VoetbalDWH')
BEGIN
  CREATE DATABASE VoetbalDWH;
END;
GO

USE [VoetbalDWH]

CREATE TABLE [dbo].[DimTime](
    TimeKey BIGINT NOT NULL,
    Tijdstip TIME NOT NULL,
	Uur INT NOT NULL,
	Minuut INT NOT NULL,
	PRIMARY KEY (TimeKey)
);


CREATE TABLE [dbo].[DimDate](
    DateKey BIGINT NOT NULL,
	[FullDateAlternateKey] [date] NOT NULL,
	[DayOfMonth] [varchar](2) NULL,
	[EnglishDayNameOfWeek] [varchar](10) NOT NULL,
	[DutchDayNameOfWeek] [varchar](10) NOT NULL,
	[DayOfWeek] [char](1) NULL,
	[DayOfWeekInMonth] [varchar](2) NULL,
	[DayOfWeekInYear] [varchar](2) NULL,
	[DayOfQuarter] [varchar](3) NULL,
	[DayOfYear] [varchar](3) NULL,
	[WeekOfMonth] [varchar](1) NULL,
	[WeekOfQuarter] [varchar](2) NULL,
	[WeekOfYear] [varchar](2) NULL,
	[Month] [varchar](2) NULL,
	[EnglishMonthName] [varchar](10) NOT NULL,
	[DutchMonthName] [varchar](10) NOT NULL,
	[MonthOfQuarter] [varchar](2) NULL,
	[Quarter] [char](1) NULL,
	[QuarterName] [varchar](9) NULL,
	[Year] [char](4) NULL,
	[MonthYear] [char](10) NULL,
	[MMYYYY] [char](6) NULL,
	PRIMARY KEY (DateKey)
);


CREATE TABLE [dbo].[DimTeam](
	TeamKey INT NOT NULL,
    Naam NVARCHAR(255) NOT NULL
	PRIMARY KEY (TeamKey)
);

CREATE TABLE [dbo].[DimType](
	TypeKey INT NOT NULL,
    TypeWedstrijd NVARCHAR(255) NOT NULL
	PRIMARY KEY (TypeKey)
);

CREATE TABLE [dbo].[FactMatchen](
    MactchKey BIGINT NOT NULL,
    DateKey BIGINT NOT NULL,
    TimeKey BIGINT NOT NULL,
	HomeTeamKey INT NOT NULL,
    AwayTeamKey INT NOT NULL,
	ScoreHome INT NOT NULL,
	ScoreAway INT NOT NULL,
    TypeKey INT NOT NULL,
	PRIMARY KEY (MactchKey),
	FOREIGN KEY (DateKey) REFERENCES [DimDate](DateKey),
	FOREIGN KEY (TimeKey) REFERENCES [DimTime](TimeKey),
	FOREIGN KEY (HomeTeamKey) REFERENCES [DimTeam](TeamKey),
	FOREIGN KEY (AwayTeamKey) REFERENCES [DimTeam](TeamKey),
    FOREIGN KEY (TypeKey) REFERENCES [DimType](TypeKey),
);
