# Status Package

Esse repositório tem o objetivo de padronizar os status de execução dos coletores escritos em Go e Python.

## Status disponíveis

Abaixo segue uma tabela com os status disponíveis:

|Nº| Status code | Significado |
|--|-------------|-------------|
|0|OK|O processo ocorreu sem erros.|
|1|InvalidParameters|Deve ser utilizado em caso de parâmetros inválidos, como ano e mês.|
|2|SystemError|Deve ser usado em casos como falha ao criar o diretório dos arquivos ou na leitura de arquivos.|
|3|ConnectionError|Deve ser usado em problemas de conexão, como timeout ou serviço fora do ar.|
|4|DataUnavailable|A informação solicitada não foi encontrada, provavelmente o órgão não disponibilizou ainda.|
|5|InvalidFile|Deve ser usado para cenários onde o arquivo não é o esperado ou em caso de falhas na extração de dados.|
|6|Unknown|Deve ser usando quando um erro inesperado ocorrer.|
|7|InvalidInput|A entrada do estágio é inválida.|
|8|OutputError|Quando o estágio não for capaz de imprimir a saída correta.|
|9|DeadlineExceeded|Quando uma determinada ação não foi concluída dentro do prazo esperado.|
______________

## Exemplo de uso em Go
```
package main

import (
	"fmt"

	"github.com/dadosjusbr/status"
)

func myFunc() *status.Error {
	return status.NewError(status.DataUnavailable, fmt.Errorf("Este é um exemplo!"))
}

func main() {
	err := myFunc()
	status.ExitFromError(err)
}
```

## Exemplo de uso em Python

```
import status

def myfunc():
    return status.Error(status.DataUnavailable, "Este é um exemplo!")

err = myfunc()
status.exit_from_error(err)
```
## Atulizando a lib no pypi

Antes, faz-se necessário atualizar o número da versão em ./setup.py #L9 (visar versionamento semântico).
É importante atualizar a versão no PyPi para que as últimas modificações estejam presentes no pacote a ser baixado com pip.

```sh
    $ python3 setup.py sdist
    $ python3 -m twine upload --skip-existing dist/*
```