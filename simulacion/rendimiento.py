"""Simulación del tiempo de respuesta de la búsqueda de libros.

Modelo simplificado de colas: T = S / (1 - rho), con rho = carga / capacidad.
Los parámetros son SUPUESTOS del caso (no mediciones reales); ver informe.
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

TOPE_S = 30.0  # tiempo máximo mostrado (saturación / timeout)

# --- Monolito actual: 1 instancia, búsqueda sin caché ---
# Calibrado con el supuesto: ~3 s a 40 solicitudes/s.
CAPACIDAD_MONOLITO = 60  # solicitudes/s
S_MONOLITO = 1.0  # s, latencia sin carga

# --- Microservicios: Catálogo con 3 réplicas + caché Redis ---
TASA_ACIERTO_CACHE = 0.80
S_CACHE, S_BD = 0.02, 0.40  # s
S_MICRO = TASA_ACIERTO_CACHE * S_CACHE + (1 - TASA_ACIERTO_CACHE) * S_BD
REPLICAS = 3
CAPACIDAD_REPLICA = 150  # solicitudes/s por réplica


def tiempo_respuesta(carga, s_base, capacidad):
    rho = carga / capacidad
    if rho >= 1:
        return TOPE_S
    return min(s_base / (1 - rho), TOPE_S)


def main():
    cargas = np.arange(5, 251, 5)
    mono = [tiempo_respuesta(c, S_MONOLITO, CAPACIDAD_MONOLITO) for c in cargas]
    micro = [tiempo_respuesta(c, S_MICRO, REPLICAS * CAPACIDAD_REPLICA) for c in cargas]

    fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
    ax.plot(cargas, mono, color="#c0392b", lw=2, label="Monolito actual (1 instancia)")
    ax.plot(cargas, micro, color="#2e8b57", lw=2,
            label="Microservicios (Catálogo x3 + caché Redis)")
    ax.axhline(0.5, color="gray", ls="--", lw=1)
    ax.text(3, 0.56, "Objetivo: 500 ms", color="gray", fontsize=8)
    ax.axvline(200, color="#999", ls=":", lw=1)
    ax.text(201, 12, "Pico\nsupuesto", fontsize=8, color="#555")
    ax.set_yscale("log")
    ax.set_xlabel("Carga (solicitudes por segundo)")
    ax.set_ylabel("Tiempo de respuesta (s, escala log)")
    ax.set_title("Tiempo de respuesta de la búsqueda según la carga\n(resultados simulados)",
                 fontsize=11)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="center right")
    fig.tight_layout()
    fig.savefig("docs/grafico_rendimiento.png")

    for c in (40, 100, 200):
        m = tiempo_respuesta(c, S_MONOLITO, CAPACIDAD_MONOLITO)
        u = tiempo_respuesta(c, S_MICRO, REPLICAS * CAPACIDAD_REPLICA)
        print(f"{c:>3} req/s -> monolito {m:5.2f} s | microservicios {u*1000:6.0f} ms")


if __name__ == "__main__":
    main()
