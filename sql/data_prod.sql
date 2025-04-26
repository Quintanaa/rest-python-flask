CREATE TABLE IF NOT EXISTS usuarios (
                                        id SERIAL PRIMARY KEY,
                                        username VARCHAR(50) UNIQUE NOT NULL,
                                        email VARCHAR(100) UNIQUE NOT NULL,
                                        password VARCHAR(255) NOT NULL
);

INSERT INTO usuarios (id, username, email, password) VALUES
(1, 'rubi', 'rubi@gmail.com', 'rubi'),
(2, 'igna', 'igna@gmail.com', 'igna'),
(3, 'carl', 'carl@gmail.com', 'carl'),
(4, 'juan', 'juan@gmail.com', 'juan');
