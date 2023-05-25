CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL NOT NULL, 
    symbol VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    price_close DECIMAL NOT NULL,
    current_price DECIMAL NOT NULL,
    fiftyDayAverage DECIMAL NOT NULL,
    change DECIMAL NOT NULL,
    percent_change DECIMAL NOT NULL,
    date_created TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc') NOT NULL,
    PRIMARY KEY (symbol)
 );
