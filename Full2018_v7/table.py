'''
Código empleado para obtener la tabla 4.4 de comparación de la FOM para las distintas señales (al final se decidió no mostrar 
las filas correspondientes a la señal "ttH_ZZ")
'''

import ROOT as r
import math


tag = 'Full2018_v7'
fileName = f"histogramas_finales/mkShapes__histogramas_finales.root"
file = r.TFile.Open(fileName)

# pasos definidos en cuts_estudio.py
pasos = ["step0_skim", "ch_3lep", "pt_cuts", "mll>20", "mpmet>20", "PuppiMET_pt>20", "ZVeto", "1bj_emu", "emu_tDM", "emu_ttDM", "emu_tttDM"]

# fondos
muestras_fondo = ["DY", "ttbar", "tt_semileptonic", "SingleTop", "ttV", "VZ", "WW", "Other"]

# señales
muestras_señal = [
    "ttH_nonbb",    # Señal total
    "ttH_ZZ4nu",    # H->ZZ->4ν (invisible)
    "ttH_ZZ",       # Todos los H->ZZ
]

print("\n" + "=" * 120)
print(f"{'CORTE':22} | {'SEÑAL':20} | {'S':12} | {'B':12} | {'S+B':12} | {'FOM':12}")
print("=" * 120)

for paso in pasos:
    for s_name in muestras_señal:
        S = 0.0
        B = 0.0

        # 1. Suma de la señal
        path = f"{paso}/events/histo_{s_name}"
        h = file.Get(path)
        if h:
            S += h.Integral()
        else:
            print(f"No se encontró {path}")
            continue

        # 2. Suma de los fondos
        for b_name in muestras_fondo:
            path = f"{paso}/events/histo_{b_name}"
            h = file.Get(path)
            if h:
                B += h.Integral()

        # 3. Cálculo FoM
        S_plus_B = S + B
        fom = S / math.sqrt(S_plus_B) if S_plus_B > 0 else 0

        # 4. Contrucción de las filas
        print(f"{paso:22} | {s_name:20} | {S:12.2f} | {B:12.2f} | {S_plus_B:12.2f} | {fom:12.3g}")

    print("-" * 120)

file.Close()
