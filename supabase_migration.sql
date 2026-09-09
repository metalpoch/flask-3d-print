-- =====================================================
-- Migracion a Supabase - Fooziman 3D Print
-- Ejecutar en el SQL Editor de Supabase Dashboard
-- =====================================================

-- Tabla de usuarios (admin login)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de mensajes de contacto
CREATE TABLE IF NOT EXISTS contact_messages (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de portafolio
CREATE TABLE IF NOT EXISTS portfolio_items (
    id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(140) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(500),
    fecha TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS (Row Level Security) pero con política abierta
-- ya que la app maneja auth por su cuenta
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_items ENABLE ROW LEVEL SECURITY;

-- Políticas: acceso completo con la service_role key
-- (la app usa la key publishable que tiene acceso completo via backend)
CREATE POLICY "Acceso total users" ON users FOR ALL USING (true);
CREATE POLICY "Acceso total contact_messages" ON contact_messages FOR ALL USING (true);
CREATE POLICY "Acceso total portfolio_items" ON portfolio_items FOR ALL USING (true);
