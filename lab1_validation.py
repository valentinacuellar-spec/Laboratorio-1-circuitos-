import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURACION
# ============================================================

archivo = "DEFAULT1.csv"

T_celsius = 25.0
f = 10000.0
fs = 50e6

R1 = 10000.0
R2 = 10000.0
R3 = 10000.0

R_a = 20.0
R_b = 20.0
R_cable = (R_a * R_b) / (R_a + R_b)

L = 14.7e-6
C = 4.7e-9

R0 = 10000.0
Beta = 3950.0
T0 = 25.0 + 273.15

# ============================================================
# LECTURA DEL CSV
# ============================================================

datos = np.loadtxt(
    archivo,
    delimiter=",",
    skiprows=6
)

VA = datos[:, 0] / 1000.0
VB = datos[:, 1] / 1000.0

t = np.arange(len(VA)) / fs

# ============================================================
# DATOS EXPERIMENTALES
# ============================================================

Vout_exp = VA - VB

VA_pp = np.ptp(VA)
VB_pp = np.ptp(VB)

Vout_pp_exp = np.ptp(Vout_exp)
Vout_pico_exp = Vout_pp_exp / 2.0

Vin_pp_estimado = 2.0 * VA_pp
Vin_pico_estimado = Vin_pp_estimado / 2.0

# ============================================================
# NORMALIZACION PARA COMPARAR FORMA Y FASE
# ============================================================

VA_centrada = VA - np.mean(VA)
VB_centrada = VB - np.mean(VB)

VA_norm = VA_centrada / np.max(np.abs(VA_centrada))
VB_norm = VB_centrada / np.max(np.abs(VB_centrada))

# ============================================================
# DESFASE ENTRE CH1 Y CH2 POR CORRELACION CRUZADA
# ============================================================

corr = np.correlate(VA_norm, VB_norm, mode="full")
lag = np.argmax(corr) - (len(VA_norm) - 1)

delta_t_AB = lag / fs
fase_AB = delta_t_AB * f * 360.0
fase_AB = (fase_AB + 180) % 360 - 180

# ============================================================
# MODELO TEORICO
# ============================================================

T_kelvin = T_celsius + 273.15

R_ntc = R0 * np.exp(
    Beta * (1.0 / T_kelvin - 1.0 / T0)
)

omega = 2 * np.pi * f

Zc = 1.0 / (1j * omega * C)
Zpar = (R_ntc * Zc) / (R_ntc + Zc)
ZL = 1j * omega * L
Zsensor = R_cable + ZL + Zpar

# Convencion experimental del osciloscopio:
# Vout = VA - VB = CH1 - CH2
relacion_Vout = 0.5 - Zsensor / (R3 + Zsensor)

Vout_teorico = Vin_pico_estimado * relacion_Vout
Vout_pico_teorico = np.abs(Vout_teorico)
Vout_pp_teorico = 2 * Vout_pico_teorico
fase_teorica = np.angle(Vout_teorico, deg=True)

VB_teorico = Vin_pico_estimado * Zsensor / (R3 + Zsensor)
VB_pico_teorico = np.abs(VB_teorico)
VB_pp_teorico = 2 * VB_pico_teorico

error_amplitud = (
    abs(Vout_pico_exp - Vout_pico_teorico)
    / Vout_pico_teorico
    * 100
)

# ============================================================
# RESULTADOS
# ============================================================

print("==============================================")
print("      DATOS EXPERIMENTALES DEL CSV")
print("==============================================")
print(f"CH1 / VA Vpp:              {VA_pp:.4f} V")
print(f"CH2 / VB Vpp:              {VB_pp:.4f} V")
print(f"Vin estimado Vpp:          {Vin_pp_estimado:.4f} V")
print()
print(f"Vout experimental Vpp:     {Vout_pp_exp:.4f} V")
print(f"Vout experimental pico:    {Vout_pico_exp:.4f} V")
print()
print(f"Desfase CH1-CH2:            {fase_AB:.2f} grados")
print(f"Delta t CH1-CH2:           {delta_t_AB*1e6:.3f} us")
print()

print("==============================================")
print("           MODELO TEORICO")
print("==============================================")
print(f"Temperatura:                {T_celsius:.1f} °C")
print(f"R_NTC:                      {R_ntc:.2f} ohm")
print(f"R_cable equivalente:        {R_cable:.2f} ohm")
print(f"L:                          {L*1e6:.2f} uH")
print(f"C:                          {C*1e9:.2f} nF")
print()
print(f"Zsensor rectangular:        {Zsensor.real:.2f} {Zsensor.imag:+.2f}j ohm")
print(f"|Zsensor|:                  {abs(Zsensor):.2f} ohm")
print(f"Fase Zsensor:               {np.angle(Zsensor, deg=True):.2f} grados")
print()
print(f"VB teorico Vpp:             {VB_pp_teorico:.4f} V")
print(f"Vout teorico pico:          {Vout_pico_teorico:.4f} V")
print(f"Vout teorico Vpp:           {Vout_pp_teorico:.4f} V")
print(f"Fase teorica Vout:          {fase_teorica:.2f} grados")
print()

print("==============================================")
print("              COMPARACION")
print("==============================================")
print(f"Vout pico experimental:     {Vout_pico_exp:.4f} V")
print(f"Vout pico teorico:          {Vout_pico_teorico:.4f} V")
print(f"Error de amplitud bruto:    {error_amplitud:.2f} %")
print()
print("NOTA:")
print("La normalizacion solo se utiliza para comparar forma y fase.")
print("Los datos originales del CSV no son modificados.")

# ============================================================
# GRAFICA 1: DATOS ORIGINALES
# ============================================================

plt.figure(figsize=(12, 5))
plt.plot(t * 1e6, VA, label="CH1 = Nodo A")
plt.plot(t * 1e6, VB, label="CH2 = Nodo B")
plt.plot(t * 1e6, Vout_exp, label="Vout experimental = VA - VB")
plt.xlabel("Tiempo (us)")
plt.ylabel("Voltaje (V)")
plt.title("Datos experimentales originales")
plt.grid()
plt.legend()
plt.xlim(0, 500)
plt.tight_layout()
plt.savefig("grafica_datos_originales.png", dpi=200)
plt.show()

# ============================================================
# GRAFICA 2: CH1 Y CH2 NORMALIZADOS
# ============================================================

plt.figure(figsize=(12, 5))
plt.plot(t * 1e6, VA_norm, label="CH1 normalizado")
plt.plot(t * 1e6, VB_norm, label="CH2 normalizado")
plt.xlabel("Tiempo (us)")
plt.ylabel("Amplitud normalizada")
plt.title("Comparacion de forma y fase CH1 vs CH2")
plt.grid()
plt.legend()
plt.xlim(0, 500)
plt.tight_layout()
plt.savefig("grafica_normalizada.png", dpi=200)
plt.show()
