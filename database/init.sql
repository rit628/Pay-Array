CREATE TABLE household (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL
);

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash BINARY(32) NOT NULL,
    salt BINARY(32) NOT NULL,
    household_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    phone CHAR(10),
    balance DECIMAL(5,2) UNSIGNED,
    UNIQUE(username),
    FOREIGN KEY (household_id) REFERENCES household(id)
);

CREATE TABLE item (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(100),
    price DECIMAL(5,2) UNSIGNED,
    purchase_link VARCHAR(2048),
    UNIQUE(name)
);

CREATE TABLE transaction (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    amount DECIMAL(5,2) NOT NULL,
    completed BOOLEAN NOT NULL,
    item_id INT NOT NULL,
    purchaser_id INT NOT NULL
);

CREATE TABLE transaction_user (
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    balance DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    FOREIGN KEY (transaction_id) REFERENCES transaction(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE user_preference (
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (item_id) REFERENCES item(id)
);