# -*- coding: utf-8 -*-
from typing import Union
import re
from rds_core import searchengine, config

# from rds_core.searchengine import search_engine
__all__ = ("validate", "get")

CEP_REGEX = re.compile(r"^(\d{2})\.?(\d{3})-?(\d{3})?$")


def validate(cep: str, silentily: bool = True) -> Union[str, bool]:
    """Valida o CEP informado

    Args:
        cep (str): número do CEP, aceita CEP com ou sem máscara, ou seja, aceita exemplos como:
          "59015", "59015000", "59015-000", "59.015", "59.015000", "59.015-000", "59015-" ou "59.015-"
        silentily (bool, optional): Caso não seja um CEP válido e silentily seja True então retorna False,
          caso contrário lança a exception ValueError. Defaults to True.

    Raises:
        ValueError: Significa que a validação do CEP falhou.

    Returns:
        Union[str, bool]:
          Se for válido retorna uma string com o CEP validado,
          caso contrário retorna False se o silentily=True
          também pode lançar um exception ValueError se for um CEP inválido e o silentily=False
    """

    matches = CEP_REGEX.match(cep)
    if matches is None:
        if not silentily:
            raise ValueError("Este não é um CEP válido.")
        return False
    result = "".join([x for x in matches.groups() if x is not None])
    if len(result) == 5:
        result += "000"
    return result


def get(cep: str, silentily: bool = True) -> Union[dict, None, bool]:
    """Retorna o CEP informado

    Args:
        cep (str): número do CEP, aceita CEP com ou sem máscara, ou seja, aceita exemplos como:
          "59015", "59015000", "59015-000", "59.015", "59.015000", "59.015-000", "59015-" ou "59.015-"
        silentily (bool, optional): Caso não seja um CEP válido e `silentily` seja `True` então retorna `False`,
          caso contrário lança a exception `ValueError`. Defaults to `True`.

    Raises:
        ValueError: Significa que a validação do CEP falhou.

    Returns:
        **Union[dict, None, False]**:
          Se for válido e **existir** retorna um `Dict` com o CEP.
          Se for válido e **não existir**, retorna `None`.
          Se não for válido e o `silentily=True`, retorna `False`.
          Se não for válido `silentily=False`, lança uma exception `ValueError`.
    """
    valid_cep = validate(cep, silentily)
    if not valid_cep:
        return False

    query = {
        "query": {"query_string": {"query": f"cep: {valid_cep}"}},
        "size": 10,
        "from": 0,
    }
    result = searchengine.search(config.settings.get("RDS_CEP_INDEX_NAME", "cep_logradouro"), body=query)
    if len(result) > 0 and len(result[0]) > 0 and "_source" in result[0][0]:
        return result[0][0]["_source"]

    if not silentily:
        raise ValueError("CEP não existe")
    return False
