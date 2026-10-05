from flask import Flask, render_template, request

app = Flask(__name__)


# ==============================
# FUNÇÕES DE CONVERSÃO
# ==============================

def celsius_para_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def celsius_para_kelvin(celsius):
    return celsius + 273.15


def fahrenheit_para_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_para_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_para_celsius(kelvin):
    return kelvin - 273.15


def kelvin_para_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32


# ==============================
# PÁGINA PRINCIPAL
# ==============================

@app.route("/", methods=["GET", "POST"])
def index():

    resultado = None
    erro = None
    temperatura = ""
    origem = "celsius"
    destino = "fahrenheit"

    if request.method == "POST":

        temperatura = request.form.get("temperatura", "")
        origem = request.form.get("origem", "")
        destino = request.form.get("destino", "")

        try:
            temperatura_numero = float(temperatura.replace(",", "."))

            # Não permite Kelvin negativo
            if origem == "kelvin" and temperatura_numero < 0:
                erro = "A temperatura em Kelvin não pode ser negativa."

            else:

                conversoes = {
                    ("celsius", "fahrenheit"): celsius_para_fahrenheit,
                    ("celsius", "kelvin"): celsius_para_kelvin,
                    ("fahrenheit", "celsius"): fahrenheit_para_celsius,
                    ("fahrenheit", "kelvin"): fahrenheit_para_kelvin,
                    ("kelvin", "celsius"): kelvin_para_celsius,
                    ("kelvin", "fahrenheit"): kelvin_para_fahrenheit
                }

                if origem == destino:
                    resultado = temperatura_numero

                else:
                    funcao = conversoes.get((origem, destino))

                    if funcao:
                        resultado = funcao(temperatura_numero)
                    else:
                        erro = "Conversão inválida."

        except ValueError:
            erro = "Digite uma temperatura válida."

    return render_template(
        "index.html",
        resultado=resultado,
        erro=erro,
        temperatura=temperatura,
        origem=origem,
        destino=destino
    )


# ==============================
# EXECUTAR O PROGRAMA
# ==============================

if __name__ == "__main__":
    app.run(debug=True)