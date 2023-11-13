-- Apagar o banco de dados caso ele já exista.
drop database if exists db_items;

-- Criar o banco de dados com atenção á tabela de caracteres.
create database db_items 
	character set utf8mb4 
    collate utf8mb4_general_ci;
    
-- Selecionar o banco de dados.    
    use db_items;
    
    -- Criar tabela 'user' conforme o modelo.
    CREATE TABLE user (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_name VARCHAR(127) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(63) NOT NULL,
    user_birth DATE,
    user_status ENUM('on', 'off') DEFAULT 'on'
);

-- Inserir cadastros 'user'.
insert into user (user_name, user_email, user_password, user_birth) value
('Anderson Santos', 'anderson.programador@yahoo.com', '1020304050', '1988-01-15'),
('Mary Jane', 'Maryjane@juana.com', '123', '2000-11-13'),
('Patricia Silva', 'Putifera@sex.com', '12345', '1986-08-11');

-- Lista os cadastros feitos em 'user'.
select * from user where user_status='on';

-- Apagar cadastros.
update user set user_status='off' where user_id='1';
