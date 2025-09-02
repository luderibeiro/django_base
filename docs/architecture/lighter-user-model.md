# Refatorando o Modelo de Usuário do Django para uma Entidade mais Leve

Esta seção detalha o processo de refatoração do modelo `User` do Django para que ele seja uma entidade de persistência mais leve, com menos acoplamento ao framework Django e mais alinhada com a camada de Domínio da Arquitetura Limpa.

## 1. Contexto e Justificativa

Originalmente, o modelo `User` do Django herda de `AbstractUser`, o que traz consigo muitas funcionalidades e dependências específicas do framework (permissões, grupos, etc.). Embora conveniente, isso pode levar a um forte acoplamento da camada de Domínio à Infraestrutura (Django). O objetivo desta refatoração é isolar a entidade de Domínio `User` e fazer com que o modelo Django atue apenas como um adaptador de persistência.

## 2. Abordagem da Refatoração

### a. Modelo `User` do Django (`project/core/models/user.py`)

O modelo `User` será simplificado. Em vez de herdar diretamente de `AbstractUser`, ele pode herdar de `AbstractBaseUser` (se a necessidade de personalização for alta) ou até mesmo ser um modelo simples, delegando a gestão de permissões e outras características do `AbstractUser` para a camada de Infraestrutura, onde o mapeamento para a entidade de Domínio ocorre.

(Detalhes das alterações no arquivo `project/core/models/user.py` serão adicionados aqui)

### b. Entidade de Domínio `User` (`project/core/domain/entities/user.py`)

Esta entidade já foi criada para ser agnóstica a frameworks. A refatoração garantirá que ela contenha apenas os atributos e métodos de negócio essenciais, sem qualquer dependência do Django.

(Revisão e confirmação de que esta entidade permanece puramente de domínio será adicionada aqui)

### c. Repositório de Usuário (`project/core/repositories/user_repository_impl.py`)

O `DjangoUserRepository` será a principal ponte entre a entidade de Domínio `User` e o modelo de persistência do Django. Ele será responsável por:

- Converter a entidade de Domínio `User` para o modelo Django antes de salvar.
- Converter o modelo Django para a entidade de Domínio `User` após a leitura do banco de dados.
- Gerenciar as operações de persistência usando o ORM do Django, sem expor esses detalhes às camadas superiores.

(Detalhes das alterações no arquivo `project/core/repositories/user_repository_impl.py` serão adicionados aqui)

### d. Impacto em Casos de Uso, Serializers e Views

Idealmente, os Casos de Uso, Serializers e Views não deveriam ser afetados por esta mudança, pois eles já interagem com a entidade de Domínio `User` e seus DTOs, e não diretamente com o modelo Django. Qualquer ajuste necessário será documentado.

## 3. Passos da Implementação

(Os passos técnicos detalhados serão adicionados aqui à medida que a refatoração for implementada.)
