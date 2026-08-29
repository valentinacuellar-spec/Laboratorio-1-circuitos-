# Laboratorio 1 - Puente de Wheatstone en CA

Repositorio correspondiente al Laboratorio N.º 1 de Circuitos Electrónicos II.

## Contenido

- `lab1_validation.py`: procesamiento automático del CSV y comparación teórico-experimental.
- `DEFAULT1.csv`: archivo exportado del osciloscopio. Debe colocarse en la misma carpeta que el script.
- `grafica_datos_originales.png`: se genera automáticamente al ejecutar el programa.
- `grafica_normalizada.png`: se genera automáticamente al ejecutar el programa.

## Parámetros utilizados

- Frecuencia: 10 kHz
- Temperatura aproximada: 25 °C
- NTC: 10 kΩ, β = 3950 K
- R1 = R2 = R3 = 10 kΩ
- Rcable ≈ 10 Ω, obtenida con 20 Ω || 20 Ω
- L = 14.7 µH
- C = 4.7 nF

## Ejecución

Instalar dependencias:

```bash
pip install numpy matplotlib
```

Luego ejecutar:

```bash
python lab1_validation.py
```

El script importa el CSV, calcula los valores experimentales, normaliza CH1 y CH2 para comparar forma y fase, calcula el modelo teórico y genera dos gráficas.

## Nota experimental

El CSV disponible presenta una inconsistencia de amplitud en CH2. Por ese motivo, los datos originales se conservan sin correcciones arbitrarias y la normalización se utiliza únicamente para comparación cualitativa de forma y desfase.
