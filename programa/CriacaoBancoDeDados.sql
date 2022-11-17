create database db_acesso;

create table tb_usuario (
    id_usuario int primary key not null,
    nome_usuario varchar (45),
    imagem_codificada varchar (5000),
    nivel_acesso int
);