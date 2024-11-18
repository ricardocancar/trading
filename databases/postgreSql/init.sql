-- init.sql: Script de inicialización para crear la tabla 'users'

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Opcional: Insertar algunos datos de prueba
-- INSERT INTO users (username, email, hashed_password) VALUES
-- ('usuario1', 'usuario1@example.com', 'hashed_password_1'),
-- ('usuario2', 'usuario2@example.com', 'hashed_password_2');
