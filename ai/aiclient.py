import os
import openai
import json
from typing import List, Dict, Optional, Any

# # print the openai module version
# print(f"OpenAI Version: {openai.__version__}")
class CostCalculator:
    @staticmethod
    def calculate_cost(prompt_tokens: int, completion_tokens: int, cost_per_thousand_input: float, cost_per_thousand_output: float) -> float:
        input_cost = (prompt_tokens / 1000) * cost_per_thousand_input
        output_cost = (completion_tokens / 1000) * cost_per_thousand_output
        return input_cost + output_cost


def load_config(config_file: str) -> Dict[str, str]:
    with open(config_file, 'r') as f:
        return json.load(f)

class Model: 
    def __init__(self , name , cost_per_thousand_input , cost_per_thousand_output):
        self.name = name 
        self.cost_per_thousand_input = cost_per_thousand_input
        self.cost_per_thousand_output = cost_per_thousand_output

class Prompt: 
    system_content : str
    user_content: str
    
    def __init__(self , system_content , user_content):
        self.system_content = system_content
        self.user_content = user_content
        
    def get_messages(self) -> list: 
        return [
            {"role": "system", "content": self.system_content},
            {"role": "user", "content": self.user_content}
        ]

class Function: 
    name: str
    description: str
    properties : dict
    required: list[str]
    strict : bool = False
    additional_properties : bool = False
    
    def __init__(self , name , description , properties , required , strict = False , additional_properties = False):
        self.name = name
        self.description = description
        self.properties = properties
        self.required = required 
        self.strict = strict
        self.additional_properties = additional_properties
    
    
    def get_dict(self): 
        function_dict = {
          "name": self.name,
          "description": self.description,
          "strict": self.strict,
          "parameters": {
            "type": "object",
            "properties": self.properties,
            "required": self.required,
            "additionalProperties": self.additional_properties
          }
        }
        
        return function_dict

class Response: 
    successful : bool
    #response_dict : dict
    structured_arguments : dict
    input_tokens: int
    output_tokens: int
    cost: int
    model : Model

    def __init__(self , model , response):
        self.model = model
        arguments = response.choices[0].message.function_call.arguments
        self.structured_arguments = json.loads(arguments)
        usage = response.usage
        self.input_tokens = usage.prompt_tokens
        self.output_tokens = usage.completion_tokens
        self.cost = CostCalculator.calculate_cost(self.input_tokens , self.output_tokens , self.model.cost_per_thousand_input , self.model.cost_per_thousand_output)

    def get_dict(self): 
        return {
            "structured_arguments" : self.structured_arguments , 
            "input_tokens" : self.input_tokens , 
            "output_tokens" : self.output_tokens , 
            "cost_in_dollors" : self.cost , 
            "cost_in_irt" : (self.cost * 100000)
        }

    def log(self): 
        print(self.get_dict())
    

class AIClient: 
    model : Model
    
    def __init__(self , model , api_key):
        self.model = model
        self.api_key = api_key
        openai.api_key = self.api_key

    def set_model(self, model: Model): self.model = model
    def set_api_key(self, api_key) : 
        self.api_key = api_key
        openai.api_key = self.api_key

    def chat(self , prompt: Prompt , function: Function , temperature=0.7 , max_tokens = 512): 
        client = openai.OpenAI(
            api_key=self.api_key
        )
        response = client.chat.completions.create(
        model=self.model.name,
        messages=prompt.get_messages(),
        function_call= {"name": function.name} , 
        functions=[function.get_dict()],
        temperature=temperature,
        max_tokens=max_tokens
        )
        # print(response)        
        return Response(self.model , response)