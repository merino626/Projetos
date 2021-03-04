<h1> Projeto Buscador de ceps </h1>
  <p>Este projeto consiste em uma simples interface feita em <strong>Python</strong> com o módulo <strong>PyQt5</strong>, onde o principal objetivo é demonstrar o uso de uma Api
  (mesmo que muito simples) de ceps, em que caso o cep sejá válido, o programa retornará campos do endereço como rua, uf, cidade e bairro. Casto o cep seja digitado errado, ou não existir
  o retorno será "cep inválido"</p>
  
  <H2>O que o buscador faz na prática?</H2>
  <p>Na prática, através de uma requisição <strong>Http</strong> com o verbo "get" conseguimos passar o cep digitado pelo usuário junto com a requisição. A resposta desta requisição
  pode ser um <strong>Json</strong> com as informações do cep buscado(status code 200) ou apenas um erro devido ao cep ser inválido(status code 400). Há algumas situações em que mesmo
  um cep sendo inválido, o status code é 200, porém o programa lida com esses casos através da estrutura <strong>Try</strong>, <strong>except </strong> do python</p>
