# Projeto Multi-Agente Calculadora

Um projeto Python abrangente com calculadora, interface CLI, geração automatizada de testes usando agentes de IA e ferramentas de análise de qualidade.

## 📋 Índice

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Início Rápido](#início-rápido)
- [Configuração e Instalação](#configuração-e-instalação)
- [Uso da Calculadora](#uso-da-calculadora)
- [GeniusTest - Gerador de Testes com IA](#geniustest---gerador-de-testes-com-ia)
- [Benchmark - Análise de Qualidade](#benchmark---análise-de-qualidade)
- [Fluxo de Desenvolvimento](#fluxo-de-desenvolvimento)
- [Configuração](#configuração)
- [Solução de Problemas](#solução-de-problemas)

## 🏗️ Estrutura do Projeto

```
multi_agents/
├── calculator/                 # Projeto principal da calculadora
│   ├── src/calculator/        # Código fonte
│   │   ├── calculator.py      # Lógica principal da calculadora
│   │   ├── cli.py            # Interface de linha de comando
│   │   └── main.py           # Ponto de entrada da aplicação
│   ├── tests/                # Arquivos de teste
│   │   ├── test_calculator.py
│   │   ├── test_cli.py
│   │   └── test_main.py
│   └── pyproject.toml        # Dependências do projeto
├── geniustest.py             # Gerador de testes com IA
├── benchmark.py              # Analisador de qualidade e cobertura
├── .env                      # Variáveis de ambiente
└── README.md                 # Este arquivo
```

## 🚀 Início Rápido

1. **Clone e configuração:**
```bash
git clone <seu-repositorio>
cd multi_agents
```

2. **Configurar ambiente:**
```bash
uv sync
echo "GOOGLE_API_KEY=sua_chave_api_aqui" > .env
```

3. **Executar calculadora:**
```bash
cd calculator
uv run calc add 5 3
```

4. **Gerar testes:**
```bash
uv run python ../geniustest.py --directory ./calculator/src --write-files
```

5. **Executar benchmark:**
```bash
cd calculator
uv run python ../benchmark.py
```

## 🛠️ Configuração e Instalação

### Pré-requisitos

- Python 3.12+
- Gerenciador de pacotes [uv](https://docs.astral.sh/uv/)
- Chave API do Google Gemini

### Passos de Instalação

1. **Instalar uv** (se ainda não instalado):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Inicializar o projeto:**
```bash
cd multi_agents
uv sync
```

3. **Configurar variáveis de ambiente:**
```bash
# Criar arquivo .env com sua chave API do Google
echo "GOOGLE_API_KEY=sua_chave_api_real_aqui" > .env
```

4. **Instalar calculadora como pacote:**
```bash
cd calculator
uv pip install -e .
```

5. **Verificar instalação:**
```bash
uv run calc --help
```

## 🧮 Uso da Calculadora

A calculadora fornece uma interface CLI para operações matemáticas com rastreamento de histórico.

### Operações Básicas

```bash
cd calculator

# Adição
uv run calc add 5 3
# Resultado: 8.0

# Subtração
uv run calc subtract 10 4
# Resultado: 6.0

# Multiplicação
uv run calc multiply 6 7
# Resultado: 42.0

# Divisão
uv run calc divide 15 3
# Resultado: 5.0

# Potenciação
uv run calc power 2 8
# Resultado: 256.0
```

### Recursos Avançados

**Trabalhando com números negativos:**
```bash
# Use -- para separar números negativos das opções
uv run calc add -- -5 -3
# Resultado: -8.0

uv run calc subtract -- 5 -3
# Resultado: 8.0
```

**Gerenciamento de histórico:**
```bash
# Ver histórico de cálculos
uv run calc history

# Limpar histórico
uv run calc clear
```

### Uso da API Python

```python
from calculator.calculator import Calculator

calc = Calculator()
result = calc.add(5, 3)
print(f"Resultado: {result}")
print(f"Histórico: {calc.get_history()}")
```

## 🤖 GeniusTest - Gerador de Testes com IA

GeniusTest é um sistema multi-agente que gera automaticamente testes unitários abrangentes para código Python usando IA.

### Funcionalidades

- **Análise multi-agente**: Analisador de código, gerador de testes, especialista em padrões, avaliador de qualidade
- **Testes funcionais reais**: Gera testes executáveis, não apenas exemplos
- **Cobertura abrangente**: Testa casos de sucesso, erros e casos extremos
- **Múltiplos formatos de saída**: Exibição no console ou geração de arquivos

### Exemplos de Uso

**Analisar e exibir testes para um único arquivo:**
```bash
uv run python geniustest.py --file ./calculator/src/calculator/calculator.py
```

**Gerar arquivos de teste para diretório inteiro:**
```bash
uv run python geniustest.py --directory ./calculator/src --write-files --output ./calculator/tests_generated
```

**Processar com diretório de saída personalizado:**
```bash
uv run python geniustest.py --directory ./meu_projeto --write-files --output ./meus_testes
```

**Executar com código de exemplo:**
```bash
uv run python geniustest.py
```

### Opções da Linha de Comando

```bash
uv run python geniustest.py --help

Opções:
  -d, --directory TEXT    Caminho do diretório para escanear arquivos Python
  -f, --file TEXT        Arquivo Python único para processar
  -o, --output TEXT      Diretório de saída para arquivos de teste gerados (padrão: tests)
  -w, --write-files      Escrever testes gerados em arquivos
  --example              Executar com código de exemplo
```

### Estrutura dos Testes Gerados

GeniusTest gera testes seguindo esta estrutura:

```python
import unittest
import sys
import os

# Configuração de caminho para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator.calculator import Calculator

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calculator = Calculator()
    
    def test_add_positive_numbers(self):
        result = self.calculator.add(5, 3)
        self.assertEqual(result, 8)
    
    def test_add_negative_numbers(self):
        result = self.calculator.add(-5, -3)
        self.assertEqual(result, -8)
    
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calculator.divide(5, 0)

if __name__ == '__main__':
    unittest.main()
```

## 📊 Benchmark - Análise de Qualidade

O script de benchmark fornece análise abrangente de cobertura de testes e métricas de qualidade.

### Funcionalidades

- **Análise de Cobertura**: Cobertura de linha e branch usando pytest-cov
- **Métricas de Qualidade de Testes**: Densidade de testes, qualidade de assertions, melhores práticas
- **Pontuação de Qualidade**: Pontuação geral (0-100) com notas por letras
- **Múltiplos Formatos de Saída**: Relatórios em texto e dados JSON

### Exemplos de Uso

**Análise básica de benchmark:**
```bash
cd calculator
uv run python ../benchmark.py
```

**Gerar arquivo de relatório:**
```bash
cd calculator
uv run python ../benchmark.py --output relatorio_benchmark.txt
```

**Saída JSON para CI/CD:**
```bash
cd calculator
uv run python ../benchmark.py --json --output resultados.json
```

**Caminhos de projeto personalizados:**
```bash
uv run python benchmark.py --project ./meu_projeto --tests meus_testes --source meu_src
```

### Opções da Linha de Comando

```bash
uv run python benchmark.py --help

Opções:
  -p, --project TEXT     Caminho do diretório do projeto (padrão: .)
  -t, --tests TEXT       Caminho do diretório de testes (padrão: tests)
  -s, --source TEXT      Diretório do código fonte (padrão: src)
  -o, --output TEXT      Arquivo de relatório de saída
  --json                 Gerar resultados em formato JSON
```

### Exemplo de Relatório de Benchmark

```
# Relatório de Benchmark de Qualidade e Cobertura de Testes
Gerado em: 2025-08-13 22:15:23
Projeto: calculator

## Pontuação Geral de Qualidade: 85.42/100 (Nota: B)

### Análise de Cobertura
- Cobertura de Linha: 94.94%
- Cobertura de Branch: 87.50%
- Pontuação de Cobertura: 94.94/100

### Métricas de Qualidade de Testes
- Total de Arquivos de Teste: 3
- Total de Métodos de Teste: 44
- Total de Assertions: 92
- Média de Assertions por Teste: 2.09
- Métodos Setup/Teardown: 3
- Uso de Mock: 8
- Testes Parametrizados: 0

### Detalhamento das Pontuações de Qualidade
- Pontuação de Densidade de Testes: 100/100
- Pontuação de Qualidade de Assertions: 41.82/100
- Pontuação de Melhores Práticas: 59.09/100

### Cobertura Arquivo por Arquivo
- calculator.py: 100.0% linhas
- cli.py: 97.7% linhas
- main.py: 0.0% linhas

✅ Análise de cobertura concluída com sucesso
```

## 🔧 Fluxo de Desenvolvimento

### Executando Testes

```bash
cd calculator

# Executar todos os testes
uv run pytest

# Executar com cobertura
uv run pytest --cov=src/calculator --cov-report=html

# Executar arquivo de teste específico
uv run pytest tests/test_calculator.py

# Executar com saída verbosa
uv run pytest -v
```

### Verificações de Qualidade de Código

```bash
cd calculator

# Executar análise de benchmark
uv run python ../benchmark.py

# Gerar relatório de cobertura
uv run pytest --cov=src/calculator --cov-report=html
open htmlcov/index.html  # Visualizar no navegador
```

### Integração Contínua

Exemplo de workflow do GitHub Actions:

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v1
    
    - name: Instalar dependências
      run: uv sync
      
    - name: Executar testes
      run: |
        cd calculator
        uv run pytest --cov=src/calculator --cov-report=xml
        
    - name: Executar benchmark
      run: |
        cd calculator  
        uv run python ../benchmark.py --json --output benchmark.json
```

## ⚙️ Configuração

### Variáveis de Ambiente

Criar um arquivo `.env` na raiz do projeto:

```env
# Necessário para recursos de IA do GeniusTest
GOOGLE_API_KEY=sua_chave_api_google_aqui

# Opcional: Configurações de modelo personalizado
GEMINI_MODEL=gemini-2.0-flash
TEMPERATURE=0.7
```

### Configuração do Projeto

**pyproject.toml** para calculadora:

```toml
[project]
name = "calculator"
version = "0.1.0"
dependencies = [
    "typer>=0.9.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src/calculator --cov-report=term-missing"
```

### Configuração da IDE

**VS Code settings.json:**

```json
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.linting.enabled": true
}
```

## 🐛 Solução de Problemas

### Problemas Comuns

**1. Erros de "Módulo não encontrado":**
```bash
# Certifique-se de usar uv run
uv run pytest

# Ou ative o ambiente virtual
source .venv/bin/activate
pytest
```

**2. Números negativos tratados como opções:**
```bash
# Use separador --
uv run calc add -- -5 -3

# Ou coloque os números entre aspas
uv run calc add "-5" "-3"
```

**3. Cobertura não coletando dados:**
```bash
# Certifique-se de usar uv run
cd calculator
uv run pytest --cov=src/calculator

# Verifique se os testes estão realmente importando o código
uv run pytest -v
```

**4. Erros de API do GeniusTest:**
```bash
# Verifique se a chave API está definida
echo $GOOGLE_API_KEY

# Verifique se o arquivo .env existe
cat .env
```

**5. Erros de import nos testes gerados:**
- Testes gerados incluem configuração adequada de caminho
- Certifique-se de que a estrutura do código fonte corresponde aos imports
- Execute testes com `uv run pytest`

### Obtendo Ajuda

1. **Verificar logs**: A maioria dos comandos fornece saída verbosa com flag `-v`
2. **Validar ambiente**: Execute `uv run python -c "import calculator; print('OK')"`
3. **Testar conectividade**: Execute GeniusTest com código de exemplo primeiro
4. **Verificar dependências**: Execute `uv sync` para garantir que todos os pacotes estão instalados

### Dicas de Performance

- **Use `--write-files`** com GeniusTest para projetos grandes para evitar spam no console
- **Execute benchmark periodicamente** para acompanhar melhorias de qualidade
- **Use saída JSON** para processamento automatizado em CI/CD
- **Cache do ambiente virtual** em sistemas CI para builds mais rápidos

## 📚 Recursos Adicionais

- [Documentação do uv](https://docs.astral.sh/uv/)
- [Documentação do pytest](https://docs.pytest.org/)
- [Documentação do Typer](https://typer.tiangolo.com/)
- [API do Google Gemini](https://ai.google.dev/docs)

---

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch de feature: `git checkout -b nome-da-feature`
3. Faça mudanças e adicione testes
4. Execute verificações de qualidade: `uv run python benchmark.py`
5. Submeta um pull request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para detalhes.