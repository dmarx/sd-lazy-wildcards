# scavenged and modified from https://github.com/FartyPants/sd_web_ui_scripts/blob/main/scripts/hallucinate.py

import random

from modules.shared import opts
from modules.processing import Processed, process_images, images
import modules.scripts as scripts
import gradio as gr
import openai # TODO: more generic


ONTOLOGY_PROMPT=(
    "I'm building an ontology. please propose a list of at least {n} members that fit the following ontology category: ```{text}```."
    'please respond with a bulleted list. each item in the list should be on its own line and preceded by an asterisk ("* item\n").'
)

def invoke_llm(prompt, **kargs):
    completions = openai.ChatCompletion.create(
        messages=[
            #{"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ], **kargs)
    return completions.choices[0]['message']['content'].strip()


class Wildcard:
    _options_cache = {}
    def __init__(self, text:str, prompt_template:str=ONTOLOGY_PROMPT):
        self.text = text
        self.prompt_template = prompt_template
    def materialize(self, n:int=20) -> str:
        prompt = self.prompt_template.format(n=n, text=self.text)
        self._options_cache[self.text] = self.options_from_prompt(prompt)
    def fill(self):
        if self.text not in self._options_cache:
            self.materialize()
        options = self._options_cache.get(self.text)
        return random.choice(options)
    def options_from_prompt(self, prompt):
        response = invoke_llm(prompt)
        options = []
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("*"):
                value = line[1:].strip()
                options.append(value)
        return options
            

def replace_wildcards(text):
    return text
    # TODO: implementation
    chunks = []
    for chunk in text.split():
        if chunk.startswith('__'):
            chunk = Wildcard(chunk).fill()
        chunks += [chunk]
    return ' '.join(chunks)
        


class Script(scripts.Script):
    def title(self):
        return "Lazy Wildcards"

    def ui(self, is_img2img):
        enable_m = gr.Checkbox(label="Activate", value=True, elem_id=self.elem_id("enable"))
       
        return [enable_m]

    def run(self, p, enable_m):
        all_prompts = []
        infotexts = []

        if (enable_m==True):
            p.prompt = replace_wildcards(p.prompt)
            p.negative_prompt = replace_wildcards(p.negative_prompt)

        proc = process_images(p)
        all_prompts = proc.all_prompts
        infotexts = proc.infotexts
        return Processed(p, proc.images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts)
