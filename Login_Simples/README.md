<h1> Projeto de login simples </h1> <br>
<p> Este pequeno projeto consiste em uma tela de login feita em <strong>Python</strong>, utilizando a biblioteca <strong>Tkinter</strong>, que possibilita gerar interfaces gráficas a partir de um código python. Esta biblioteca já é nativa da linguagem, por isso decidi escolhe-la. </p> <br>

<h2> Objetivo principal do projeto </h2>
<p>O principal objetivo deste projeto é possuir um ambiente em que possa ser feito validações em uma tela de login, ou seja, fazer verificações de campos como <b>Apelido</b>, <b>Email</b> e <b>Senha</b>. Também é possível ver no projeto o conceito de <strong>orientação a objeto</strong>, pois decidi fazer a janela do "aplicativo" Tkinter a partir de uma classe, que possui seus respectivos métodos que validam os campos quando acionados.</p>
<br>

<ul>
  <li>
    <h3>1 - A interface </h3>
    <img src='https://user-images.githubusercontent.com/65437607/109542017-4755df00-7aa3-11eb-963b-5f1d1061364e.png'>
    <p>A interface consiste em uma tela muito simples de cadastro, com os campos necessários para a criação de uma conta. Logo após, na parte de baixo da mesma janela existe a         tela de login, na qual o usuário terá que usar os dados que acabou de cadastrar para se logar no sistema. </p>
  </li>
  
  <li>
    <h3>2 - Validação de apelido </h3>
    <img src='https://user-images.githubusercontent.com/65437607/109542619-07432c00-7aa4-11eb-8213-e6c3e5259e39.png'>
    <p> A primeira validação é referente ao campo <strong>apelido</strong>. Quando o usuário apenas digita um apelido, e logo em seguida clica no botão <strong>Confirmar </strong>
        o programa executa apenas a primeira validação. No caso da imagem a validação não foi satisfeita, pois o caractere '_'(underline) não é permitido como apelido válido.
    </p>
  </li>
  
   <li>
    <h3>3 - Validação do Email (Email em branco) </h3>
    <img src='https://user-images.githubusercontent.com/65437607/109543565-3908c280-7aa5-11eb-94a4-46fa301bec5b.png'>
    <p> 
      A segunda validação é feita a partir do campo <strong>Email</strong>. Nesta imagem o usuário informou um apelido válido, porém como deixou o campo de email em branco, o
      programa não indentificou nenhum caractere no campo, ocasionando a mensagem de erro que pede para o usuário informar um email.
    </p>
  </li>
  
   <li>
    <h3>4 - Validação do Email (Dominio do email inválido) </h3>
    <img src='https://user-images.githubusercontent.com/65437607/109544364-39ee2400-7aa6-11eb-955d-6b122c83b8fc.png'>
    <p> 
      Está validação ainda acontece no campo <strong>Email</strong>, porém desta vez ocasiona um erro devido ao dominio inválido digitado pelo usuario. Nestre programa
      um email considerado válido necessita ter apenas um caractere '@', e ao menos um caratere '.' após o arroba.
    </p>
  </li>
  
  
</ul>
