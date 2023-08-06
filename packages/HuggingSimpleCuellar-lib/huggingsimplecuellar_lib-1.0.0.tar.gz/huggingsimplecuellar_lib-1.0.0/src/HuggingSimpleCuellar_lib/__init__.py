import requests
import io
import torch
import tensorflow as tf
from PIL import Image
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from transformers import AutoTokenizer, AutoModelForCausalLM, TFAutoModelForCausalLM

def generate_image(model_name, token, prompt, title):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    image_bytes = response.content
    image = Image.open(io.BytesIO(image_bytes))
    image.save(f"{title}.png")

def generate_text(model_name, token, prompt, max_length):
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(api_url, headers=headers, json={"inputs": prompt, "max_length": max_length})
    output = response.json()[0]['generated_text']
    return output

def generate_transformers_text(model_name, prompt, max_length):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids
    generated_ids = model.generate(input_ids=input_ids, max_length=max_length)
    output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return output

def generate_transformersTF_text(model_name, prompt, max_length):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = TFAutoModelForCausalLM.from_pretrained(model_name)
    input_ids = tokenizer(prompt, return_tensors='tf').input_ids
    generated_ids = model.generate(input_ids=input_ids, max_length=max_length)
    output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return output    

def generate_image_diffusers(nombre_del_modelo, ingresa_prompt, nombre_de_la_imagen):
    model_id = nombre_del_modelo
    # Use the DPMSolverMultistepScheduler (DPM-Solver++) scheduler here instead
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cuda")
    prompt = ingresa_prompt
    image = pipe(prompt).images[0]    
    image.save(f"{nombre_de_la_imagen}.png")