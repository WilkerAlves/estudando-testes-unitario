from src.leilao.excecoes import LanceInvalido


class Usuario:

    def __init__(self, nome, carteira):
        self.__nome = nome
        self.__carteira = carteira

    @property
    def nome(self):
        return self.__nome

    @property
    def carteira(self):
        return self.__carteira

    def propoe_lance(self, leilao, valor):
        if not self._valor_eh_valido(valor):
            raise ValueError("Não pode propor um lance com o valor maior que a carteira")
        lance = Lance(self, valor)
        leilao.propoe(lance)
        self.__carteira -= valor

    def _valor_eh_valido(self, valor):
        return valor <= self.__carteira


class Lance:

    def __init__(self, usuario, valor):
        self.usuario = usuario
        self.valor = valor


class Leilao:

    def __init__(self, descricao):
        self.descricao = descricao
        self.__lances = []
        self.maior_lance = 0.0
        self.menor_lance = 0.0

    def propoe(self, lance: Lance):
        if self._lance_eh_valido(lance):
            if not self._tem_lances():
                self.menor_lance = lance.valor

            self.maior_lance = lance.valor
            self.__lances.append(lance)
        else:
            raise LanceInvalido('Erro ao propor lance')

    @property
    # devolvendo um copia da lista
    def lances(self):
        return self.__lances[:]

    def _tem_lances(self):
        return self.__lances

    def _usuarios_diferentes(self, lance):
        if self.lances[-1].usuario != lance.usuario:
            return True
        else:
            raise LanceInvalido('O mesmo usuario não pode dar dois lances seguidos')

    def _valor_maior_que_lance_anterior(self, lance):
        if lance.valor > self.lances[-1].valor:
            return True
        else:
            raise LanceInvalido('O valor do lance deve ser maior que o lance anterior')

    def _lance_eh_valido(self, lance):
        return not self._tem_lances() or (self._usuarios_diferentes(lance)
                                          and self._valor_maior_que_lance_anterior(lance))
