# Cálculo Numérico — Tema 2: Movimento Físico

Trabalho da disciplina de Cálculo Numérico (2026.2) — Ciências da Computação, UESPI, campus Floriano.
Profa. Suzana Matos França de Oliveira.

## Integrantes do grupo

- Renan Carlos de Sousa Pereira Lima
- Suelen Rodrigues Sá
- Leonarda Dias 

## Descrição do problema

Seja um movimento físico regido pela função:

```
f(d) = a * e^d - 4 * d²
```

onde `a` são amplitudes devido à oscilação encontrada em cada movimento considerado, e `d` é o
deslocamento encontrado em cada movimento, variando com o valor de `a`.

O objetivo é calcular o valor de `d` que zera a função, usando dois métodos numéricos, e analisar
para quais valores de `a` existe deslocamento.

## Métodos implementados

- **Bisseção**
- **Newton-Raphson**

Ambos herdam de uma classe abstrata comum (`MetodoNumerico`), seguindo o paradigma de programação
orientada a objetos.

## Diagrama de classes

<img width="2250" height="2058" alt="Image" src="https://github.com/user-attachments/assets/61ab7e8c-61ff-4729-ba86-f06ed2bf9cfd">

## Estrutura do código

- `MetodoNumerico`: classe abstrata base para os métodos numéricos.
- `Bissecao`: implementação do método da bisseção.
- `NewtonRaphson`: implementação do método de Newton-Raphson.
- `AnalisadorMovimento`: orquestra a execução dos métodos para cada movimento e imprime os
  resultados.
- `f(d, a)` e `f_prime(d, a)`: função do problema e sua derivada.

## Como executar

```bash
python Trabalho_Tema2.py
```

O programa solicita:

1. `n` — número de movimentos.
2. `a` — valor de `a` para cada movimento.
3. Início e fim do intervalo de isolamento.
4. `ε` — precisão desejada.

## Teste padrão

| Parâmetro    | Valor      |
|--------------|------------|
| a            | 1          |
| Isolamento   | (0, 1)     |
| ε (precisão) | 10⁻⁴       |

## Saída

Para cada movimento, o programa exibe:

- O isolamento (valores de `f` nas extremidades do intervalo e verificação de mudança de sinal).
- Para cada método (Bisseção e Newton-Raphson): tabela passo a passo das iterações e o valor de
  `d` calculado.

O critério de erro utilizado é o **erro relativo**.

## Análise da variação de `a`

Com f(0) = 1 e f(1) ≈ -1,28, há mudança de sinal no intervalo, garantindo que existe uma raiz isolada. Os dois métodos convergem para o mesmo valor de deslocamento, d ≈ 0,7148, confirmando a consistência da implementação.

A diferença está na velocidade de convergência: a Bisseção precisou de 14 iterações para atingir a precisão exigida, dividindo o intervalo ao meio a cada passo, de forma estável porém lenta. Já o Newton-Raphson convergiu em apenas 4 iterações, por usar a derivada da função para direcionar cada aproximação diretamente para a raiz.

## Repositório

https://github.com/renancarlos2004/c-lculo_num-rico_tema_2.git
