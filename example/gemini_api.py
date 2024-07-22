import google.generativeai as genai
import configparser

class GeminiAPI:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config['DEFAULT']['GOOGLE_API_KEY']
        self.model = None
        self.configure()

    def configure(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_content(self, input_text):
        try:
            response = self.model.generate_content(input_text)
            return response.text
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            return None