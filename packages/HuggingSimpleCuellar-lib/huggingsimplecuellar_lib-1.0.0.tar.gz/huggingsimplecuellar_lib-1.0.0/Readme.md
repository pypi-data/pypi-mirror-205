#HuggingSimpleCuellar_lib

Una libreria simple para usar modelos de huggingface de forma sencilla en pocas lineas de codigo
Ya sea con transformers o usando la api de request de huggingface, puedes generar imagenes de forma rapida con Stable diffusion

instalacion de la libreria:

```shell
pip3 install HuggingSimpleCuellar_lib
```

Genera Imagenes usando la api de huggingface:

```python
from HuggingSimpleCuellar_lib import generate_image

generate_image(
    model_name="Ingresa_modelo_Stable diffusion",
    token="Tu_token_hugging",
    prompt="descripcion de la imagen",
    title="Titulo para guardar la Imagen"
)
```
Para generar texto usando la Api:

```python
from HuggingSimpleCuellar_lib import generate_text

generated_text = generate_text(
    model_name="EleutherAI/gpt-neo-125m",
    token="Tu_Token_Huggingface",
    prompt="Can you please let us know more details about your",
    max_length=50
)

print(generated_text)
```

Para generar texto usando transformers:

```python
from HuggingSimpleCuellar_lib import generate_transformers_text

generated_transformers_text = generate_transformers_text(
    model_name="Emilianohack6950/M.A.R.I.A",
    prompt="Hello, how are you?",
    max_length=50
)

print(generated_transformers_text)
```

si quieres usar un modelo de tensorflow:

```python
from HuggingSimpleCuellar_lib import generate_transformers_text

generated_transformersTF_text = generate_transformersTF_text(
    model_name="Emilianohack6950/M.A.R.I.A",
    prompt="Hello, how are you?",
    max_length=50
)

print(generated_transformers_text)
```

Para generar imagenes con Stable diffusion en caso de tener una Gpu en tu ordenador:

```python
from HuggingSimpleCuellar_lib import generate_image_diffusers

generate_image_diffusers = generate_image_diffusers(
    nombre_del_modelo="Nombre_del_modelo_Stable_diffusion", 
    ingresa_prompt="Descripcion_de_la_imagen", 
    nombre_de_la_imagen="Nombre_a_guardar_la_imagen
)
```

Por el momento la libreria aun se encuentra en desarrollo pronto se le agregaran mas cosas como entrenamiento de modelos de lenguaje usando la api de transformers en pocas lineas de codigo