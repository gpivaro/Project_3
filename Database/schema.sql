-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- Table Scraped Data:

-- Remove table if it exists
DROP TABLE IF EXISTS realstatelisting CASCADE;

-- Create the table
CREATE TABLE realstatelisting(
	house_id SERIAL,
	price FLOAT NOT NULL,
	address VARCHAR(300) NOT NULL UNIQUE,
	house_link VARCHAR(300) NOT NULL,
	photolink VARCHAR(300) NOT NULL,
	latitude FLOAT,
	longitude FLOAT,
	PRIMARY KEY(house_id)
);

-- Table User Selection:

-- Remove table if it exists
DROP TABLE IF EXISTS userselection CASCADE;

-- Create the table
CREATE TABLE userselection(
	userselection_id SERIAL,
	username VARCHAR(300) NOT NULL,
	house_id INT NOT NULL,
	user_choice VARCHAR(300),
	PRIMARY KEY(userselection_id)
);
