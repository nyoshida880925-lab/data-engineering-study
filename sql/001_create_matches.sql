CREATE TABLE IF NOT EXISTS matches (
    match_id BIGINT PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    home_goals INTEGER NOT NULL CHECK (home_goals >= 0),
    away_goals INTEGER NOT NULL CHECK (away_goals >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
