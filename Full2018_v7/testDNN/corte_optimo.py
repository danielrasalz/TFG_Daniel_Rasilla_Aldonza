'''
Aquí se muestra el código empleado para la obtención de la figura 4.19. En él. se realiza un muestreo de todos los puntos pertenecientes a una curva ROC dada
y se obtiene el punto de corte óptimo considerando aquel punto cuya distancia con respecto al eje superior izquierdo sea mínima
'''
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Ruta a la EOS
cernbox_dir = "/eos/user/d/drasilla/Entrenamientos_red/archivos_ROOT"

root_file_path = os.path.join(cernbox_dir, "TMVA_mth_puppimet_eqnum.root")
output_img_path = os.path.join(cernbox_dir, "roc_optimo_pykeras.png")

print(f"Leyendo el archivo ROOT desde: {root_file_path}")

# 2. Abrir el archivo ROOT
root_file = ROOT.TFile.Open(root_file_path, "READ")
if not root_file or root_file.IsZombie():
    raise FileNotFoundError(f"No se pudo abrir el archivo ROOT en: {root_file_path}")

# 3. Buscar el gráfico ROC de PyKeras
roc_hist = root_file.Get("dataset_mth_puppimet_eqnum/Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")

if not roc_hist:
    # Intento alternativo de búsqueda si la estructura cambia
    root_file.ReadAll()
    raise ValueError("No se pudo encontrar el gráfico ROC 'MVA_PyKeras_rejBvsS' en el archivo ROOT.")

# 4. Extraer los puntos de la curva ROC
sig_effs = []
bkg_rej = []

# Recorremos todos los bines del histograma
for i in range(1, roc_hist.GetNbinsX() + 1):
    eff = roc_hist.GetBinCenter(i)  # Eje X: Eficiencia de señal
    rej = roc_hist.GetBinContent(i) # Eje Y: Rechazo de fondo

    if 0.0 <= eff <= 1.0:
        sig_effs.append(eff)
        bkg_rej.append(rej)

sig_effs = np.array(sig_effs)
bkg_rej = np.array(bkg_rej)

# 5. Encontrar el punto óptimo (mínima distancia euclidiana al punto ideal [1.0, 1.0])
distances = np.sqrt((1.0 - sig_effs)**2 + (1.0 - bkg_rej)**2)
distances = np.sqrt((1.0 - sig_effs)**2 + (1.0 - bkg_rej)**2)
optimal_idx = np.argmin(distances)

opt_sig_eff = sig_effs[optimal_idx]
opt_bkg_rej = bkg_rej[optimal_idx]

# Resultados
print("\n" + "="*40)
print("=== PUNTO ÓPTIMO EN LA CURVA ROC (PYKERAS) ===")
print("="*40)
print(f" Eficiencia de Señal (True Positive Rate): {opt_sig_eff * 100:.2f}%")
print(f" Rechazo de Fondo (1 - False Positive Rate): {opt_bkg_rej * 100:.2f}%")
print(f" Eficiencia de Fondo (Falsos Positivos):    {(1.0 - opt_bkg_rej) * 100:.2f}%")
print("="*40 + "\n")

# 6. Dibujar la curva ROC y marcar el punto óptimo
plt.figure(figsize=(9, 7))
plt.plot(sig_effs, bkg_rej, label='Curva ROC PyKeras', color='#1f77b4', linewidth=2.5)
plt.scatter(opt_sig_eff, opt_bkg_rej, color='red', s=120, zorder=5,
            label=f'Punto Óptimo\nSig Eff: {opt_sig_eff*100:.1f}%\nBkg Rej: {opt_bkg_rej*100:.1f}%')

plt.xlabel('Signal Efficiency', fontsize=12, loc='right')
plt.ylabel('Background Rejection', fontsize=12, loc='top')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower left', fontsize=11, frameon=True)
plt.xlim(0, 1.02)
plt.ylim(0, 1.02)

# 7. Guardar la gráfica 
plt.savefig(output_img_path, dpi=300, bbox_inches='tight')
print(f"Gráfica guardada con éxito en: {output_img_path}")

root_file.Close()
plt.close()
