-- Apaga as tabelas ja existente.
-- Caution! Isso destroy todos os dados do banco.
drop table if exists item;
drop table if exists owner;

-- Criar a tabela 'owner'.

create table owner(
    owner_id integer primary key autoincrement,
    owner_date timestamp default current_timestamp,
    owner_name text,
    owner_email text,
    owner_password text,
    owner_birth date,
    owner_status text default 'on',
    owner_field1 text,
    owner_field2 text,
    owner_field3 text
);

-- Popular a tabela 'owner' com dados 'fake'.

INSERT INTO owner (owner_id, owner_date, owner_name, owner_email, owner_password,
 owner_birth, owner_status)

VALUES('1', '2023-09-13 15:23:15', 'Anderson Santos', 'anderson.programador@yahoo.com', '1234', '1988-01-15', 'on'),
('2', '2023-08-21 09:45:30', 'Lucas Silva', 'lucas.programador@example.com', 'senha456', '1992-07-18', 'off'),
('3', '2023-07-14 18:37:52', 'Ana Lima', 'ana.lima@gmail.com', 'senha789', '1985-04-20', 'on'),
('4', '2023-06-28 14:52:10', 'Fernanda Costa', 'fernanda.costa@outlook.com', 'senhaabc', '1998-11-10', 'off'),
('5', '2023-05-05 20:10:45', 'Rafael Souza', 'rafael.souza@example.com', 'senhaXYZ', '1987-03-25', 'on'),
('6', '2022-07-01 05:11:00', 'Leticia Lima', 'leticia.lima@example.com', '6789', '1986-08-11', 'off');


-- Criar a tabela 'item'.


create table item(
    item_id integer primary key autoincrement,
    item_date timestamp default current_timestamp,
    item_name text,
    item_description text,
    item_location text,
    item_owner integer,
    item_status text default 'on',
    item_field1 text,
    item_field2 text,
    item_field3 text,
	FOREIGN KEY (item_owner) references  owner (owner_id)
	
	);
	
	
	-- Popular tabela item.


INSERT INTO item (item_date, item_name, item_description, item_location, item_owner, item_status)

VALUES ('2023-09-13 15:23:15', 'Processador', 'intel i9 ', 'Em estoque', 1, 'on'),
    ('2023-08-21 09:45:30', 'Memoria ram', 'DDR5 hyperx', 'Esgotado', 2, 'off'),
    ('2023-07-14 18:37:52', 'M2mve 4Tb', 'M2mve', 'Em estoque', 3, 'on'),
    ('2023-06-28 14:52:10', 'Pl mae', 'Intel', 'Esgotado', 4, 'off'),
    ('2023-05-05 20:10:45', 'Fonte real', 'Fonte de valor real 800w', 'Em estoque', 5, 'on'),
	('2023-04-12 14:30:45', 'Placa de Vídeo GTX 1080', 'Placa de vídeo de alta performance', 'Em estoque', 6, 'on'),
	('2023-03-25 11:15:20', 'Monitor LED 27 polegadas', 'Monitor Full HD para computador', 'Esgotado', 1, 'off');
	


-- Cria a tabela 'contact'.

CREATE TABLE contact (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date DATETIME DEFAULT CURRENT_TIMESTAMP,
	name TEXT,
	email TEXT,
	subject TEXT,
	message TEXT,
	status TEXT DEFAULT 'received'
);