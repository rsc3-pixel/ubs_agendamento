-- --------------------------------------------------------
-- SCRIPT DE INICIALIZAÇÃO DO BANCO DE DADOS - UBS_AGENDAMENTO
-- Versão MySQL: 8.0+
-- --------------------------------------------------------

-- 1. Cria o banco de dados (schema) se ele não existir
CREATE DATABASE IF NOT EXISTS ubs_agendamento;

-- 2. Define o banco de dados a ser usado para os comandos seguintes
USE ubs_agendamento;

-- 3. Cria a tabela Pacientes
CREATE TABLE Pacientes (
	paciente_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(255) NOT NULL,
	cpf VARCHAR(14) NOT NULL UNIQUE,
	data_nascimento DATE NOT NULL,
	telefone VARCHAR(15) NOT NULL,
	endereco TEXT 
);

-- 4. Cria a tabela Profissionais
CREATE TABLE Profissionais (
	profissional_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(255) NOT NULL,
	especialidade VARCHAR(255) NOT NULL,
	crm VARCHAR(10) NOT NULL UNIQUE
);

-- 5. Cria a tabela Consultas (com Foreign Keys)
CREATE TABLE Consultas (
	consulta_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	data DATE NOT NULL,
	hora TIME NOT NULL,
	status VARCHAR(50) NOT NULL,
	paciente_id INT NOT NULL,
    profissional_id INT NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(paciente_id),
    FOREIGN KEY (profissional_id) REFERENCES Profissionais(profissional_id)
);

-- 6. Opcional: Inserir dados de teste (ex: um profissional para começar)
-- INSERT INTO Profissionais (nome, especialidade, crm) VALUES ('Dr. João Silva', 'Clínico Geral', 'CRM/SP1234');