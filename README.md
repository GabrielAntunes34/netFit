# **NetFit**

## Introdução

Este projeto da disciplina de Análise e Projeto Orientados a Objeto se empenha em desenvolver um dos casos de uso para o sistema web modelado ao longo nos diagramas e atividades práticas da disciplina. O objetivo da implementação era seguir o que foi descrito ao longo das atividades para garantir que até mesmo essa pequena parte concretizada do código do sistema apresentassem os principios do Paradigma Orientado a Objetos e outras boas práticas de design,como baixo acoplamento e alta coesão.

## Tema do projeto

Netfit foi modelado como um website para automatizar o gerenciamento de treinos e dietas de qualquer um que esteja interessado no mundo Fitness! Dessa forma, o sistema se desenvolveu em torno de 3 tipos de usuários: Entusiastas, que apenas buscam melhorar o gerenciamento de seues treinos e dietas, seja com ou sem orientação; personais, os quais buscam alunos para orientar, cadastrando exercícios e treinos específicos; e nutricionistas que, assim como o anterior, auxiliam e fornecem opções de dieta para os entusiastas. 

Nesse sentido, varios casos de uso com diferentes funcionalidades foram modelados, oferecendo praticidades e restrições para os três tipos de usuário.

## O caso de uso modelado

Por ser complexo e envolver diferentes entidades do sistema proposto, escolhemos implementar o caso de uso "Montar Treino". Este pode ser efetuado tanto por entusiastas quanto personais cadastrados no site. O primeiro grupo sempre pode montar um treino, a partir das séries e exercícios já cadastrados no banco de dados do site; já o segundo grupo só é efetivamente capaz de fazê-lo quando já possui um aluno que o adcionou como personal associado. Além disso, o fim do processo sempre resulta na página de treinos ativos para o entusiasta em questão.

## Dependências do projeto
- Python3
- SQL Lite
- Framework Django

## Como executar

Com o ambiente devidamente configurado, inicia-se a execução entrando na pasta do projeto e rodando o comendo:

```
python3 manage.py runserver
```

A partir disso, pode-se cadastrar ou logar em um usuário e testar o caso de uso preenchendo os formulários. Para testar a criação por parte do personal, deixamos dois usuários já cadastrados no site: 

Entusiasta:
- username: Bruno Lima
- senha: 123
  
Personal:
- username: Bruno Lima 2
- senha: 123
