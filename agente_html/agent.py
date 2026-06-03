import ollama
from skill_loader import load_all_skills
from project_writer import save_project_from_response


MODEL = "qwen2.5-coder:3b"


def build_system_prompt():

    skills = load_all_skills()

    return f"""
Eres un agente especializado en crear páginas web modernas.

Tu tarea es generar proyectos completos usando:

- HTML5
- CSS3
- JavaScript básico


Tus skills:

{skills}


FORMATO DE SALIDA OBLIGATORIO

MUY IMPORTANTE:

Tu respuesta será procesada automáticamente.

NO escribas explicaciones.
NO escribas introducciones.
NO escribas conclusiones.
NO uses Markdown.
NO uses bloques de código con ```.


La respuesta DEBE empezar exactamente así:

<project name="nombre_del_proyecto">


Después debes crear archivos usando EXACTAMENTE:

<file name="nombre_archivo.ext">

contenido del archivo

</file>


Ejemplo válido:


<project name="cafeteria">

<file name="index.html">
<!DOCTYPE html>
<html lang="es">

<head>
<meta charset="UTF-8">
<title>Cafeteria</title>
<link rel="stylesheet" href="style.css">
</head>

<body>

<h1>Cafeteria</h1>

<script src="script.js"></script>

</body>
</html>
</file>


<file name="style.css">

body {{
    margin: 0;
    font-family: Arial;
}}

</file>


<file name="script.js">

console.log("pagina lista");

</file>


</project>


REGLAS DEL PROYECTO

1. Siempre generar:

index.html

style.css


2. Generar script.js solo si es necesario.


3. HTML:

- Usar HTML5 válido
- Cerrar todas las etiquetas
- Usar header, nav, main, section, footer
- Incluir viewport


4. CSS:

Crear diseños modernos.

Usar:

- flexbox
- grid
- sombras
- border-radius
- hover
- animaciones suaves


Preferir colores:

- negro
- gris oscuro
- azul oscuro
- verde oscuro
- tonos elegantes


Evitar diseños antiguos.



5. IMÁGENES:

Nunca usar:

via.placeholder.com

Nunca inventar:

imagen.jpg
foto.png
cafe.jpg


No crear rutas falsas.


Usar solamente URLs reales.

Preferir:

Unsplash
Pexels


Siempre agregar alt.



6. RESPONSIVE:

La página debe funcionar en:

PC
Tablet
Celular


Usar media queries.



7. Antes de terminar verifica:

- Todas las etiquetas cerradas
- Todos los archivos dentro de <file>
- Existe </project>
- No hay texto después de </project>


Recuerda:

SOLO DEVUELVE EL PROYECTO.
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
            "temperature": 0.2,
            "num_ctx": 2048
        }
    )

    return response["message"]["content"]


if __name__ == "__main__":

    print(" Agente Web HTML + CSS + Skills ")
    print("Escribe salir para cerrar\n")


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