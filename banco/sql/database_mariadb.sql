-- Deletar
	-- Banco de dados
-- 		DROP DATABASE IF EXISTS bot_telegram;
-- Criação do Banco de Dados
		CREATE DATABASE IF NOT EXISTS bot_telegram;
		USE bot_telegram;
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
			id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
			codigo			VARCHAR(13)	NOT NULL UNIQUE,
			informacoes     LONGTEXT 	NOT NULL,
			atualizacao 	DATETIME	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela das Solicitações de Rastreio
		CREATE TABLE IF NOT EXISTS solicitacao_rastreio(
		 	id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
		 	id_user			INT			UNSIGNED NOT NULL,
		 	id_rastreio		INT			UNSIGNED NOT NULL,
		 	nome_rastreio	VARCHAR(30)	NOT NULL,
		 	PRIMARY KEY (id)
		);
	-- Tabela dos CPFs
		CREATE TABLE IF NOT EXISTS cpf(
			id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
			CPF				VARCHAR(11)	NOT NULL UNIQUE,
			status			VARCHAR(5)	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela das Solicitações dos CPFs
		CREATE TABLE IF NOT EXISTS solicitacao_cpf(
		 	id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
		 	id_user			INT			UNSIGNED NOT NULL,
		 	id_cpf			INT			UNSIGNED NOT NULL,
		 	dia				DATETIME	NOT NULL,
		 	PRIMARY KEY (id)
		);
	-- Tabela dos CNPJs 	
		CREATE TABLE IF NOT EXISTS cnpj(
			id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
			CNPJ			VARCHAR(14)	NOT NULL UNIQUE,
			status			VARCHAR(5)	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela das Solicitações dos CNPJs
		CREATE TABLE IF NOT EXISTS solicitacao_cnpj(
		 	id				INT			UNSIGNED AUTO_INCREMENT NOT NULL,
		 	id_user			INT			UNSIGNED NOT NULL,
		 	id_cnpj			INT			UNSIGNED NOT NULL,
		 	dia				DATETIME	NOT NULL,
		 	PRIMARY KEY (id)
		);
	-- Tabela das mensagens
		CREATE TABLE IF NOT EXISTS mensagem(
			id			 	INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user 		INT 		UNSIGNED NOT NULL,
			dia 			DATETIME	NOT NULL,
			log_mensagem 	LONGTEXT 	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela do Horário do Remédio
		CREATE TABLE IF NOT EXISTS hora_do_remedio(
			id 			INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			hora 		VARCHAR(5)	NOT NULL UNIQUE,
			atualizacao VARCHAR(10)	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela das Solicitações do Horário do Remédio
		CREATE TABLE IF NOT EXISTS solicitacao_hora_do_remedio(
			id 				INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user	 		INT 		UNSIGNED NOT NULL,
			id_hora 		INT 		UNSIGNED NOT NULL,
			nome_remedio 	VARCHAR(30)	NOT NULL,
			PRIMARY KEY (id)
		);
-- Criação das referência necessárias
	-- Tabela das Solicitações de Rastreio
		ALTER TABLE solicitacao_rastreio 
		ADD FOREIGN KEY (id_rastreio) 
		REFERENCES rastreio(id);
	-- Tabela das Solicitações de verificações de CPFs
		ALTER TABLE solicitacao_cpf 
		ADD FOREIGN KEY (id_cpf) 
		REFERENCES cpf(id);
	-- Tabela das Solicitações de verificações de CNPJs
		ALTER TABLE solicitacao_cnpj 
		ADD FOREIGN KEY (id_cnpj) 
		REFERENCES cnpj(id);
	-- Tabela das Solicitações do Horário do Remédio
		ALTER TABLE solicitacao_hora_do_remedio
		ADD FOREIGN KEY(id_hora) 
		REFERENCES hora_do_remedio (id);
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
		CREATE INDEX IF NOT EXISTS index_mensagem_id_user 	ON mensagem(id_user);
		CREATE INDEX IF NOT EXISTS index_mensagem_dia 		ON mensagem(dia);
	-- Tabela do Horário do Remédio
		CREATE INDEX  IF NOT EXISTS index_hora_do_remedio_id 	ON hora_do_remedio(id);
		CREATE INDEX  IF NOT EXISTS index_hora_do_remedio_hora 	ON hora_do_remedio(hora);
	-- Tabela das Solicitações do Horário do Remédio
		CREATE INDEX  IF NOT EXISTS index_solicitacao_hora_do_remedio_id_user ON solicitacao_hora_do_remedio(id_user);
		CREATE INDEX  IF NOT EXISTS index_solicitacao_hora_do_remedio_id_hora ON solicitacao_hora_do_remedio(id_hora);