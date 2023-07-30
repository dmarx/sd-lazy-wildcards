# Lazy Prompt Wildcards for SD-WebUI

This extension is inspired by https://github.com/adieyal/sd-dynamic-prompts/. To use wildcards in the dynamic prompts extension, you need to prepopulate text files with candidate words to use for wildcard filling. I'm lazy and don't feel like going to the trouble of curating a complex ontology, and with the power of LLMs I don't need to! This extension let's you pretend you have whatever ontology you want already constructed and available and just fills the values in for you on the fly as you need them.

# Setup

Setup is the same as any other webui extension, with the addition of putting your OpenAI API Key somewhere that the extension can find it. 
You have two options here:

1. attach your key to the `OPENAI_API_KEY` environment variable
2. save your key to a file named `KEY.txt` and place that inside the `sd-lazy-wildcards` folder (i.e. the folder for this extension).

# Use

A "wildcard" in your prompt must satisfy the following to be read correctly by the extension:

* Start and end with double underscores enclosed by white space
* contains no white space

The text contained between those double underscores will then be passed into the following prompt with n=20 (users will have more control over `n` in the future):

```python
ONTOLOGY_PROMPT=(
    "I'm building an ontology. please propose a list of at least {n} members that fit the following ontology category: ```{text}```."
    'please respond with a bulleted list. each item in the list should be on its own line and preceded by an asterisk ("* item\n").'
)
```

I recommend using a forward-slash separated hierarchy for your wildcard, e.g. `__places/usa/major_cities__`. 
