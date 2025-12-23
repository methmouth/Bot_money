class BallPredictor:
    def __init__(self, y_raqueta_norm):
        self.last_x, self.last_y = None, None
        self.y_raqueta = y_raqueta_norm

    def predecir(self, x_actual, y_actual):
        if self.last_x is None:
            self.last_x, self.last_y = x_actual, y_actual
            return x_actual
        vx, vy = x_actual - self.last_x, y_actual - self.last_y
        self.last_x, self.last_y = x_actual, y_actual
        if vy <= 0: return 0.5 # Si sube, ir al centro
        
        pasos = (self.y_raqueta - y_actual) / vy
        x_final = x_actual + (vx * pasos)
        # Rebotes en bordes 0 y 1
        while x_final < 0 or x_final > 1:
            x_final = abs(x_final) if x_final < 0 else 2 - x_final
        return x_final
