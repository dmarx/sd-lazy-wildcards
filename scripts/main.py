# scavenged from https://github.com/FartyPants/sd_web_ui_scripts/blob/main/scripts/hallucinate.py

from modules.shared import opts
from modules.processing import Processed, process_images, images
import modules.scripts as scripts
import gradio as gr
#import openai # TODO: more generic


ONTOLOGY_PROMPT="respond only with a bulleted list of {n} members of the following ontology: {text}"


class Wildcard:
    def __init__(self, text:str, prompt_template:str=ONTOLOGY_PROMPT):
        self.text = text
        self.prompt_template = prompt_template
        self.parse()
    def materialize(self, n:int=1) -> str:
        prompt = self.prompt_template.format(n=n, text=self.text_)
        return self.text
    def parse(self):
        # TODO: implement
        self.text_ = self.text


def replace_wildcards(text):
    return text
    # TODO: implementation
    outv = ""
    for chunk in segment(text):
        if is_wildcard(chunk):
            chunk = Wildcard(chunk).materialize()
        outv += chunk
    return outv
        


class Script(scripts.Script):
    def title(self):
        return "Hallucinate"

    def ui(self, is_img2img):
        enable_m = gr.Checkbox(label="Yes please, Hallucinate about Monsters", value=True, elem_id=self.elem_id("enable"))
       
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
