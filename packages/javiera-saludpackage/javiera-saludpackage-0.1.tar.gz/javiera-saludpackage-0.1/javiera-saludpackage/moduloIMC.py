def calcularIMC(p, a):
    return p / (a * a)

def nivelDePeso(IMC):
    if IMC < 18.5:
        return "Peso bajo"
    elif 18.5 <= IMC <= 24.9:
        return "Peso normal"
    elif 25.0 <= IMC <= 29.9:
        return "Sobrepeso"
    elif 30.0 <= IMC <= 39.9:
        return "Obesidad"
    elif IMC >= 40.0:
        return "Obesidad morbida"

