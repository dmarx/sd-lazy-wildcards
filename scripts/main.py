# scavenged from https://github.com/FartyPants/sd_web_ui_scripts/blob/main/scripts/hallucinate.py

from modules.shared import opts
from modules.processing import Processed, process_images, images
import modules.scripts as scripts
import gradio as gr
#import openai # TODO: more generic


ONTOLOGY_PROMPT="respond only with a bulleted list of {n} members of the following ontology: {ontology}"


class Wildcard:
    def __init__(self, text, prompt_template=ONTOLOGY_PROMPT):
        self.text = text
        self.parse()
    def materialize(self, n=1):
        pass

class Script(scripts.Script):
    def title(self):
        return "Hallucinate"

    def ui(self, is_img2img):
        enable_m = gr.Checkbox(label="Yes please, Hallucinate about Monsters", value=True, elem_id=self.elem_id("enable"))
       
        return [enable_m]

    def run(self, p,enable_m):
        all_prompts = []
        infotexts = []

        if (enable_m==True):
            #initial_prompt =  p.prompt
            #p.prompt = p.negative_prompt
            #p.negative_prompt = initial_prompt
            pass

        proc = process_images(p)
        all_prompts = proc.all_prompts
        infotexts = proc.infotexts
        return Processed(p, proc.images, p.seed, "",all_prompts=all_prompts,infotexts=infotexts)
