<h1>Como funciona o algoritmo BubbleSort? </h1>
<p>O algoritmo de BubbleSort funciona com dois laços aninhados e devido a isso possui a complexidade assintótica de O(N²), pois a lista é porcorrida 2 vezes para que possa ser feito as verificações e iterações.</p><br>
<p>O algoritmo passa pela lista fazendo verificações de duas posições até o final dela. O objetivo de fazer essas verificações de 2 em 2 até o final da lista é para que o maior
elemento daquela iteração possa ser levado ao fim da lista. No momento que o maior elemento de uma iteração é levado ao fim da lista, ele não será mais verificado. Ao final de uma iteração o BubbleSort sempre deixa o maior elemento na posição final da iteração e automaticamente começa a próxima, mas já excluindo aqueles elementos que já são considerados como maiores. A imagem abaixo ilustra o algoritmo:</p>
<img src='https://user-images.githubusercontent.com/65437607/112512326-08e5d400-8d72-11eb-8986-5dc8e73813c0.png'><br>
<p>Note que nesta imagem a iteração que ela está se referindo, são as iterações de verificação, ou seja, do laço <strong>FOR</strong> mais interno do algoritmo</p>

<br>
<img src='https://user-images.githubusercontent.com/65437607/112514007-a55ca600-8d73-11eb-9132-28813516ff91.png'>
<p>O laço <strong>FOR</strong> de fora é responsavel pelas iterações de fora, como visto na imagem acima. </p>
