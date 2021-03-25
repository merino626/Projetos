<h1>Como funciona o algoritmo BubbleSort? </h1>
<p>O algoritmo de BubbleSort funciona com dois laços aninhados e devido a isso possui a complexidade assintótica de O(N²), pois a lista é porcorrida 2 vezes para que possa ser feito as verificações e iterações.</p><br>
<p>O algoritmo passa pela lista fazendo verificações de duas posições até o final dela. O objetivo de fazer essas verificações de 2 em 2 até o final da lista é para que o maior
elemento daquela iteração possa ser levado ao fim da lista. No momento que o maior elemento de uma iteração é levado ao fim da lista, ele não será mais verificado. Ao final de uma iteração o BubbleSort sempre deixa o maior elemento posição final da iteração e automaticamente começa a próxima, mas já excluindo aqueles elementos que já são considerados como maiores. A imagem abaixo ilustra o algoritmo:</p>
<img src='https://user-images.githubusercontent.com/65437607/112512326-08e5d400-8d72-11eb-8986-5dc8e73813c0.png'>


