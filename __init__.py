from openai import OpenAI
import os
import re
from dotenv import load_dotenv

load_dotenv()

class CoderLLM:
  CATEGORY = "AppGen"
  RETURN_TYPES = ("CODER_LLM",)
  RETURN_NAMES = ("coder_llm",)
  FUNCTION = "execute"
  
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "base_url": ("STRING", {"default": os.environ.get("DEFAULT_LLM_BASE_URL", "")}),
        "api_key": ("STRING", {"default": os.environ.get("DEFAULT_LLM_API_KEY", "")}),
        "model": ("STRING", {"default": os.environ.get("DEFAULT_LLM_MODEL", "")}),
      }
    }
    
  def execute(self, base_url, api_key, model):
    client = OpenAI(base_url=base_url, api_key=api_key)
    client.model = model
    return (client,)
    
class AppGen:
  CATEGORY = "AppGen"
  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("html",)
  FUNCTION = "execute"
  
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "coder_llm": ("CODER_LLM", {}),
        "query": ("STRING", {"multiline": True, "default": "Create a calculator app with a clean modern design. Include basic arithmetic operations (add, subtract, multiply, divide) and a clear button. The calculator should support decimal numbers and display the current calculation."}),
      },
      "hidden": {
        "unique_id": "UNIQUE_ID",
      },
    }
  
  def construct_prompt(self, **kwargs):
    query = kwargs["query"]
    prompt = f'''
<query>Generate a single HTML file based on this query: "{query}"</query>`
<output instructions>
The output should be valid HTML and should be creative and well-structured. Use Tailwind CSS, load it in the <head> tag with <script src="https://cdn.tailwindcss.com"></script>.
Return the HTML content wrapped in triple backticks with 'html' language specifier, like this:
```html
<your html code here>
```
</output instructions>
    '''
    return prompt
  
  def execute(self, coder_llm, **kwargs):
    prompt = self.construct_prompt(**kwargs)
    completion = coder_llm.chat.completions.create(
      messages=[ {"role": "user", "content": prompt} ],
      model=coder_llm.model,
      temperature=0.1,
      max_tokens=8192,
      top_p=1,
      stream=False,
    )
    html = completion.choices[0].message.content
    pattern = r"```html\n([\s\S]*?)\n```"
    match = re.search(pattern, html)
    if match:
      clean_html = match.group(1)
    else:
      clean_html = ""
    return (clean_html, )

class AppEdit(AppGen):
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "coder_llm": ("CODER_LLM", {}),
        "html": ("STRING", {"forceInput": True}),
        "feedback": ("STRING", {"multiline": True}),
      },
      "hidden": {
        "unique_id": "UNIQUE_ID",
      },
    }    
    
  def construct_prompt(self, **kwargs):
    html = kwargs["html"]
    feedback = kwargs["feedback"]
    prompt = f'''
<current html>{html}</current html>`
<feedback>{feedback}</feedback>
<output instructions>
The output should be valid HTML and should be creative and well-structured. Use Tailwind CSS, load it in the <head> tag with <script src="https://cdn.tailwindcss.com"></script>.
Return the HTML content wrapped in triple backticks with 'html' language specifier, like this:
```html
<your html code here>
```
</output instructions>
    '''
    return prompt
    
class AppSandbox:
  CATEGORY = "AppGen"
  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("html",)
  FUNCTION = "execute"
  OUTPUT_NODE = True
  
  @classmethod
  def INPUT_TYPES(s):
    return {
      "required": {
        "html": ("STRING", {"forceInput": True}),
      }
    }
    
  def execute(self, html):
    return {"ui": {"text": html}, "result": (html,)}
    
NODE_CLASS_MAPPINGS = {
  "AG_CODER_LLM": CoderLLM,
  "AG_APP_GEN": AppGen,
  "AG_APP_EDIT": AppEdit,
  "AG_APP_SANDBOX": AppSandbox,
}    

NODE_DISPLAY_NAME_MAPPINGS = {
  "AG_CODER_LLM": "Coder LLM",
  "AG_APP_GEN": "App. Generator",
  "AG_APP_EDIT": "App. Editor",
  "AG_APP_SANDBOX": "App. Sandbox",
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]