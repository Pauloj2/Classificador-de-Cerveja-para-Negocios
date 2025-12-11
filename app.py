"""
Sistema de Classificação de Cervejas - Backend
FastAPI com PMML Model
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from pypmml import Model
import os
from typing import Dict
import pandas as pd

app = FastAPI(title="Beer Classifier API")

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CONFIGURAÇÃO DO MODELO PMML
# ============================================
# ALTERE AQUI o caminho do seu arquivo PMML
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PMML_MODEL_PATH = os.path.join(BASE_DIR, "models", "random_forest_cervejas.pmml")


# Variável global para armazenar o modelo carregado
pmml_model = None


def load_pmml_model():
    global pmml_model
    
    print(f"📁 Tentando carregar modelo em: {PMML_MODEL_PATH}")

    if not os.path.exists(PMML_MODEL_PATH):
        print("❌ Modelo NÃO encontrado no caminho real dentro do container.")
        return
    
    try:
        pmml_model = Model.load(PMML_MODEL_PATH)
        print(f"✅ Modelo PMML carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo PMML: {e}")


# Carregar modelo na inicialização
@app.on_event("startup")
async def startup_event():
    load_pmml_model()


# ============================================
# MODELOS DE DADOS (REQUEST/RESPONSE)
# ============================================

class BeerFeatures(BaseModel):
    """
    Modelo de dados para as características da cerveja.
    
    IMPORTANTE: Todos os valores devem estar normalizados entre 0 e 1,
    pois o modelo foi treinado com dados nessa escala.
    """
    review_aroma: float = Field(..., ge=0.0, le=1.0, description="Avaliação do aroma (0-1)")
    review_appearance: float = Field(..., ge=0.0, le=1.0, description="Avaliação da aparência (0-1)")
    review_palate: float = Field(..., ge=0.0, le=1.0, description="Avaliação do paladar (0-1)")
    review_taste: float = Field(..., ge=0.0, le=1.0, description="Avaliação do sabor (0-1)")
    beer_abv: float = Field(..., ge=0.0, le=1.0, description="Teor alcoólico normalizado (0-1)")
    
    @field_validator('*')
    @classmethod
    def clamp_values(cls, v):
        """
        Garante que os valores estão dentro do intervalo [0, 1].
        Se estiver fora, faz o clamp para os limites.
        """
        if v < 0.0:
            return 0.0
        if v > 1.0:
            return 1.0
        return v


class PredictionResponse(BaseModel):
    """Modelo de resposta da predição"""
    prediction: str
    probabilities: Dict[str, float]


# ============================================
# ENDPOINTS DA API
# ============================================

@app.get("/")
async def root():
    """Endpoint raiz - informações da API"""
    return {
        "message": "Beer Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/predict (POST)"
        },
        "model_loaded": pmml_model is not None
    }


@app.get("/health")
async def health_check():
    """Health check - verifica se o modelo está carregado"""
    return {
        "status": "healthy" if pmml_model is not None else "degraded",
        "model_loaded": pmml_model is not None,
        "model_path": PMML_MODEL_PATH
    }


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_beer_quality(features: BeerFeatures):
    """
    Endpoint de predição de qualidade da cerveja.
    
    Recebe as características da cerveja normalizadas (0-1) e retorna:
    - prediction: "Boa" ou "Ruim"
    - probabilities: probabilidades simuladas para cada classe
    
    NOTA SOBRE NORMALIZAÇÃO:
    - O modelo espera valores entre 0 e 1 (dados normalizados).
    - Se você quiser aceitar valores em outras escalas (ex: ABV em %),
      adicione uma função de pré-processamento aqui antes de chamar o modelo.
    """
    
    # Verificar se o modelo está carregado
    if pmml_model is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "Modelo PMML não disponível",
                "message": f"O arquivo {PMML_MODEL_PATH} não foi encontrado ou não pôde ser carregado.",
                "solution": "Verifique se o arquivo PMML existe no caminho especificado."
            }
        )
    
    try:
        # Preparar dados de entrada como DataFrame (formato esperado pelo pypmml)
        input_df = pd.DataFrame([{
            'review_aroma': features.review_aroma,
            'review_appearance': features.review_appearance,
            'review_palate': features.review_palate,
            'review_taste': features.review_taste,
            'beer_abv': features.beer_abv
        }])
        
        print(f"📊 Input enviado ao modelo: {input_df.to_dict('records')[0]}")
        
        # Fazer a predição usando o modelo PMML
        result = pmml_model.predict(input_df)
        
        print(f"🔍 Resultado bruto do modelo:")
        print(f"   Tipo: {type(result)}")
        print(f"   Conteúdo: {result}")
        if hasattr(result, 'columns'):
            print(f"   Colunas: {result.columns.tolist()}")
            print(f"   Valores: {result.iloc[0].to_dict()}")
        
        # Extrair a predição da coluna 'classe_cerveja'
        prediction = None
        
        # Tentar diferentes nomes de coluna
        possible_column_names = [
            'classe_cerveja',
            'predicted_classe_cerveja', 
            'prediction',
            'qualidade',
            'predicted_qualidade'
        ]
        
        for col_name in possible_column_names:
            if col_name in result.columns:
                prediction = str(result[col_name].iloc[0])
                print(f"✅ Predição encontrada na coluna '{col_name}': {prediction}")
                break
        
        # Se não encontrou por nome, pegar a primeira coluna
        if prediction is None:
            prediction = str(result.iloc[0, 0])
            print(f"⚠️ Usando primeira coluna como predição: {prediction}")
        
        # Garantir que a predição é "Boa" ou "Ruim"
        prediction = prediction.strip()
        
        if prediction not in ['Boa', 'Ruim']:
            print(f"⚠️ Valor inesperado: '{prediction}'. Tentando converter...")
            # Tentar converter valores numéricos ou booleanos
            prediction_lower = prediction.lower()
            if prediction_lower in ['0', '0.0', 'false', 'ruim', 'bad']:
                prediction = 'Ruim'
            elif prediction_lower in ['1', '1.0', 'true', 'boa', 'good']:
                prediction = 'Boa'
            else:
                print(f"❌ Não foi possível converter '{prediction}' para Boa/Ruim")
                prediction = 'Boa'  # Valor padrão
        
        print(f"✅ Predição final: {prediction}")
        
        # Calcular probabilidades simuladas baseadas na média dos atributos
        # (já que o modelo PMML não retorna probabilidades explícitas)
        avg_score = (
            features.review_aroma + 
            features.review_appearance + 
            features.review_palate + 
            features.review_taste
        ) / 4.0
        
        # Ajustar probabilidades baseado no score médio
        if prediction == 'Boa':
            prob_boa = 0.5 + (avg_score * 0.4)  # Entre 0.5 e 0.9
            prob_ruim = 1.0 - prob_boa
        else:
            prob_ruim = 0.5 + ((1.0 - avg_score) * 0.4)  # Entre 0.5 e 0.9
            prob_boa = 1.0 - prob_ruim
        
        return PredictionResponse(
            prediction=prediction,
            probabilities={
                "Boa": round(float(prob_boa), 3),
                "Ruim": round(float(prob_ruim), 3)
            }
        )
        
    except Exception as e:
        print(f"❌ ERRO: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro ao processar predição",
                "message": str(e),
                "type": type(e).__name__
            }
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("🍺 Beer Classifier API")
    print("=" * 60)
    print(f"📁 Caminho do modelo PMML: {PMML_MODEL_PATH}")
    print(f"🚀 Iniciando servidor em http://0.0.0.0:{port}")
    print(f"📖 Documentação: http://0.0.0.0:{port}/docs")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)