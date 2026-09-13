import math
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any, Tuple


# =============================================================================
# CLASSE BASE DOS MÉTODOS NUMÉRICOS
# =============================================================================

class MetodoNumerico(ABC):
    """
    Classe abstrata para os métodos numéricos utilizados no trabalho.
    """

    def __init__(
        self,
        f: Callable[[float, float], float],
        precisao: float
    ):
        self.f = f
        self.precisao = precisao

    @abstractmethod
    def executar(
        self,
        a: float,
        intervalo: Tuple[float, float]
    ) -> Dict[str, Any]:
        """
        Executa o método numérico e retorna os resultados.
        """
        pass


# =============================================================================
# MÉTODO DA BISSEÇÃO
# =============================================================================

class Bissecao(MetodoNumerico):
    """
    Implementação do Método da Bisseção.

    O método divide o intervalo ao meio e mantém
    o subintervalo que contém a raiz.
    """

    def executar(
        self,
        a: float,
        intervalo: Tuple[float, float]
    ) -> Dict[str, Any]:

        inicio, fim = intervalo

        # Calcula os valores da função nas extremidades
        f_inicio = self.f(inicio, a)
        f_fim = self.f(fim, a)

        # Verifica se existe mudança de sinal
        if f_inicio * f_fim > 0:
            raise ValueError(
                f"O intervalo [{inicio}, {fim}] não isola uma raiz."
            )

        historico = []

        # Valor anterior utilizado para calcular o erro relativo
        anterior = None

        k = 1

        while True:

            # Calcula o ponto médio
            d = (inicio + fim) / 2

            # Calcula a função no ponto médio
            f_d = self.f(d, a)

            # ---------------------------------------------------------------
            # Cálculo do erro relativo
            # ---------------------------------------------------------------

            if anterior is None:
                erro = None

            elif d != 0:
                erro = abs(d - anterior) / abs(d)

            else:
                erro = abs(d - anterior)

            # ---------------------------------------------------------------
            # Guarda os dados da iteração
            # ---------------------------------------------------------------

            historico.append({
                "k": k,
                "a_k": inicio,
                "b_k": fim,
                "d_k": d,
                "f(d_k)": f_d,
                "erro_relativo": erro
            })

            # ---------------------------------------------------------------
            # Critérios de parada
            # ---------------------------------------------------------------

            if abs(f_d) < self.precisao:
                break

            if erro is not None and erro < self.precisao:
                break

            # ---------------------------------------------------------------
            # Atualiza o intervalo
            # ---------------------------------------------------------------

            if f_inicio * f_d < 0:

                fim = d
                f_fim = f_d

            else:

                inicio = d
                f_inicio = f_d

            # Guarda o valor atual para a próxima iteração
            anterior = d

            k += 1

        return {
            "raiz": d,
            "historico": historico
        }


# =============================================================================
# MÉTODO DE NEWTON-RAPHSON
# =============================================================================

class NewtonRaphson(MetodoNumerico):
    """
    Implementação do Método de Newton-Raphson.

    Fórmula:

        d_(k+1) = d_k - f(d_k) / f'(d_k)
    """

    def __init__(
        self,
        f: Callable[[float, float], float],
        f_prime: Callable[[float, float], float],
        precisao: float
    ):

        super().__init__(f, precisao)

        self.f_prime = f_prime

    def executar(
        self,
        a: float,
        intervalo: Tuple[float, float]
    ) -> Dict[str, Any]:

        inicio, fim = intervalo

        # Utiliza o ponto médio do isolamento como aproximação inicial
        d = (inicio + fim) / 2

        historico = []

        k = 1

        while True:

            # Calcula f(d)
            f_d = self.f(d, a)

            # Calcula f'(d)
            f_prime_d = self.f_prime(d, a)

            # Verifica se a derivada é zero
            if f_prime_d == 0:
                raise ValueError(
                    "A derivada é zero. "
                    "O método de Newton-Raphson não pode continuar."
                )

            # ---------------------------------------------------------------
            # Fórmula de Newton-Raphson
            # ---------------------------------------------------------------

            d_novo = d - (f_d / f_prime_d)

            # ---------------------------------------------------------------
            # Cálculo do erro relativo
            # ---------------------------------------------------------------

            if d_novo != 0:

                erro = abs(d_novo - d) / abs(d_novo)

            else:

                erro = abs(d_novo - d)

            # ---------------------------------------------------------------
            # Guarda os dados da iteração
            # ---------------------------------------------------------------

            historico.append({
                "k": k,
                "d_k": d,
                "f(d_k)": f_d,
                "f'(d_k)": f_prime_d,
                "d_(k+1)": d_novo,
                "erro_relativo": erro
            })

            # ---------------------------------------------------------------
            # Critérios de parada
            # ---------------------------------------------------------------

            if abs(f_d) < self.precisao:

                d = d_novo
                break

            if erro < self.precisao:

                d = d_novo
                break

            # Próxima iteração
            d = d_novo

            k += 1

        return {
            "raiz": d,
            "historico": historico
        }


# =============================================================================
# ANALISADOR DO MOVIMENTO
# =============================================================================

class AnalisadorMovimento:
    """
    Classe responsável por executar os métodos numéricos
    para cada movimento e mostrar os resultados.
    """

    def __init__(
        self,
        f: Callable[[float, float], float],
        f_prime: Callable[[float, float], float]
    ):

        self.f = f
        self.f_prime = f_prime

    # -------------------------------------------------------------------------
    # VERIFICAÇÃO DO ISOLAMENTO
    # -------------------------------------------------------------------------

    def verificar_isolamento(
        self,
        a: float,
        intervalo: Tuple[float, float]
    ) -> bool:

        inicio, fim = intervalo

        f_inicio = self.f(inicio, a)
        f_fim = self.f(fim, a)

        # Existe mudança de sinal?
        return f_inicio * f_fim <= 0

    # -------------------------------------------------------------------------
    # IMPRESSÃO DA TABELA
    # -------------------------------------------------------------------------

    @staticmethod
    def imprimir_tabela(
        historico: List[Dict[str, Any]]
    ):

        if not historico:
            return

        colunas = list(historico[0].keys())

        print("-" * 115)

        print(
            " | ".join(
                f"{coluna:^17}"
                for coluna in colunas
            )
        )

        print("-" * 115)

        for linha in historico:

            valores = []

            for coluna in colunas:

                valor = linha[coluna]

                if valor is None:

                    texto = "-"

                elif isinstance(valor, float):

                    texto = f"{valor:.8f}"

                else:

                    texto = str(valor)

                valores.append(
                    f"{texto:^17}"
                )

            print(" | ".join(valores))

        print("-" * 115)

    # -------------------------------------------------------------------------
    # EXECUÇÃO DA ANÁLISE
    # -------------------------------------------------------------------------

    def executar(
        self,
        lista_a: List[float],
        intervalo: Tuple[float, float],
        precisao: float
    ):

        print("\n")
        print("=" * 80)
        print("        TEMA 2 - ANÁLISE DE MOVIMENTO FÍSICO")
        print("=" * 80)

        print(f"Isolamento utilizado: {intervalo}")
        print(f"Precisão (ε): {precisao}")
        print(f"Valores de a analisados: {lista_a}")

        # Cria os objetos dos métodos numéricos
        bissecao = Bissecao(
            self.f,
            precisao
        )

        newton = NewtonRaphson(
            self.f,
            self.f_prime,
            precisao
        )

        # =====================================================================
        # ANALISA CADA MOVIMENTO
        # =====================================================================

        for numero, valor_a in enumerate(
            lista_a,
            start=1
        ):

            print("\n")
            print("=" * 80)
            print(f"MOVIMENTO {numero}")
            print(f"Valor de a = {valor_a}")
            print("=" * 80)

            inicio, fim = intervalo

            # Valores da função nas extremidades
            f_inicio = self.f(
                inicio,
                valor_a
            )

            f_fim = self.f(
                fim,
                valor_a
            )

            # -----------------------------------------------------------------
            # ISOLAMENTO
            # -----------------------------------------------------------------

            print("\n[ISOLAMENTO]")

            print(
                f"f({inicio}) = {f_inicio:.8f}"
            )

            print(
                f"f({fim}) = {f_fim:.8f}"
            )

            # Verifica se existe mudança de sinal
            if not self.verificar_isolamento(
                valor_a,
                intervalo
            ):

                print(
                    "\nNão existe mudança de sinal no intervalo."
                )

                print(
                    "Não foi encontrada raiz isolada nesse intervalo."
                )

                continue

            print(
                "\nExiste mudança de sinal: "
                "raiz isolada no intervalo."
            )

            # =================================================================
            # MÉTODO DA BISSEÇÃO
            # =================================================================

            print("\n")
            print("-" * 80)
            print("MÉTODO DA BISSEÇÃO")
            print("-" * 80)

            try:

                resultado_bissecao = bissecao.executar(
                    valor_a,
                    intervalo
                )

                self.imprimir_tabela(
                    resultado_bissecao["historico"]
                )

                print(
                    f"\nValor de d calculado: "
                    f"{resultado_bissecao['raiz']:.8f}"
                )

            except ValueError as erro:

                print(
                    f"Erro na Bisseção: {erro}"
                )

            # =================================================================
            # MÉTODO DE NEWTON-RAPHSON
            # =================================================================

            print("\n")
            print("-" * 80)
            print("MÉTODO DE NEWTON-RAPHSON")
            print("-" * 80)

            try:

                resultado_newton = newton.executar(
                    valor_a,
                    intervalo
                )

                self.imprimir_tabela(
                    resultado_newton["historico"]
                )

                print(
                    f"\nValor de d calculado: "
                    f"{resultado_newton['raiz']:.8f}"
                )

            except ValueError as erro:

                print(
                    f"Erro no Newton-Raphson: {erro}"
                )


# =============================================================================
# FUNÇÃO DO TEMA 2
# =============================================================================
#
# f(d) = a * e^d - 4 * d^2
#
# Esta função pode ser facilmente alterada.
# =============================================================================

def f(
    d: float,
    a: float
) -> float:

    return a * math.exp(d) - 4 * (d ** 2)


# =============================================================================
# DERIVADA DA FUNÇÃO
# =============================================================================
#
# f'(d) = a * e^d - 8 * d
#
# Esta função também pode ser facilmente alterada.
# =============================================================================

def f_prime(
    d: float,
    a: float
) -> float:

    return a * math.exp(d) - 8 * d


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    # Entrada de dados.
    # Número de movimentos.
    n = int(input("Digite o número de movimentos: "))
    lista_a = []

    for i in range(n):
        valor_a = float(
            input(f"Digite o valor de a do movimento {i + 1}: ")
        )
        lista_a.append(valor_a)

    # Intervalo de isolamento e precisão são únicos para toda a análise,
    # pois AnalisadorMovimento.executar() recebe um só intervalo/precisão
    # para todos os movimentos da lista.
    inicio = float(
        input("Digite o início do intervalo de isolamento: ")
    )
    fim = float(
        input("Digite o fim do intervalo de isolamento: ")
    )

    isolamento = (inicio, fim)

    eps = float(
        input("Digite a precisão (epsilon): ")
    )

    # Cria o analisador.
    analisador = AnalisadorMovimento(
        f,
        f_prime
    )

    # Executa o programa
    analisador.executar(
        lista_a=lista_a,
        intervalo=isolamento,
        precisao=eps
    )