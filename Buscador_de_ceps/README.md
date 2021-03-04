<h1> Projeto Buscador de ceps </h1>
  <p>Este projeto consiste em uma simples interface feita em <strong>Python</strong> com o módulo <strong>PyQt5</strong>, onde o principal objetivo é demonstrar o uso de uma Api
  (mesmo que muito simples) de ceps, em que caso o cep sejá válido, o programa retornará campos do endereço como rua, uf, cidade e bairro. Caso o cep seja digitado errado, ou não existir,
  o retorno será "cep inválido"</p>
  
  <H2>O que o buscador faz na prática?</H2>
  <p>Na prática, através de uma requisição <strong>Http</strong> com o verbo "get" conseguimos passar o cep digitado pelo usuário junto com a requisição. A resposta desta requisição
  pode ser um <strong>Json</strong> com as informações do cep buscado(status code 200) ou apenas um erro devido ao cep ser inválido(status code 400). Há algumas situações em que mesmo
  um cep sendo inválido, o status code é 200, porém o programa lida com esses casos através da estrutura <strong>Try</strong>, <strong>except </strong> do python.</p>
  
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

<li>
      <h3>3 - Informações do cep </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110002333-06a0d480-7cf4-11eb-9564-61184a04398c.png'>
      <p>Após clicar no botão, haverá um popUp em uma nova janela em que aparecerão as informações provenientes do cep, sendo respectivamente: cidade, uf, rua e bairro. Caso o 
  usuário feche este popUp, ele retornará a tela de buscar o cep novamente para que ele possa fazer outras buscas.  </p>
     </li>

<li>
      <h3>4 - Cep inválido </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110002764-84fd7680-7cf4-11eb-97f1-9930f3d9c47e.png'>
      <p>Nem sempre o cep digitado pelo usuário será um cep válido.</p>
     </li>

<li>
      <h3>5 - Cep não encontrado </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110002989-b6764200-7cf4-11eb-84e2-6dc85dd1e07c.png'>
      <p>Quando o usúario tenta buscar um cep que não existe, ou que é inválido, o programa mostra que o cep é inválido, pois após fazer a requisição ao site de ceps ele não
  obteve um retorno esperado.</p>
     </li>

<li>
      <h3>6 - Buscar novamente </h3>
      <img src='https://user-images.githubusercontent.com/65437607/110003431-2258aa80-7cf5-11eb-880a-9be96efc81f7.png'>
      <p>Depois que o usuário teve sucesso ou não na busca do cep, ele pode fechar o PopUp e buscar novamente algum outro cep.</p>
     </li>
  </ul>
  
  
<h3>Considerações finais</h3>
<p>Este projeto é um projeto bem pequeno, porém decidi postar ele separado no github, mas pretendo usar ele em alguns outros projetos maiores que precisem fazer busca de cep. </p>
