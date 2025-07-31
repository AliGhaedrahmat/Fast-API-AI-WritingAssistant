from fastapi import FastAPI 
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from ai.aiclient import *
from core.modules import *
from core.engine import *
from fastapi import Request, HTTPException, Depends
from typing import Any
from fastapi.responses import JSONResponse
import logging
import os
from logging.handlers import RotatingFileHandler

# Set up logging with rotation
log_handler = RotatingFileHandler("app.log", maxBytes=5*1024*1024, backupCount=5)  # 5MB max size, 5 backup files
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(log_handler)

app = FastAPI()

config = load_config('config.json')

model_name = config.get("model_name")
api_key = os.getenv("API_KEY", "default_api_key")  # Fetch API key from environment variable
cost_per_thousand_input = 0.002
cost_per_thousand_output = 0.008

model = Model(model_name, cost_per_thousand_input, cost_per_thousand_output)
client = AIClient(model, api_key)

engine = Engine(client, model)

class TextRequest(BaseModel):
    text: str
    
class ToneChangeRequest(BaseModel):
    text: str
    target_tone: str
    
class StyleTransferRequest(BaseModel):
    text: str
    style: str

class TextPersonalizationRequest(BaseModel): 
    text: str
    user: str
    prefrence: str

class ResponseModel(BaseModel):
    status: str
    message: str
    data: Any

# API Key validation
api_key_header = APIKeyHeader(name="Authorization")
    
def get_api_key_from_header(authorization: str = Depends(api_key_header)) -> str:
    if authorization is None:
        raise HTTPException(status_code=400, detail="API key is missing")
    return authorization

def verify_api_key(authorization: str = Depends(get_api_key_from_header)):
    logger.info(f"Verifying API key")
    if authorization != api_key:
        logger.warning(f"Invalid API key")
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    return True

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "fail", "message": exc.detail}
    )

# MVP modules with API key validation and ResponseModel
@app.post("/grammar_assistance", summary="Fix grammar issues in text", tags=["Text Processing"])
async def grammar_fix(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received grammar fix request.")
    try:
        response = engine.run_module(GrammarAssistant(request.text))
        logger.info(f"Grammar fixed successfully.")
        return ResponseModel(status="success", message="Grammar fixed successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in grammar fix: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/humanizer", summary="Make text sound more human-like", tags=["Text Processing"])
async def humanizer(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received humanizer request.")
    try:
        response = engine.run_module(Humanizer(request.text))
        logger.info(f"Text humanized successfully.")
        return ResponseModel(status="success", message="Text humanized successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in humanizer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/summarizer", summary="Summarize a given text", tags=["Text Processing"])
async def summarizer(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received summarizer request.")
    try:
        response = engine.run_module(Summarizer(request.text))
        logger.info(f"Text summarized successfully.")
        return ResponseModel(status="success", message="Text summarized successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in summarizer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/tonechange", summary="Change the tone of a given text", tags=["Text Processing"])
async def tone_change(request: ToneChangeRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received tone change request.")
    try:
        response = engine.run_module(ToneChange(request.text , request.target_tone))
        logger.info(f"Tone changed successfully.")
        return ResponseModel(status="success", message="Tone changed successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in tone change: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Premium Modules with API key validation and ResponseModel
@app.post("/contentexpander", summary="Expand the content of a text", tags=["Premium Modules"])
async def content_expander(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received content expander request.")
    try:
        response = engine.run_module(ContentExpander(request.text))
        logger.info(f"Content expanded successfully.")
        return ResponseModel(status="success", message="Content expanded successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in content expander: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/textrewriting", summary="Rewrite a given text", tags=["Premium Modules"])
async def text_rewriting(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received text rewriting request.")
    try:
        response = engine.run_module(TextRewriting(request.text))
        logger.info(f"Text rewritten successfully.")
        return ResponseModel(status="success", message="Text rewritten successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in text rewriting: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/keywordoptimizer", summary="Optimize keywords in a given text", tags=["Premium Modules"])
async def keyword_optimizer(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received keyword optimizer request.")
    try:
        response = engine.run_module(KeywordOptimizer(request.text))
        logger.info(f"Keywords optimized successfully.")
        return ResponseModel(status="success", message="Keywords optimized successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in keyword optimizer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/textpersonalization", summary="Personalize text for a user", tags=["Premium Modules"])
async def text_personalization(request: TextPersonalizationRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received text personalization request.")
    try:
        response = engine.run_module(TextPersonalization(request.text, request.user, request.prefrence))  
        logger.info(f"Text personalized successfully.")
        return ResponseModel(status="success", message="Text personalized successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in text personalization: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Utility Modules API with API key validation and ResponseModel
@app.post("/languagedetection", summary="Detect the language of a given text", tags=["Utility Modules"])
async def language_detection(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received language detection request.")
    try:
        response = engine.run_module(LanguageDetection(request.text))
        logger.info(f"Language detected successfully.")
        return ResponseModel(status="success", message="Language detected successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in language detection: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/sentimentanalysis", summary="Analyze the sentiment of a text", tags=["Utility Modules"])
async def sentiment_analysis(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received sentiment analysis request.")
    try:
        response = engine.run_module(SentimentAnalysis(request.text))
        logger.info(f"Sentiment analysis completed.")
        return ResponseModel(status="success", message="Sentiment analysis completed", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/emotionrecognition", summary="Recognize emotions from text", tags=["Utility Modules"])
async def emotion_recognition(request: TextRequest, api_key_valid: bool = Depends(verify_api_key)):
    logger.info(f"Received emotion recognition request.")
    try:
        response = engine.run_module(EmotionRecognition(request.text))
        logger.info(f"Emotion recognized successfully.")
        return ResponseModel(status="success", message="Emotion recognized successfully", data=response.structured_arguments)
    except Exception as e:
        logger.error(f"Error occurred in emotion recognition: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
