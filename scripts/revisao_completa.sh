#!/bin/bash

# Script de Revisão Completa do Projeto Django Base
# Testa todos os componentes do projeto

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
PASSED=0
FAILED=0

# Função para testar comandos
test_command() {
    local name=$1
    local command=$2
    
    echo -e "${BLUE}🧪 Testando: ${name}${NC}"
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ ${name}: PASSOU${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ ${name}: FALHOU${NC}"
        ((FAILED++))
        return 1
    fi
}

# Função para testar endpoints
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local data=${4:-""}
    
    echo -e "${BLUE}🌐 Testando endpoint: ${name}${NC}"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" -H "Content-Type: application/json" -d "$data" 2>/dev/null || echo "000")
    fi
    
    if [ "$response" = "200" ] || [ "$response" = "201" ] || [ "$response" = "302" ] || [ "$response" = "401" ] || [ "$response" = "404" ]; then
        echo -e "${GREEN}✅ ${name}: Respondeu (HTTP ${response})${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ ${name}: Falhou (HTTP ${response})${NC}"
        ((FAILED++))
        return 1
    fi
}

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔍 REVISÃO COMPLETA DO PROJETO DJANGO BASE${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# 1. VERIFICAÇÃO DE ESTRUTURA
# ============================================================================
echo -e "${YELLOW}📁 1. VERIFICAÇÃO DE ESTRUTURA${NC}"
echo ""

test_command "Arquivo Makefile existe" "test -f Makefile"
test_command "Arquivo requirements.txt existe" "test -f project/requirements.txt"
test_command "Arquivo settings.py existe" "test -f project/project/settings.py"
test_command "Arquivo manage.py existe" "test -f project/manage.py"
test_command "Diretório core existe" "test -d project/core"
test_command "Arquivo .gitignore existe" "test -f .gitignore"
test_command "Arquivo .pre-commit-config.yaml existe" "test -f .pre-commit-config.yaml"

echo ""

# ============================================================================
# 2. TESTES DE COMANDOS MAKEFILE
# ============================================================================
echo -e "${YELLOW}🔧 2. TESTES DE COMANDOS MAKEFILE${NC}"
echo ""

test_command "make help" "make help | grep -q 'Comandos disponíveis'"
test_command "make install (verifica sintaxe)" "make -n install"

echo ""

# ============================================================================
# 3. VERIFICAÇÃO DE QUALIDADE DE CÓDIGO
# ============================================================================
echo -e "${YELLOW}🎨 3. VERIFICAÇÃO DE QUALIDADE DE CÓDIGO${NC}"
echo ""

# Verificar se Python está disponível
if command -v python3 &> /dev/null; then
    test_command "Python 3 disponível" "python3 --version"
    
    # Verificar sintaxe Python dos arquivos principais
    test_command "Sintaxe settings.py" "python3 -m py_compile project/project/settings.py"
    test_command "Sintaxe manage.py" "python3 -m py_compile project/manage.py"
    
    # Verificar se scripts Python têm sintaxe válida
    if [ -f "scripts/generate_env.py" ]; then
        test_command "Sintaxe generate_env.py" "python3 -m py_compile scripts/generate_env.py"
    fi
    if [ -f "scripts/setup_oauth_client.py" ]; then
        test_command "Sintaxe setup_oauth_client.py" "python3 -m py_compile scripts/setup_oauth_client.py"
    fi
else
    echo -e "${YELLOW}⚠️  Python 3 não encontrado, pulando testes de sintaxe${NC}"
fi

echo ""

# ============================================================================
# 4. VERIFICAÇÃO DE CONFIGURAÇÕES
# ============================================================================
echo -e "${YELLOW}⚙️  4. VERIFICAÇÃO DE CONFIGURAÇÕES${NC}"
echo ""

test_command "Arquivo .coveragerc existe" "test -f .coveragerc"
test_command "Arquivo mypy.ini existe" "test -f mypy.ini"
test_command "Arquivo pydocstyle.ini existe" "test -f pydocstyle.ini"
test_command "Arquivo pytest.ini existe" "test -f pytest.ini"
test_command "Arquivo mkdocs.yml existe" "test -f mkdocs.yml"

echo ""

# ============================================================================
# 5. VERIFICAÇÃO DE DOCKER
# ============================================================================
echo -e "${YELLOW}🐳 5. VERIFICAÇÃO DE DOCKER${NC}"
echo ""

test_command "Dockerfile existe" "test -f Dockerfile"
test_command "Dockerfile.dev existe" "test -f Dockerfile.dev"
test_command "docker-compose.dev.yml existe" "test -f docker-compose.dev.yml"
test_command "docker-compose.prod.yml existe" "test -f docker-compose.prod.yml"

# Verificar sintaxe YAML
if command -v python3 &> /dev/null; then
    test_command "Sintaxe docker-compose.dev.yml" "python3 -c 'import yaml; yaml.safe_load(open(\"docker-compose.dev.yml\"))'"
    test_command "Sintaxe docker-compose.prod.yml" "python3 -c 'import yaml; yaml.safe_load(open(\"docker-compose.prod.yml\"))'"
fi

echo ""

# ============================================================================
# 6. VERIFICAÇÃO DE SCRIPTS
# ============================================================================
echo -e "${YELLOW}📜 6. VERIFICAÇÃO DE SCRIPTS${NC}"
echo ""

test_command "Script run.sh existe" "test -f scripts/run.sh"
test_command "Script run.sh é executável" "test -x scripts/run.sh"

if [ -f "scripts/generate_env.py" ]; then
    test_command "Script generate_env.py existe" "test -f scripts/generate_env.py"
    test_command "Script generate_env.py é executável" "test -x scripts/generate_env.py"
fi

echo ""

# ============================================================================
# 7. VERIFICAÇÃO DE DOCUMENTAÇÃO
# ============================================================================
echo -e "${YELLOW}📚 7. VERIFICAÇÃO DE DOCUMENTAÇÃO${NC}"
echo ""

test_command "README.md existe" "test -f README.md"
test_command "CONTRIBUTING.md existe" "test -f CONTRIBUTING.md"
test_command "LICENSE existe" "test -f LICENSE"

echo ""

# ============================================================================
# 8. TESTES DE ENDPOINTS (se servidor estiver rodando)
# ============================================================================
echo -e "${YELLOW}🌐 8. TESTES DE ENDPOINTS${NC}"
echo ""

SERVER_URL="http://127.0.0.1:8000"

# Verificar se servidor está rodando
if curl -s --connect-timeout 2 "$SERVER_URL" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Servidor Django está rodando${NC}"
    echo ""
    
    # Testar endpoints públicos
    test_endpoint "Admin Django" "$SERVER_URL/admin/"
    test_endpoint "API Schema" "$SERVER_URL/api/schema/"
    test_endpoint "Swagger UI" "$SERVER_URL/api/docs/"
    test_endpoint "ReDoc" "$SERVER_URL/api/redoc/"
    test_endpoint "OAuth2 Authorize" "$SERVER_URL/o/authorize/"
    
    # Testar endpoints da API (esperamos 401 sem autenticação)
    test_endpoint "API Users List" "$SERVER_URL/api/v1/users/list/"
    test_endpoint "API Login" "$SERVER_URL/api/v1/login/" "POST" '{"email":"test@test.com","password":"test"}'
    
    echo ""
    echo -e "${YELLOW}💡 Para testar endpoints autenticados, configure OAuth2 primeiro${NC}"
else
    echo -e "${YELLOW}⚠️  Servidor Django não está rodando${NC}"
    echo -e "${YELLOW}   Execute 'make run' em outro terminal para testar endpoints${NC}"
    ((FAILED++))
fi

echo ""

# ============================================================================
# RESUMO
# ============================================================================
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  📊 RESUMO DA REVISÃO${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

TOTAL=$((PASSED + FAILED))
if [ $TOTAL -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Nenhum teste foi executado${NC}"
else
    echo -e "${GREEN}✅ Testes passaram: ${PASSED}${NC}"
    if [ $FAILED -gt 0 ]; then
        echo -e "${RED}❌ Testes falharam: ${FAILED}${NC}"
    fi
    echo ""
    
    PERCENTAGE=$((PASSED * 100 / TOTAL))
    echo -e "Taxa de sucesso: ${PERCENTAGE}%"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}🎉 Todos os testes passaram! Projeto está em excelente estado!${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Alguns testes falharam. Revise os erros acima.${NC}"
        exit 1
    fi
fi

