#!/usr/bin/env bash
set -euo pipefail


MODULE="cart"


echo "Criando/atualizando estrutura do módulo: ${MODULE} (executar dentro de project/)"


mkdir -p ${MODULE}/{api,domain/entities,domain/use_cases,models,repositories,services,tests/unit,tests/integration}


# arquivos __init__.py
for d in "${MODULE}" "${MODULE}/api" "${MODULE}/domain" "${MODULE}/domain/entities" "${MODULE}/domain/use_cases" "${MODULE}/models" "${MODULE}/repositories" "${MODULE}/services" "${MODULE}/tests" "${MODULE}/tests/unit" "${MODULE}/tests/integration"; do
if [ ! -f "${d}/__init__.py" ]; then
echo "# package" > "${d}/__init__.py"
fi
done


# arquivos base com conteúdo inicial apenas se não existirem
write_if_missing() {
local path="$1"; shift
local content="$@"
if [ ! -f "$path" ]; then
printf "%s\n" "$content" > "$path"
fi
}


write_if_missing ${MODULE}/apps.py "from django.apps import AppConfig\n\nclass CartConfig(AppConfig):\n default_auto_field = 'django.db.models.BigAutoField'\n name = 'cart'\n verbose_name = 'Carrinho de Compras'"


write_if_missing ${MODULE}/models/__init__.py "# models package"
write_if_missing ${MODULE}/models/cart.py "# placeholder - veja implementacao real no arquivo models/cart.py gerado manualmente"
write_if_missing ${MODULE}/models/cart_item.py "# placeholder - veja implementacao real no arquivo models/cart_item.py gerado manualmente"


write_if_missing ${MODULE}/services/cart_service.py "# placeholder - veja implementacao real em services/cart_service.py"
write_if_missing ${MODULE}/api/serializers.py "# placeholder - serializers"
write_if_missing ${MODULE}/api/views.py "# placeholder - views"
write_if_missing ${MODULE}/repositories/cart_repository_impl.py "# placeholder - repository"
write_if_missing ${MODULE}/domain/data_access.py "# placeholder - data access"
write_if_missing ${MODULE}/domain/gateways.py "# placeholder - gateways"
write_if_missing ${MODULE}/domain/exceptions.py "# placeholder - exceptions"


write_if_missing ${MODULE}/tests/unit/test_models.py "# placeholder - tests for models"
write_if_missing ${MODULE}/tests/integration/test_cart_endpoints.py "# placeholder - integration tests"


echo "Estrutura criada/atualizada. Edite arquivos gerados conforme necessário."
