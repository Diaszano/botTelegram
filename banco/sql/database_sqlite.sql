-- Deletar
	-- Tabelas
-- 		DROP TABLE IF EXISTS mensagem;
-- 		DROP TABLE IF EXISTS cnpj;
-- 		DROP TABLE IF EXISTS cpf;
-- 		DROP TABLE IF EXISTS encomenda;
-- Criação das tabelas necessária
	-- Tabela das mensagens
		CREATE TABLE IF NOT EXISTS mensagem(
			id			 	INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 		INTEGER NOT NULL,
			dia 			TEXT	NOT NULL,
			log_mensagem 	TEXT 	NOT NULL);
	-- Tabela dos CNPJs
		CREATE TABLE IF NOT EXISTS cnpj(
			id			 	INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 		INTEGER NOT NULL,
			dia 			TEXT	NOT NULL,
			CNPJ			TEXT	NOT NULL,
			status			TEXT	NOT NULL);
	-- Tabela dos CPFs
		CREATE TABLE IF NOT EXISTS cpf(
			id			 	INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 		INTEGER NOT NULL,
			dia 			TEXT	NOT NULL,
			CPF				TEXT	NOT NULL,
			status			TEXT	NOT NULL);
	-- Tabela das Encomenda
		CREATE TABLE IF NOT EXISTS encomenda(
			id			 	INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 		INTEGER NOT NULL,
			codigo			TEXT	NOT NULL,
			nome_rastreio	TEXT	NOT NULL,
			dia 			TEXT	NOT NULL,
			informacoes     TEXT 	NOT NULL);
-- Criação de index das tabelas
	-- Tabela das mensagem;
		CREATE INDEX IF NOT EXISTS 	index_mensagem_id_user 	
									ON mensagem(id_user);
		CREATE INDEX IF NOT EXISTS 	index_mensagem_dia 		
									ON mensagem(dia);
	-- Tabela dos CNPJs;
		CREATE INDEX IF NOT EXISTS 	index_cnpj_id_user 	
									ON cnpj(id_user);
		CREATE INDEX IF NOT EXISTS 	index_cnpj_CNPJ 		
									ON cnpj(CNPJ);
		CREATE INDEX IF NOT EXISTS 	index_cnpj_status
									ON cnpj(status);
	-- Tabela dos CPFs;
		CREATE INDEX IF NOT EXISTS 	index_cpf_id_user 	
									ON cpf(id_user);
		CREATE INDEX IF NOT EXISTS 	index_cpf_CPF
									ON cpf(CPF);
		CREATE INDEX IF NOT EXISTS 	index_cpf_status
									ON cpf(status);
	-- Tabela das Encomendas;
		CREATE INDEX IF NOT EXISTS 	index_encomenda_id_user
									ON encomenda(id_user);
		CREATE INDEX IF NOT EXISTS 	index_encomenda_codigo
									ON encomenda(codigo);