from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


perplexity_api_key = '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'
perplexity_base_url = 'https://api.perplexity.ai/chat/completions'


messages = [
    {"role": "system", "content": "actua como un supervisor de call center n1 para soporte de internet en donde tus ejectivos te haran preguntas de posibles casos que no se puede resolver facilmente. dame un respuesta corta maximo de 3 lineas"}
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data1 = request.json
        user_input = data1.get("user")
        if not user_input:
            return jsonify({"error": "Campo 'user' no encontrado o vacío"}), 400
        
        messages.append({"role": "user", "content": user_input})
        
      
        headers = {
            'Authorization': f'Bearer {perplexity_api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": messages
        }

        try:
            response = requests.post(perplexity_base_url, headers=headers, json=data)
            response.raise_for_status() 
            response_data = response.json()

           
            if 'choices' in response_data:
                assistant_message = response_data['choices'][0]['message']['content']
                messages.append({"role": "assistant", "content": assistant_message})
            else:
                print("La clave 'choices' no está presente en la respuesta.")
               
                assistant_message = "No se encontró la respuesta esperada."

            return jsonify({"messages": messages})
        
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return jsonify({"error": "Error en la solicitud a la API."}), 500
        except Exception as err:
            print(f"Other error occurred: {err}")
            return jsonify({"error": "Error inesperado."}), 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
