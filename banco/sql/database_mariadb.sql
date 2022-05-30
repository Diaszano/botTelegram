SET time_zone = 'America/Sao_Paulo';
-- Deletar
	-- Tabelas
-- 		DROP TABLE IF EXISTS mensagem;
-- 		DROP TABLE IF EXISTS cnpj;
-- 		DROP TABLE IF EXISTS cpf;
-- 		DROP TABLE IF EXISTS encomenda;
	-- Banco de dados
-- 		DROP DATABASE IF EXISTS bot_telegram;
-- Criação do Banco de Dados
	CREATE DATABASE IF NOT EXISTS bot_telegram;
	USE bot_telegram;
-- Criação das tabelas necessária
	-- Tabela das mensagens
		CREATE TABLE IF NOT EXISTS mensagem(
			id			 	INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user 		INT 		UNSIGNED NOT NULL,
			dia 			DATETIME	NOT NULL,
			log_mensagem 	LONGTEXT 	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela dos CNPJs
		CREATE TABLE IF NOT EXISTS cnpj(
			id			 	INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user 		INT 		UNSIGNED NOT NULL,
			dia 			DATETIME	NOT NULL,
			CNPJ			VARCHAR(14)	NOT NULL,
			status			VARCHAR(5)	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela dos CPFs
		CREATE TABLE IF NOT EXISTS cpf(
			id			 	INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user 		INT 		UNSIGNED NOT NULL,
			dia 			DATETIME	NOT NULL,
			CPF				VARCHAR(11)	NOT NULL,
			status			VARCHAR(5)	NOT NULL,
			PRIMARY KEY (id)
		);
	-- Tabela das Encomenda
		CREATE TABLE IF NOT EXISTS encomenda(
			id			 	INT 		UNSIGNED AUTO_INCREMENT NOT NULL,
			id_user 		INT 		UNSIGNED NOT NULL,
			codigo			VARCHAR(13)	NOT NULL,
			nome_rastreio	VARCHAR(30)	NOT NULL,
			dia 			DATETIME	NOT NULL,
			informacoes     LONGTEXT 	NOT NULL,
			PRIMARY KEY (id)
		);
-- Criação de index das tabelas
	-- Tabela das mensagem;
		CREATE INDEX index_mensagem_id_user ON mensagem(id_user);
		CREATE INDEX index_mensagem_dia 	ON mensagem(dia);
	-- Tabela dos CNPJs;
		CREATE INDEX index_cnpj_id_user ON cnpj(id_user);
		CREATE INDEX index_cnpj_CNPJ 	ON cnpj(CNPJ);
		CREATE INDEX index_cnpj_status 	ON cnpj(status);
	-- Tabela das solicitações;
		CREATE INDEX index_cpf_id_user 	ON cpf(id_user);
		CREATE INDEX index_cpf_CPF 		ON cpf(CPF);
		CREATE INDEX index_cpf_status 	ON cpf(status);
	-- Tabela dos dados dos clientes;
		CREATE INDEX index_encomenda_id_user 	ON encomenda(id_user);
		CREATE INDEX index_encomenda_codigo		ON encomenda(codigo);