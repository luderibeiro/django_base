#!/bin/bash

# Script para testar endpoints da API Django Base
# Requer servidor rodando em http://127.0.0.1:8000

set -e

SERVER_URL="http://127.0.0.1:8000"

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🌐 TESTE DE ENDPOINTS - DJANGO BASE${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Verificar se servidor está rodando
echo -e "${YELLOW}Verificando se servidor está rodando...${NC}"
if ! curl -s --connect-timeout 2 "$SERVER_URL" > /dev/null 2>&1; then
    echo -e "${RED}❌ Servidor não está rodando em $SERVER_URL${NC}"
    echo -e "${YELLOW}Execute 'make run' em outro terminal primeiro${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Servidor está rodando${NC}"
echo ""

# Função para testar endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local method=${3:-GET}
    local expected=${4:-200}
    
    echo -e "${BLUE}Testando: ${name}${NC}"
    echo -e "  URL: ${url}"
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" 2>/dev/null || echo "000")
    fi
    
    if [ "$response" = "$expected" ] || [ "$response" = "302" ] || [ "$response" = "401" ]; then
        echo -e "  ${GREEN}✅ HTTP ${response}${NC}"
        return 0
    else
        echo -e "  ${RED}❌ HTTP ${response} (esperado: ${expected})${NC}"
        return 1
    fi
}

# Testar endpoints públicos
echo -e "${YELLOW}📋 Endpoints Públicos${NC}"
echo ""

test_endpoint "Admin Django" "$SERVER_URL/admin/" "GET" "200"
test_endpoint "API Schema" "$SERVER_URL/api/schema/" "GET" "200"
test_endpoint "Swagger UI" "$SERVER_URL/api/docs/" "GET" "200"
test_endpoint "ReDoc" "$SERVER_URL/api/redoc/" "GET" "200"
test_endpoint "OAuth2 Authorize" "$SERVER_URL/o/authorize/" "GET" "200"

echo ""

# Testar endpoints da API (esperamos 401 sem autenticação)
echo -e "${YELLOW}🔐 Endpoints da API (sem autenticação)${NC}"
echo ""

test_endpoint "API Users List" "$SERVER_URL/api/v1/users/list/" "GET" "401"
test_endpoint "API Create User" "$SERVER_URL/api/v1/users/" "POST" "401"
test_endpoint "API Login" "$SERVER_URL/api/v1/login/" "POST" "400"

echo ""
echo -e "${YELLOW}💡 Para testar endpoints autenticados:${NC}"
echo -e "  1. Configure OAuth2: python scripts/setup_oauth_client.py"
echo -e "  2. Obtenha token: curl -X POST $SERVER_URL/o/token/ ..."
echo -e "  3. Use token: curl -H 'Authorization: Bearer TOKEN' ..."
echo ""

echo -e "${GREEN}✅ Testes de endpoints concluídos${NC}"

