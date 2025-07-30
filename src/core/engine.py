from ai.aiclient import *
from .modules import *

class Engine:
    def __init__(self, ai_client: AIClient, model: Model):
        self.ai_client = ai_client
        self.model = model

    def run_module(self, module: BaseModule):
        if isinstance(module, BaseModule):
            if module.prompt and module.function:
                try:
                    # Run the module's function with the prompt and function
                    response = self.ai_client.chat(module.prompt, module.function)
                    response.log()  # Log the response
                    return response
                except Exception as e:
                    print(f"[Error] AI client failed: {e}")
            else:
                print("[Error] Module prompt or function not set")
        else:
            print("[Error] Invalid module type")
