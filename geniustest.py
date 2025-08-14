"""
GeniusTest - Multi-Agent System for Automated Unit Test Generation

A system that analyzes Python code and generates comprehensive unit tests
using multiple specialized agents working together.
"""
import os
import argparse
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from .env file
load_dotenv()


def get_llm():
    """Initialize the LLM with configuration from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    return GoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        google_api_key=api_key,
    )

class MultiAgentTestGenerator:
    """Multi-agent system for generating comprehensive unit tests."""
    
    def __init__(self):
        """Initialize all agents with their specific prompts."""
        self.llm = get_llm()
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup all specialized agents."""
        # Agent 1: Code Analyzer
        code_analysis_prompt = PromptTemplate.from_template("""
        Você é um assistente especializado em análise de código Python para geração de testes.
        
        Analise o código abaixo e extraia:
        
        1. **Funções e métodos testáveis:**
           - Nome da função/método
           - Parâmetros e tipos esperados
           - Valor de retorno esperado
           - Comportamentos esperados (casos normais e edge cases)
        
        2. **Classes e suas funcionalidades:**
           - Nome da classe
           - Métodos públicos
           - Atributos importantes
           - Estados possíveis
        
        3. **Dependências externas:**
           - Imports necessários
           - Bibliotecas externas
           - Módulos internos
        
        4. **Casos de teste a serem cobertos:**
           - Casos de sucesso (happy path)
           - Casos de erro/exceção
           - Casos extremos (edge cases)
           - Validação de entrada
        
        Código a analisar:
        {code}
        
        Forneça uma análise detalhada focada em identificar exatamente o que precisa ser testado.
        """)
        self.code_analyzer = LLMChain(llm=self.llm, prompt=code_analysis_prompt)
        
        # Agent 2: Test Pattern Specialist
        test_review_prompt = PromptTemplate.from_template("""
        Você é um especialista em qualidade de testes unitários Python. Avalie criticamente os testes fornecidos.
        
        CRITÉRIOS DE AVALIAÇÃO:
        
        1. **Funcionalidade Real:**
           - Os testes realmente executam o código?
           - Os valores de entrada e saída são realistas?
           - Os testes cobrem o comportamento real da função?
        
        2. **Cobertura de Casos:**
           - Casos de sucesso (happy path) estão cobertos?
           - Casos de erro e exceções estão testados?
           - Edge cases importantes estão incluídos?
           - Validação de entrada está presente?
        
        3. **Qualidade dos Assertions:**
           - As assertions verificam os resultados corretos?
           - Os valores esperados são precisos?
           - Exceções são testadas adequadamente?
        
        4. **Estrutura e Organização:**
           - Nomes de testes são descritivos e claros?
           - Seguem o padrão AAA (Arrange, Act, Assert)?
           - Código está bem organizado?
           - Setup/teardown adequados quando necessário?
        
        5. **Executabilidade:**
           - Os testes podem ser executados sem modificações?
           - Imports estão corretos?
           - Não há dependências faltando?
        
        FORMATO DE RESPOSTA:
        - ✅ PONTOS POSITIVOS: [liste o que está bem]
        - ⚠️  PROBLEMAS ENCONTRADOS: [liste problemas específicos]
        - 🔧 SUGESTÕES DE MELHORIA: [como corrigir os problemas]
        - 📊 NOTA GERAL: [1-10] com justificativa
        
        Testes para avaliar:
        {test_code}
        """)
        self.test_specialist = LLMChain(llm=self.llm, prompt=test_review_prompt)
        
        # Agent 3: Test Generator
        test_gen_prompt = PromptTemplate.from_template("""
        Você é um especialista em geração de testes unitários Python. Gere testes FUNCIONAIS e EXECUTÁVEIS usando unittest.
        
        REGRAS IMPORTANTES:
        1. Os testes devem ser REAIS e EXECUTÁVEIS, não exemplos fictícios
        2. Analise o código fornecido e entenda sua lógica exata
        3. Teste todos os caminhos de execução possíveis
        4. Use assertions corretas com valores esperados reais
        5. Inclua imports necessários
        6. Cubra casos de sucesso, erro e edge cases
        
        ESTRUTURA OBRIGATÓRIA:
        ```python
        import unittest
        # Imports adicionais conforme necessário
        
        class TestNomeDaClasse(unittest.TestCase):
            
            def setUp(self):
                # Setup se necessário
                pass
            
            def test_caso_sucesso(self):
                # Teste do caminho principal
                resultado = funcao_testada(parametros_reais)
                self.assertEqual(resultado, valor_esperado_real)
            
            def test_caso_erro(self):
                # Teste de exceções
                with self.assertRaises(TipoExcecao):
                    funcao_testada(parametro_invalido)
            
            def test_edge_case(self):
                # Teste de casos extremos
                resultado = funcao_testada(caso_extremo)
                self.assertEqual(resultado, valor_esperado_extremo)
        
        if __name__ == '__main__':
            unittest.main()
        ```
        
        EXEMPLO DE TESTE REAL para referência:
        Para o código: 
        def calculate_factorial(n):
            if not isinstance(n, int) or n < 0:
                raise ValueError("Input must be a non-negative integer")
            if n == 0:
                return 1
            result = 1
            for i in range(1, n + 1):
                result *= i
            return result
        
        Teste correspondente:
        ```python
        import unittest
        
        class TestCalculateFactorial(unittest.TestCase):
            
            def test_factorial_zero(self):
                result = calculate_factorial(0)
                self.assertEqual(result, 1)
            
            def test_factorial_positive_number(self):
                result = calculate_factorial(5)
                self.assertEqual(result, 120)
                
            def test_factorial_one(self):
                result = calculate_factorial(1)
                self.assertEqual(result, 1)
            
            def test_factorial_negative_number(self):
                with self.assertRaises(ValueError):
                    calculate_factorial(-1)
            
            def test_factorial_non_integer(self):
                with self.assertRaises(ValueError):
                    calculate_factorial(3.5)
        
        if __name__ == '__main__':
            unittest.main()
        ```
        
        Agora gere testes REAIS e FUNCIONAIS para o código a seguir:
        
        {code}
        
        LEMBRE-SE: Os testes devem ser executáveis e testar o comportamento REAL do código!
        """)
        self.test_generator = LLMChain(llm=self.llm, prompt=test_gen_prompt)
        
        # Agent 4: Quality Evaluator
        quality_eval_prompt = PromptTemplate.from_template("""
        Você é um auditor de qualidade de testes. Forneça uma avaliação final concisa e prática.
        
        ANÁLISE OBRIGATÓRIA:
        
        1. **EXECUTABILIDADE** (Crítico):
           - Testes podem rodar sem erros?
           - Imports e dependências corretas?
           - Sintaxe Python válida?
        
        2. **COBERTURA FUNCIONAL**:
           - Testa comportamento real do código?
           - Cobre casos principais, erros e edge cases?
           - Assertions verificam resultados corretos?
        
        3. **QUALIDADE TÉCNICA**:
           - Nomes descritivos e claros?
           - Estrutura organizada (AAA pattern)?
           - Sem código redundante?
        
        FORMATO DE RESPOSTA (MÁXIMO 8 LINHAS):
        
        🎯 **FUNCIONALIDADE**: [Os testes realmente testam o código? São executáveis?]
        📊 **COBERTURA**: [Casos cobertos - principais/erro/edge cases]
        ⚡ **QUALIDADE**: [Estrutura, nomes, organização]
        🚨 **PROBLEMAS CRÍTICOS**: [Problemas que impedem execução]
        💡 **RECOMENDAÇÃO**: [Aprovado/Precisa ajustes/Refazer]
        
        Testes a avaliar:
        {test_code}
        """)
        self.quality_evaluator = LLMChain(llm=self.llm, prompt=quality_eval_prompt)

    def read_python_files(self, directory_path: str) -> List[Dict[str, str]]:
        """
        Read all Python files from a directory.
        
        Args:
            directory_path: Path to the directory containing Python files
            
        Returns:
            List of dictionaries with 'filename' and 'content' keys
        """
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory {directory_path} does not exist")
        
        python_files = []
        for file_path in directory.rglob("*.py"):
            # Skip __init__.py files and files in .venv or __pycache__ directories
            if (file_path.is_file() and 
                file_path.name != "__init__.py" and
                ".venv" not in file_path.parts and
                "__pycache__" not in file_path.parts):
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        python_files.append({
                            'filename': str(file_path.relative_to(directory)),
                            'full_path': str(file_path),
                            'content': content
                        })
                except Exception as e:
                    print(f"⚠️ Erro ao ler arquivo {file_path}: {e}")
        
        return python_files

    def generate_tests_for_file(self, file_info: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate tests for a specific file.
        
        Args:
            file_info: Dictionary containing file information
            
        Returns:
            Dictionary containing analysis results and generated tests
        """
        print(f"📁 Processando arquivo: {file_info['filename']}")
        return self.generate_tests(file_info['content'])

    def process_directory(self, directory_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Process all Python files in a directory and generate tests.
        
        Args:
            directory_path: Path to the directory containing Python files
            
        Returns:
            Dictionary mapping filenames to their test generation results
        """
        python_files = self.read_python_files(directory_path)
        results = {}
        
        print(f"🔍 Encontrados {len(python_files)} arquivos Python em {directory_path}")
        
        for file_info in python_files:
            try:
                results[file_info['filename']] = self.generate_tests_for_file(file_info)
            except Exception as e:
                print(f"❌ Erro ao processar {file_info['filename']}: {e}")
                results[file_info['filename']] = {"error": str(e)}
        
        return results

    def clean_test_content(self, test_content: str) -> str:
        """
        Remove markdown code annotations from test content.
        
        Args:
            test_content: Raw test content that may contain markdown
            
        Returns:
            Cleaned Python code without markdown annotations
        """
        import re
        
        # Remove markdown code blocks (```python ... ``` or ``` ... ```)
        # This pattern matches code blocks with optional language specification
        pattern = r'```(?:python)?\s*\n?(.*?)\n?```'
        matches = re.findall(pattern, test_content, re.DOTALL)
        
        if matches:
            # If we found code blocks, extract the content from them
            return '\n'.join(matches).strip()
        else:
            # If no code blocks found, return original content
            return test_content.strip()

    def write_test_file(self, test_content: str, original_filename: str, output_dir: str) -> str:
        """
        Write generated test content to a test file.
        
        Args:
            test_content: The generated test code
            original_filename: Name of the original file
            output_dir: Output directory for test files
            
        Returns:
            Path to the created test file
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create test filename: calculator.py -> test_calculator.py
        base_name = Path(original_filename).stem
        test_filename = f"test_{base_name}.py"
        test_file_path = output_path / test_filename
        
        try:
            # Clean the test content to remove markdown annotations
            clean_content = self.clean_test_content(test_content)
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            print(f"✅ Test file created: {test_file_path}")
            return str(test_file_path)
        except Exception as e:
            print(f"❌ Error writing test file {test_file_path}: {e}")
            raise

    def process_directory_with_output(self, directory_path: str, output_dir: str = "tests") -> Dict[str, Dict[str, Any]]:
        """
        Process all Python files in a directory and write test files.
        
        Args:
            directory_path: Path to the directory containing Python files
            output_dir: Directory where test files will be written
            
        Returns:
            Dictionary mapping filenames to their test generation results
        """
        results = self.process_directory(directory_path)
        
        for filename, result in results.items():
            if "error" not in result and "generated_tests" in result:
                try:
                    test_content = result["generated_tests"]["text"]
                    test_file_path = self.write_test_file(test_content, filename, output_dir)
                    result["test_file_path"] = test_file_path
                except Exception as e:
                    print(f"❌ Failed to write test for {filename}: {e}")
                    result["write_error"] = str(e)
        
        return results

    def generate_tests(self, source_code: str) -> dict:
        """
        Orchestrate the multi-agent test generation process.
        
        Args:
            source_code: Python source code as string
            
        Returns:
            Dictionary containing analysis results and generated tests
        """
        print("🔎 Analisando o código...")
        analysis = self.code_analyzer.invoke({"code": source_code})

        print("🛠️ Gerando testes...")
        generated_tests = self.test_generator.invoke({"code": source_code})

        print("🧪 Avaliando padrões de teste...")
        pattern_evaluation = self.test_specialist.invoke({
            "test_code": generated_tests.get('text', '')
        })

        print("📈 Avaliando qualidade dos testes...")
        quality_evaluation = self.quality_evaluator.invoke({
            "test_code": generated_tests.get('text', '')
        })

        return {
            "code_analysis": analysis,
            "generated_tests": generated_tests,
            "pattern_evaluation": pattern_evaluation,
            "quality_evaluation": quality_evaluation,
        }


def generate_tests_for_code(source_code: str) -> dict:
    """
    Convenience function to generate tests for given source code.
    
    Args:
        source_code: Python source code as string
        
    Returns:
        Dictionary containing analysis results and generated tests
    """
    generator = MultiAgentTestGenerator()
    return generator.generate_tests(source_code)


def process_directory(directory_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to process all Python files in a directory.
    
    Args:
        directory_path: Path to the directory containing Python files
        
    Returns:
        Dictionary mapping filenames to their test generation results
    """
    generator = MultiAgentTestGenerator()
    return generator.process_directory(directory_path)


def process_directory_with_output(directory_path: str, output_dir: str = "tests") -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to process directory and write test files.
    
    Args:
        directory_path: Path to the directory containing Python files
        output_dir: Directory where test files will be written
        
    Returns:
        Dictionary mapping filenames to their test generation results
    """
    generator = MultiAgentTestGenerator()
    return generator.process_directory_with_output(directory_path, output_dir)

def main():
    """Main function with command line argument support."""
    parser = argparse.ArgumentParser(description="Generate unit tests for Python code")
    parser.add_argument(
        "--directory", "-d",
        type=str,
        help="Directory path to scan for Python files"
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Single Python file to process"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="tests",
        help="Output directory for generated test files (default: tests)"
    )
    parser.add_argument(
        "--write-files", "-w",
        action="store_true",
        help="Write generated tests to files"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run with example code"
    )
    
    args = parser.parse_args()
    
    if args.directory:
        print(f"--- Processando diretório: {args.directory} ---")
        
        if args.write_files:
            print(f"📝 Escrevendo arquivos de teste em: {args.output}")
            results = process_directory_with_output(args.directory, args.output)
        else:
            results = process_directory(args.directory)
        
        for filename, result in results.items():
            print(f"\n{'='*60}")
            print(f"📁 ARQUIVO: {filename}")
            print('='*60)
            
            if "error" in result:
                print(f"❌ Erro: {result['error']}")
                continue
            
            if args.write_files and "test_file_path" in result:
                print(f"✅ Arquivo de teste criado: {result['test_file_path']}")
            
            if not args.write_files:  # Only show full output if not writing files
                print("\n## Análise do Código:")
                print(result["code_analysis"]["text"])
                
                print("\n## Testes Gerados:")
                print(result["generated_tests"]["text"])
                
                print("\n## Avaliação de Padrões:")
                print(result["pattern_evaluation"]["text"])
                
                print("\n## Avaliação de Qualidade:")
                print(result["quality_evaluation"]["text"])
    
    elif args.file:
        print(f"--- Processando arquivo: {args.file} ---")
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
            
            results = generate_tests_for_code(code)
            
            if args.write_files:
                generator = MultiAgentTestGenerator()
                filename = Path(args.file).name
                test_file_path = generator.write_test_file(
                    results["generated_tests"]["text"], 
                    filename, 
                    args.output
                )
                print(f"✅ Arquivo de teste criado: {test_file_path}")
            else:
                print("\n## Análise do Código:")
                print(results["code_analysis"]["text"])
                
                print("\n## Testes Gerados:")
                print(results["generated_tests"]["text"])
                
                print("\n## Avaliação de Padrões:")
                print(results["pattern_evaluation"]["text"])
                
                print("\n## Avaliação de Qualidade:")
                print(results["quality_evaluation"]["text"])
            
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {args.file}")
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
    
    else:
        print("--- Running Multi-Agent Test Generator (Example) ---")
        example_code = """
def calculate_factorial(n):
    \"\"\"Calculates the factorial of a non-negative integer.\"\"\"
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
"""
        
        results = generate_tests_for_code(example_code)
        
        print("\n## Code Analysis:")
        print(results["code_analysis"]["text"])
        
        print("\n## Generated Tests:")
        print(results["generated_tests"]["text"])
        
        print("\n## Test Pattern Evaluation:")
        print(results["pattern_evaluation"]["text"])
        
        print("\n## Quality Evaluation:")
        print(results["quality_evaluation"]["text"])


if __name__ == "__main__":
    main()
