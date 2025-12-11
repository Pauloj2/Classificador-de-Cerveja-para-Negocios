# 🍺 Sistema de Classificação de Cervejas

Sistema web completo para classificação de cervejas usando Machine Learning com modelo PMML.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## 🚀 Instalação e Execução

### 1. Estrutura de Pastas

Organize seu projeto com a seguinte estrutura:

```
beer-classifier/
│
├── app.py                          # Backend FastAPI
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
│
├── models/
│   └── random_forest_cervejas.pmml # Seu modelo PMML (COLOQUE AQUI!)
│
└── static/
    └── index.html                  # Frontend (interface web)
```

### 2. Instalar Dependências

Abra o terminal na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 3. Configurar o Modelo PMML

**IMPORTANTE:** Coloque seu arquivo PMML na pasta `models/` com o nome `random_forest_cervejas.pmml`

Se seu arquivo tiver outro nome ou localização, edite a linha 22 do arquivo `app.py`:

```python
PMML_MODEL_PATH = "models/SEU_ARQUIVO.pmml"  # Altere aqui
```

### 4. Iniciar o Backend

No terminal, execute:

```bash
python app.py
```

Você verá uma mensagem como:

```
✅ Modelo PMML carregado com sucesso de: models/random_forest_cervejas.pmml
🚀 Iniciando servidor em http://localhost:8000
```

**Deixe este terminal aberto!** O backend precisa estar rodando.

### 5. Abrir o Frontend

Abra o arquivo `static/index.html` no seu navegador web ou configure um servidor local:

```bash
# Opção 1: Abrir diretamente
# Navegue até a pasta static/ e abra index.html no navegador

# Opção 2: Usar servidor HTTP simples do Python (recomendado)
cd static
python -m http.server 8080
# Acesse: http://localhost:8080
```

## 🎯 Como Usar

1. **Ajuste os valores** usando os sliders:
   - Aroma (0 a 1)
   - Aparência (0 a 1)
   - Paladar (0 a 1)
   - Sabor (0 a 1)
   - Teor Alcoólico/ABV (0 a 1)

2. **Clique em "Classificar Cerveja"**

3. **Veja o resultado:**
   - Classificação: "Cerveja Boa" ou "Cerveja Ruim"
   - Probabilidades de cada classe

## ⚙️ Sobre a Normalização

**IMPORTANTE:** Este sistema espera valores **já normalizados** entre 0 e 1, pois o modelo foi treinado com dados nessa escala.

### Se você quiser usar valores originais (não normalizados):

Por exemplo, se ABV original era em porcentagem (0% a 30%):

1. Edite o arquivo `app.py`
2. Adicione uma função de normalização antes da predição:

```python
def normalize_abv(abv_percent):
    """Converte ABV de % para escala 0-1"""
    return abv_percent / 30.0  # Assumindo máximo de 30%

# Use na função de predição:
input_data = {
    'beer_abv': normalize_abv(features.beer_abv),  # Se receber em %
    # ... outros campos
}
```

3. Ajuste o frontend para aceitar valores em % (alterar `max` dos sliders)

## 🔧 Endpoints da API

### GET /
- Informações gerais da API

### GET /health
- Health check (verifica se modelo está carregado)

### POST /api/predict
- **Rota de predição**
- Body (JSON):
```json
{
  "review_aroma": 0.85,
  "review_appearance": 0.90,
  "review_palate": 0.75,
  "review_taste": 0.88,
  "beer_abv": 0.15
}
```
- Response:
```json
{
  "prediction": "Boa",
  "probabilities": {
    "Boa": 0.913,
    "Ruim": 0.087
  }
}
```

## 📚 Documentação Interativa

Acesse a documentação Swagger da API em:
```
http://localhost:8000/docs
```

## 🐛 Solução de Problemas

### Erro: "Modelo PMML não disponível"
- Verifique se o arquivo PMML existe na pasta `models/`
- Confirme o nome do arquivo em `app.py` (linha 22)

### Erro: "Connection refused" no frontend
- Certifique-se que o backend está rodando (`python app.py`)
- Verifique se está na porta correta (8000)

### Erro: "CORS policy"
- O backend já está configurado para aceitar requisições de qualquer origem
- Se persistir, verifique se ambos estão na mesma rede

## 🎨 Personalização

### Alterar cores do frontend
Edite as variáveis CSS em `index.html`:
- `#C68A24` - Dourado escuro
- `#F2C14E` - Dourado claro
- `#1F1F1F` - Cinza escuro
- `#4CAF50` - Verde (cerveja boa)
- `#F44336` - Vermelho (cerveja ruim)

### Alterar porta do backend
Em `app.py`, linha final:
```python
uvicorn.run(app, host="0.0.0.0", port=NOVA_PORTA)
```

## 📝 Licença

Projeto educacional - livre para uso e modificação.

## 🤝 Suporte

Se encontrar problemas:
1. Verifique os logs do terminal onde o backend está rodando
2. Abra o Console do navegador (F12) para ver erros do frontend
3. Confirme que todas as dependências foram instaladas corretamente