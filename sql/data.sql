CREATE TABLE IF NOT EXISTS usuarios (
                                        id SERIAL PRIMARY KEY,
                                        username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
    );

INSERT INTO usuarios (id, username, email, password) VALUES
(1, 'rubi', 'rubi@gmail.com', 'rubi'),
(2, 'igna', 'igna@gmail.com', 'igna'),
(3, 'oska', 'oska@gmail.com', 'oska'),
(4, 'inma', 'inma@gmail.com', 'inma');