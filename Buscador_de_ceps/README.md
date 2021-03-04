<h1> Projeto Buscador de ceps </h1>
  <p>Este projeto consiste em uma simples interface feita em <strong>Python</strong> com o módulo <strong>PyQt5</strong>, onde o principal objetivo é demonstrar o uso de uma Api
  (mesmo que muito simples) de ceps, em que caso o cep sejá válido, o programa retornará campos do endereço como rua, uf, cidade e bairro. Caso o cep seja digitado errado, ou não existir,
  o retorno será "cep inválido"</p>
  
  <H2>O que o buscador faz na prática?</H2>
  <p>Na prática, através de uma requisição <strong>Http</strong> com o verbo "get" conseguimos passar o cep digitado pelo usuário junto com a requisição. A resposta desta requisição
  pode ser um <strong>Json</strong> com as informações do cep buscado(status code 200) ou apenas um erro devido ao cep ser inválido(status code 400). Há algumas situações em que mesmo
  um cep sendo inválido, o status code é 200, porém o programa lida com esses casos através da estrutura <strong>Try</strong>, <strong>except </strong> do python</p>.
  
  <ul>
    <li>
      <h3>1 - Tela inicial </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110001570-41563d00-7cf3-11eb-9e8b-27aa8a0696c2.png'>
      <p>Esta é a tela inicial após o programa ser executado. Consiste em uma tela simples e intuitiva com apenas 3 campos. O primeiro é o que o usuário deve fazer ("digite o cep"), o segundo é onde o usuário irá digitar o cep a ser buscado, e o terceiro é um botão onde usuário irá clicar para iniciar a busca. </p>
     </li>


<li>
      <h3>2 - Digitar o cep </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110002151-db1dea00-7cf3-11eb-85cd-ba6cd07dc95c.png'>
      <p>Assim que o usuário terminar de digitar um cep válido, apenas é preciso clicar no botão para obter as informações do cep. </p>
     </li>



  </ul>
