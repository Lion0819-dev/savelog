-- 外部キー制約を有効化
PRAGMA foreign_keys = ON;


-- 口座テーブル
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    note TEXT,
    create_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 貯金履歴テーブル
CREATE TABLE savings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    saved_date TEXT NOT NULL,
    memo TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (account_id)
        REFERENCES accounts(id)
        ON DELETE CASCADE
);

-- 検索・集計用インデックス
CREATE INDEX idx_savings_account_id
    ON savings(account_id);

CREATE INDEX idx_savings_saved_date
    ON savings(saved_date);