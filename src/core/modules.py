from ai.aiclient import *

GLOBAL_SYSTEM_MESSAGE = "You are an expert writing assistant"

# Base Module

class BaseModule:  
    prompt : Prompt = None
    function : Function = None
    
# MVP

class GrammarAssistant(BaseModule): 
    function = Function(
        "grammar_fix" , 
        "Fix any grammar mistakes and misspellings in the text" , 
        {
            "corrected_text": {
              "type": "string",
              "description": "Corrected text"
            }
        } , 
        ["corrected_text"]
    )
    
    def __init__(self , text):
        super().__init__()
        self.prompt = Prompt(GLOBAL_SYSTEM_MESSAGE , f"Fix thix text's grammar and misspellings: '{str(text)}'")
    
    

class Summarizer(BaseModule):  # Inheriting from BaseModule
    function = Function(
        "summarize_text", 
        "Summarize the provided text", 
        {
            "summarized_text": {
                "type": "string",
                "description": "Summarized version of the input text"
            }
        }, 
        ["summarized_text"]
    )
    
    def __init__(self, text: str):
        # Ensure prompt and function are set for the module
        super().__init__()  # Calls the BaseModule's __init__
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,  # This should be your system-wide message/context
            f"Summarize this text: '{text}'"
        )

class Humanizer(BaseModule):
    function = Function(
        "humanize_text", 
        "Humanize the provided text", 
        {
            "humanized_text": {
                "type": "string",
                "description": "More natural and human-like version of the input text"
            }
        }, 
        ["humanized_text"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Make the following text sound more human-like and natural: '{text}'"
        )

class ToneChange(BaseModule):
    function = Function(
        "change_tone", 
        "Change the tone of the provided text", 
        {
            "modified_text": {
                "type": "string",
                "description": "Text with the changed tone"
            }
        }, 
        ["modified_text"]
    )

    def __init__(self, text: str, tone: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Change the tone of the following text to {tone}: '{text}'"
        )

# Premium

class ContentExpander(BaseModule):
    function = Function(
        "expand_content", 
        "Expand the provided text into a more detailed version", 
        {
            "expanded_text": {
                "type": "string",
                "description": "More detailed version of the input text"
            }
        }, 
        ["expanded_text"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Expand the following text with more details and examples: '{text}'"
        )
        
class TextRewriting(BaseModule):
    function = Function(
        "rewrite_text", 
        "Rewrite the provided text while keeping its meaning intact", 
        {
            "rewritten_text": {
                "type": "string",
                "description": "Rewritten version of the input text"
            }
        }, 
        ["rewritten_text"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Rewrite the following text with different wording: '{text}'"
        )

class KeywordOptimizer(BaseModule):
    function = Function(
        "optimize_keywords", 
        "Optimize keywords in the provided text", 
        {
            "optimized_text": {
                "type": "string",
                "description": "SEO-optimized version of the input text"
            }
        }, 
        ["optimized_text"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Optimize the following text for SEO by improving keyword usage: '{text}'"
        )

class TextPersonalization(BaseModule):
    function = Function(
        "personalize_text", 
        "Personalize the provided text for the user", 
        {
            "personalized_text": {
                "type": "string",
                "description": "Personalized version of the input text"
            }
        }, 
        ["personalized_text"]
    )

    def __init__(self, text: str, user_name: str, user_preference: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Personalize the following text for {user_name} who prefers {user_preference}: '{text}'"
        )

# Utility
class PlagiarismChecker: 
    pass

class ReadabilityAnalyzer: 
    pass

class LanguageDetection(BaseModule):
    function = Function(
        "detect_language", 
        "Detect the language of the provided text", 
        {
            "language": {
                "type": "string",
                "description": "Detected language of the text"
            }
        }, 
        ["language"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Detect the language of the following text: '{text}'"
        )

class SentimentAnalysis(BaseModule):
    function = Function(
        "analyze_sentiment", 
        "Analyze the sentiment of the provided text", 
        {
            "sentiment": {
                "type": "string",
                "description": "Sentiment of the text (positive, negative, or neutral)"
            },
            "confidence": {
                "type": "string",
                "description": "Confidence score of the sentiment analysis , from 1 to 10"
            }
        }, 
        ["sentiment", "confidence"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Analyze the sentiment of the following text and classify it as positive, negative, or neutral: '{text}'"
        )

class EmotionRecognition(BaseModule):
    function = Function(
        "recognize_emotion", 
        "Recognize the emotion expressed in the provided text", 
        {
            "emotion": {
                "type": "string",
                "description": "Emotion expressed in the text (joy, sadness, anger, etc.)"
            },
            "confidence": {
                "type": "string",
                "description": "Confidence score of the emotion recognition , from 1 to 10"
            }
        }, 
        ["emotion", "confidence"]
    )

    def __init__(self, text: str):
        super().__init__()
        self.prompt = Prompt(
            GLOBAL_SYSTEM_MESSAGE,
            f"Recognize the emotion expressed in this text and provide the confidence score: '{text}'"
        )
