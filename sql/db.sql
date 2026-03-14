CREATE DATABASE paymenys

/c paymenys

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passwordhash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user_to_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER NOT NULL REFERENCES user_roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE IF NOT EXISTS order_statuses (
    UUID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO order_statuses (name) VALUES ('paid'), ('unpaid'), ('partially_paid') ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY,
    user_id INT REFERENCES users(id),
    amount INT NOT NULL,
    status_id UUID NOT NUL REFERENCES payment_statuses(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS payment_statuses (
    UUID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO payment_statuses (name) VALUES ('pending'), ('completed'), ('cancelled'), ('refunded') ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS payment_types(
    UUID SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO payment_types (name) VALUES ('cash'), ('acquiring') ON CONFLICT (name) DO NOTHING;


CREATE TABLE IF NOT EXISTS paymenys (
    id UUID PRIMARY KEY,


CREATE TABLE IF NOT EXISTS auth_tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL UNIQUE,
    device_info TEXT NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL
);