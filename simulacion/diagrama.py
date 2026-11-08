"""Genera el diagrama de arquitectura propuesto (docs/diagrama_arquitectura.png)."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


def caja(ax, x, y, w, h, titulo, detalle="", color="#e8f3dc", borde="#5b8c2a"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                                fc=color, ec=borde, lw=1.5))
    ax.text(x + w / 2, y + h * 0.64, titulo, ha="center", va="center",
            fontsize=9.5, fontweight="bold")
    if detalle:
        ax.text(x + w / 2, y + h * 0.28, detalle, ha="center", va="center", fontsize=7.5)


def flecha(ax, p1, p2, estilo="-", texto="", off=(0, 0.18)):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=12,
                                 lw=1.4, ls=estilo, color="#333"))
    if texto:
        ax.text((p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1], texto,
                ha="center", fontsize=7, color="#333")


fig, ax = plt.subplots(figsize=(11, 6.4), dpi=200)
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")
ax.text(8, 9.6, "Arquitectura propuesta: sistema de gestión de bibliotecas",
        ha="center", fontsize=12, fontweight="bold")

# Contenedores
ax.add_patch(Rectangle((7.0, 1.0), 8.7, 8.0, fc="none", ec="#4a6fa5", ls="--", lw=1.5))
ax.text(7.2, 8.7, "Contenedores Docker (escalables por servicio)", fontsize=8, color="#4a6fa5")

caja(ax, 0.3, 4.2, 2.6, 1.6, "Clientes", "Estudiantes y docentes\n(web / móvil)",
     "#f2f2f2", "#777")
caja(ax, 3.8, 3.9, 2.6, 2.2, "API Gateway", "Autenticación (JWT)\nEnrutamiento\nLímite de solicitudes",
     "#fdf1d6", "#c9962b")

caja(ax, 7.4, 7.0, 3.4, 1.4, "Servicio Catálogo", "Búsqueda de libros | x3 réplicas\nBD propia: PostgreSQL")
caja(ax, 7.4, 4.3, 3.4, 1.4, "Servicio Préstamos y Reservas", "Préstamos, reservas, devoluciones\nBD propia: PostgreSQL")
caja(ax, 7.4, 1.6, 3.4, 1.4, "Servicio Usuarios", "Cuentas y estado de habilitación\nBD propia: PostgreSQL")
caja(ax, 11.8, 7.0, 3.4, 1.4, "Redis (caché)", "Resultados de búsqueda\nTTL corto", "#fbe3e3", "#b5453a")
caja(ax, 11.8, 4.3, 3.4, 1.4, "Servicio Multas y Devoluciones", "Política de multas (Strategy)\nBD propia: PostgreSQL")

flecha(ax, (2.9, 5.0), (3.8, 5.0))
for yd in (7.7, 5.0, 2.3):
    flecha(ax, (6.4, 5.0), (7.4, yd))
flecha(ax, (10.8, 7.7), (11.8, 7.7), texto="consulta caché")
flecha(ax, (9.1, 5.7), (9.1, 7.0), "--", "stock", (0.45, 0))
flecha(ax, (9.1, 4.3), (9.1, 3.0), "--", "¿habilitado?", (0.7, 0))
flecha(ax, (10.8, 5.0), (11.8, 5.0), "--", "multa")

ax.text(0.3, 0.5, "Línea continua: solicitud externa | Línea punteada: comunicación interna entre servicios (HTTP)",
        fontsize=7.5, color="#444")
fig.tight_layout()
fig.savefig("docs/diagrama_arquitectura.png")
