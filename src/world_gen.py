class GeneradorMapas:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.mapa = [[1 for _ in range(ancho)] for _ in range(alto)]

    def generar_nivel_completo(self):
        # Asegúrate de que este método exista AQUÍ ADENTRO
        return self.mapa