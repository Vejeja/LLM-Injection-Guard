class CanaryDetector:
    def __init__(self):
        self.canary_phrase = "flibbertigibbet"
        
    def get_modified_input(self, prompt: str) -> str:
        modified_prompt = prompt + " " + self.canary_phrase
        return modified_prompt
    
    def check(self, response: str) -> bool:        
        if response is None:
            return False
        return self.canary_phrase in response