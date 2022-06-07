-- Deletar
	-- Tabelas
-- 		DROP TABLE IF EXISTS rastreio;
-- 		DROP TABLE IF EXISTS solicitacao_rastreio;
-- 		DROP TABLE IF EXISTS cpf;
-- 		DROP TABLE IF EXISTS solicitacao_cpf;
-- 		DROP TABLE IF EXISTS cnpj;
-- 		DROP TABLE IF EXISTS solicitacao_cnpj;
-- 		DROP TABLE IF EXISTS mensagem;
-- Criação das tabelas necessárias
	-- Tabela dos Rastreios 
		CREATE TABLE IF NOT EXISTS rastreio(
			id 			INTEGER PRIMARY KEY AUTOINCREMENT,
			codigo 		TEXT NOT NULL UNIQUE,
			informacoes TEXT NOT NULL,
			atualizacao TEXT NOT NULL	
		);
	-- Tabela das Solicitações de Rastreio
		CREATE TABLE IF NOT EXISTS solicitacao_rastreio(
			id 				INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user	 		INTEGER NOT NULL,
			id_rastreio 	INTEGER NOT NULL,
			nome_rastreio 	TEXT 	NOT NULL,
			FOREIGN KEY(id_rastreio) REFERENCES rastreio (id)
		);
	-- Tabela dos CPFs
		CREATE TABLE IF NOT EXISTS cpf(
			id 		INTEGER PRIMARY KEY AUTOINCREMENT,
			CPF 	TEXT 	NOT NULL UNIQUE,
			status 	TEXT 	NOT NULL
		);
	-- Tabela das Solicitações dos CPFs
		CREATE TABLE IF NOT EXISTS solicitacao_cpf(
			id 			INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 	INTEGER NOT NULL,
			id_cpf 		INTEGER NOT NULL,
			dia			TEXT	NOT NULL,
			FOREIGN KEY(id_cpf) REFERENCES cpf (id)
		);
	-- Tabela dos CNPJs
		CREATE TABLE IF NOT EXISTS cnpj(
			id 		INTEGER PRIMARY KEY AUTOINCREMENT,
			CNPJ 	TEXT 	NOT NULL UNIQUE,
			status 	TEXT 	NOT NULL
		);
	-- Tabela das Solicitações dos CNPJs
		CREATE TABLE IF NOT EXISTS solicitacao_cnpj(
			id 			INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 	INTEGER NOT NULL,
			id_cnpj 	INTEGER NOT NULL,
			dia			TEXT	NOT NULL,
			FOREIGN KEY(id_cnpj) REFERENCES cnpj (id)
		);
	-- Tabela das mensagens
		CREATE TABLE IF NOT EXISTS mensagem(
			id			 	INTEGER PRIMARY KEY AUTOINCREMENT,
			id_user 		INTEGER NOT NULL,
			dia 			TEXT	NOT NULL,
			log_mensagem 	TEXT 	NOT NULL
		);
-- Criação de index das tabelas
	-- Tabela dos Rastreios 
		CREATE INDEX  IF NOT EXISTS index_rastreio_id 		ON rastreio(id); 
		CREATE INDEX  IF NOT EXISTS index_rastreio_codigo 	ON rastreio(codigo);
	-- Tabela das Solicitações de Rastreios 
		CREATE INDEX  IF NOT EXISTS index_solicitacao_rastreio_id_user 		ON solicitacao_rastreio(id_user); 
		CREATE INDEX  IF NOT EXISTS index_solicitacao_rastreio_id_rastreio 	ON solicitacao_rastreio(id_rastreio);
	-- Tabela dos CPFs
		CREATE INDEX  IF NOT EXISTS index_cpf_id 		ON cpf(id); 
		CREATE INDEX  IF NOT EXISTS index_cpf_CPF		ON cpf(CPF);
		CREATE INDEX  IF NOT EXISTS index_cpf_status	ON cpf(status);
	-- Tabela das Solicitações de verificações de CPFs
		CREATE INDEX  IF NOT EXISTS index_cpf_id_user 	ON solicitacao_cpf(id_user); 
		CREATE INDEX  IF NOT EXISTS index_cpf_id_cpf 	ON solicitacao_cpf(id_cpf);
		CREATE INDEX  IF NOT EXISTS index_cpf_dia 		ON solicitacao_cpf(dia);
	-- Tabela dos CNPJs
		CREATE INDEX  IF NOT EXISTS index_cnpj_id 		ON cnpj(id); 
		CREATE INDEX  IF NOT EXISTS index_cnpj_CNPJ		ON cnpj(CNPJ);
		CREATE INDEX  IF NOT EXISTS index_cnpj_status	ON cnpj(status);
	-- Tabela das Solicitações de verificações de CNPJs
		CREATE INDEX  IF NOT EXISTS index_cnpj_id_user 	ON solicitacao_cnpj(id_user); 
		CREATE INDEX  IF NOT EXISTS index_cnpj_id_cnpj 	ON solicitacao_cnpj(id_cnpj);
		CREATE INDEX  IF NOT EXISTS index_cnpj_dia 		ON solicitacao_cnpj(dia);
	-- Tabela das mensagem;
		CREATE INDEX  IF NOT EXISTS index_mensagem_id_user 	ON mensagem(id_user);
		CREATE INDEX  IF NOT EXISTS index_mensagem_dia 		ON mensagem(dia);