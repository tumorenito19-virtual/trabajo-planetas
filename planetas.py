import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.animation import FuncAnimation

# Constante gravitacional
G = 6.67430e-11  

class CuerpoCeleste:
    def __init__(self, nombre, masa, semieje_mayor, excentricidad, periodo_orbital, color, radio=5e9):
        self.nombre = nombre
        self.masa = masa
        self.semieje_mayor = semieje_mayor
        self.excentricidad = excentricidad
        self.color = color
        self.radio = radio
        self.periodo_orbital = periodo_orbital  
        self.velocidad_angular = 2 * np.pi / periodo_orbital  
        self.angulo_orbita = 0  
        self.circulo = plt.Circle((semieje_mayor, 0), self.radio, color=self.color)
        self.texto_distancia = None  
        self.texto_fuerza = None  

    def actualizar_posicion(self, dt):
        
        self.angulo_orbita += self.velocidad_angular * dt
        r = self.semieje_mayor * (1 - self.excentricidad**2)/(1 + self.excentricidad * np.cos(self.angulo_orbita))
        x = r*np.cos(self.angulo_orbita)
        y = r*np.sin(self.angulo_orbita)
        self.circulo.set_center((x, y))
        return x, y, r

    def calcular_fuerza_gravitatoria(self, x_sol, y_sol):
       
        x_planeta, y_planeta = self.circulo.center
        dx = x_sol - x_planeta
        dy = y_sol - y_planeta
        distancia = np.sqrt(dx**2 + dy**2)
        fuerza = G * self.masa * 1.989e30 / distancia**2  
        return fuerza, distancia

class SistemaSolar:
    def __init__(self):
        
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-5e11, 5e11)
        self.ax.set_ylim(-5e11, 5e11)
        self.ax.axis('off')

        self.sol = CuerpoCeleste('Sol', 1.989e30, 0, 0, 1, 'yellow', radio=10e9)
        self.ax.add_artist(self.sol.circulo)

       
        self.planetas = [
            CuerpoCeleste('Mercurio', 3.285e23, 57.9e9, 0.205, 7.6e6, 'gray'),        
            CuerpoCeleste('Venus', 4.867e24, 108.2e9, 0.007, 1.94e7, 'orange'),       
            CuerpoCeleste('Tierra', 5.972e24, 149.6e9, 0.017, 3.15e7, 'blue'),       
            CuerpoCeleste('Marte', 6.39e23, 227.9e9, 0.093, 5.94e7, 'red'),          
            CuerpoCeleste('Júpiter', 1.898e27, 778.5e9, 0.049, 3.74e8, 'brown'),     
            CuerpoCeleste('Saturno', 5.683e26, 1.433e12, 0.056, 9.29e8, 'gold')      
        ]

        
        for planeta in self.planetas:
            orbita = Ellipse(
                (0, 0), 
                2 * planeta.semieje_mayor,  
                2 * planeta.semieje_mayor * np.sqrt(1 - planeta.excentricidad**2),  
                edgecolor=planeta.color, fill=False, linestyle='--'
            )
            
            orbita.set_center((-planeta.semieje_mayor * planeta.excentricidad, 0))
            self.ax.add_artist(orbita)
            self.ax.add_artist(planeta.circulo)
            planeta.texto_distancia = self.ax.text(0, 0, '', color=planeta.color, ha='center')
            planeta.texto_fuerza = self.ax.text(0, 0, '', color=planeta.color, ha='center')

    def actualizar(self, frame):
        for planeta in self.planetas:
            x, y, distancia_al_sol = planeta.actualizar_posicion(100000)  
            planeta.texto_distancia.set_position((x, y + 1.5e10))
            planeta.texto_distancia.set_text(f"{planeta.nombre}: {distancia_al_sol:.2e} m")
            fuerza, _ = planeta.calcular_fuerza_gravitatoria(*self.sol.circulo.center)
            planeta.texto_fuerza.set_position((x, y - 1.5e10))
            planeta.texto_fuerza.set_text(f"F: {fuerza:.2e} N")

        return [planeta.circulo for planeta in self.planetas] + \
               [planeta.texto_distancia for planeta in self.planetas] + \
               [planeta.texto_fuerza for planeta in self.planetas]

    def iniciar_animacion(self):
        self.ani = FuncAnimation(self.fig, self.actualizar, frames=360, interval=50, blit=True)
        plt.show()

sistema_solar = SistemaSolar()
sistema_solar.iniciar_animacion()
