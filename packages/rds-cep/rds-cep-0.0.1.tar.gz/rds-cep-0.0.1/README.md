# rds-cep-python

É uma biblioteca pública em Python que acessa a RDS-LAIS e consulta dados relacionados ao CEP.

## Usando no seu projeto

```bash
pip install rds-cep
```

## Como desenvolver

Crie uma nova branch, clone o código, crie uma venv para desenvolvimento, instale os pacotes de desenvolvimento, teste o código, commit as mudanças na branch, envie para o repositório, solicite um Pull Request.

```bash
mkvirtualenv rds-core
pip install -r requirements-dev.txt
```

Caso você deseje alterar o código do rds-core e testar como reflete aqui

```bash
# Prepare
pip install -e ../rds-core

```

Teste as alterações

```bash
# Teste o software conforme os padrões de arquitetura
pre-commit run --all-files -v
```
