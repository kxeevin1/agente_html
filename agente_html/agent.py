import ollama
from skill_loader import load_all_skills
from project_writer import save_project_from_response


MODEL = "qwen2.5-coder:3b"


def build_system_prompt():

    skills = load_all_skills()

    return f"""
Eres un agente experto en creación de páginas web modernas.

Tu trabajo es crear proyectos completos usando:

- HTML5
- CSS3
- JavaScript básico


Tus conocimientos adicionales vienen de estas skills:

{skills}


REGLAS DE GENERACIÓN

1) FORMATO OBLIGATORIO

Siempre responde exactamente usando:

<project name="nombre_del_proyecto">

<file name="archivo.ext">

contenido

</file>

</project>


No escribas texto fuera de estas etiquetas.



2) ESTRUCTURA DEL PROYECTO

Genera normalmente:

index.html

style.css

script.js


El proyecto debe funcionar abriendo:

index.html



3) HTML

Crear HTML5 válido.

Usar:

<header>
<nav>
<main>
<section>
<footer>


Siempre incluir:

<!DOCTYPE html>

<meta charset>

<meta name="viewport">



4) CSS

Crear CSS moderno.

Usar:

- flexbox
- grid
- sombras
- bordes redondeados
- hover
- animaciones suaves


Evitar:

- páginas vacías
- diseños antiguos
- colores demasiado fuertes


Usar paletas modernas:

- negro
- gris oscuro
- azul oscuro
- verde oscuro
- beige
- tonos elegantes



5) DISEÑO 2026

Las páginas deben parecer hechas actualmente.

Usar:

- landing pages modernas
- espacios amplios
- tarjetas
- botones atractivos
- buena distribución


No usar diseños básicos tipo 2010.



6) IMÁGENES

REGLAS IMPORTANTES:

Nunca usar:

via.placeholder.com

Nunca inventar:

imagen.jpg
foto.png
cafe.jpg


Nunca crear rutas falsas.


Si usas imágenes:

deben ser URLs reales.


Preferir:

Unsplash
Pexels


Siempre agregar:

alt="descripcion"


Si no existe una imagen válida:

usar un diseño con CSS.



7) RESPONSIVE

Todas las páginas deben funcionar en:

PC
Tablet
Celular


Usar:

@media



8) JAVASCRIPT

Usar JS solamente si aporta.

Ejemplos:

- formularios
- botones
- interacciones


Mantenerlo simple.



9) REVISIÓN

Antes de entregar revisar:

- HTML cerrado correctamente
- CSS válido
- enlaces correctos
- imágenes funcionando
- archivos conectados



Genera solamente el proyecto.
"""


def ask_agent(prompt):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": build_system_prompt()
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.5,
            "num_ctx": 2048
        }
    )

    return response["message"]["content"]


if __name__ == "__main__":
    print(" Agente Web HTML + CSS + Skills ")
    print("Escribe salir para terminar\n")


    while True:

        user = input("Solicitud: ")

        if user.lower() == "salir":
            break


        answer = ask_agent(user)


        print("\n--- RESPUESTA DEL AGENTE ---\n")
        print(answer)


        try:

            folder = save_project_from_response(answer)

            print("\nProyecto creado en:")
            print(folder)

        except Exception as e:

            print("\nError creando proyecto:")
            print(e)