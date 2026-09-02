'''
Aquí se muestra el código empleado para la obtención de la figura 4.19. En él, se realiza un muestreo de todos los puntos pertenecientes a una curva ROC dada
y se obtienen los puntos de trabajo óptimos atendiendo a los criterios explicados en la memoria. Así mismo, se obtiene la curva de la 
figura de mérito respecto al valor de la eficiencia de señal y se trasladan los tres puntos obtenidos anteriormente a esta gráfica.
'''
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Rutas
cernbox_dir = "/eos/user/d/drasilla/Entrenamientos_red/archivos_ROOT"
root_file_path = os.path.join(cernbox_dir, "TMVA_mth_puppimet_eqnum.root")
output_img_roc = os.path.join(cernbox_dir, "aroc_tres_puntos_optimos.png")
output_img_fom = os.path.join(cernbox_dir, "afom_vs_eficiencia_con_tres_puntos.png")

print(f"Leyendo el archivo ROOT desde: {root_file_path}")

root_file = ROOT.TFile.Open(root_file_path, "READ")
if not root_file or root_file.IsZombie():
    raise FileNotFoundError(f"No se pudo abrir el archivo ROOT en: {root_file_path}")

# 2. Extraer objetos de TMVA
roc_hist = root_file.Get("dataset_mth_puppimet_eqnum/Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")
h_sig = root_file.Get("dataset_mth_puppimet_eqnum/Method_PyKeras/PyKeras/MVA_PyKeras_S")

if not roc_hist or not h_sig:
    raise ValueError("No se pudieron encontrar los objetos necesarios de TMVA en el archivo ROOT.")

# Yields totales esperados (los factores por los que se multiplica corresponden a los pesos otorgados a los eventos de señal y de fondo por el entorno mkShapes)
S_total = 335*0.0017
B_total = 7673200*0.075



# PARTE A: Obtención de los puntos de corte en la ROC (Gráfica izquierda)
sig_effs_roc = []
bkg_rej_roc = []

for i in range(1, roc_hist.GetNbinsX() + 1):
    eff = roc_hist.GetBinCenter(i)
    rej = roc_hist.GetBinContent(i)
    if 0.0 <= eff <= 1.0:
        sig_effs_roc.append(eff)
        bkg_rej_roc.append(rej)

sig_effs_roc = np.array(sig_effs_roc)
bkg_rej_roc = np.array(bkg_rej_roc)

# Índices de los 3 puntos óptimos en la ROC
# Criterio Euclidiano
idx_euclid = np.argmin(np.sqrt((1.0 - sig_effs_roc)**2 + (1.0 - bkg_rej_roc)**2))

# Índice Youden
idx_youden = np.argmax(sig_effs_roc + bkg_rej_roc)

# Maximizar FoM
fom_roc_values = []
for eff, rej in zip(sig_effs_roc, bkg_rej_roc):
    S = eff * S_total
    B = (1.0 - rej) * B_total
    fom = S / np.sqrt(S + B) if (S + B) > 0 else 0.0
    fom_roc_values.append(fom)
fom_roc_values = np.array(fom_roc_values)
idx_fom_roc = np.argmax(fom_roc_values)

# Valor máximo absoluto de la FoM
max_fom_val = np.max(fom_roc_values)

print(f"  > Máxima FoM alcanzada: {max_fom_val:.6f}")


# GENERAR GRÁFICA 1: Curva ROC con los tres puntos
plt.figure(figsize=(9, 7), constrained_layout=True)
plt.plot(sig_effs_roc, bkg_rej_roc, label='PyKeras (AUC: 0.707)', color='#1f77b4', linewidth=2.5)

plt.scatter(sig_effs_roc[idx_euclid], bkg_rej_roc[idx_euclid], color='green', s=150, zorder=8,
            marker='o', edgecolors='black', linewidths=1.0,
            label=f'1. Euclidiano\nSig: {sig_effs_roc[idx_euclid]*100:.1f}%, Rej: {bkg_rej_roc[idx_euclid]*100:.1f}%')

plt.scatter(sig_effs_roc[idx_youden], bkg_rej_roc[idx_youden], color='darkorange', s=150, zorder=7,
            marker='o', edgecolors='black', linewidths=1.0,
            label=f'2. Youden\nSig: {sig_effs_roc[idx_youden]*100:.1f}%, Rej: {bkg_rej_roc[idx_youden]*100:.1f}%')

plt.scatter(sig_effs_roc[idx_fom_roc], bkg_rej_roc[idx_fom_roc], color='red', s=180, zorder=9,
            marker='o', edgecolors='black', linewidths=1.0,
            label=f'3. FOM\nSig: {sig_effs_roc[idx_fom_roc]*100:.1f}%, Rej: {bkg_rej_roc[idx_fom_roc]*100:.1f}%')

plt.xlabel(r'Signal Efficiency', fontsize=12, loc='right')
plt.ylabel(r'Background Rejection', fontsize=12, loc='top')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower left', fontsize=10, frameon=True)
plt.xlim(-0.02, 1.02)
plt.ylim(-0.02, 1.02)

plt.savefig(output_img_roc, dpi=300, bbox_inches='tight')
plt.close()



# GENERAR GRÁFICA 2: FoM frente a eficiencia de señal

plt.figure(figsize=(9, 7), constrained_layout=True)l
plt.plot(sig_effs_roc, fom_roc_values, color='#1f77b4', linewidth=2.5, label=r'FOM ($S/\sqrt{S+B}$)')

# Proyectar el punto Euclidiano
plt.scatter(sig_effs_roc[idx_euclid], fom_roc_values[idx_euclid], color='green', s=150, zorder=8, marker='o',
            edgecolors='black', linewidths=1.0,
            label=f'1. Euclidiano (Ef. Sig: {sig_effs_roc[idx_euclid]*100:.1f}%)')

# Proyectar el punto Youden
plt.scatter(sig_effs_roc[idx_youden], fom_roc_values[idx_youden], color='darkorange', s=150, zorder=7, marker='o',
            edgecolors='black', linewidths=1.0,
            label=f'2. Youden (Ef. Sig: {sig_effs_roc[idx_youden]*100:.1f}%)')

# Proyectar el punto FOM Óptimo 
plt.scatter(sig_effs_roc[idx_fom_roc], fom_roc_values[idx_fom_roc], color='red', s=180, zorder=9, marker='o',
            edgecolors='black', linewidths=1.0,
            label=f'3. FOM Óptimo (Ef. Sig: {sig_effs_roc[idx_fom_roc]*100:.1f}%)')

# Línea vertical marcando dónde cae la eficiencia óptima
plt.axvline(x=sig_effs_roc[idx_fom_roc], color='gray', linestyle='--', alpha=0.7)

plt.xlabel(r'Signal Efficiency', fontsize=12, loc='right')
plt.ylabel(r'FoM ($S/\sqrt{S+B}$)', fontsize=12, loc='top')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower right', fontsize=10, frameon=True)
plt.xlim(-0.02, 1.02)

y_min = np.min(fom_roc_values) * 0.95
y_max = np.max(fom_roc_values) * 1.08
plt.ylim(y_min, y_max)

plt.savefig(output_img_fom, dpi=300, bbox_inches='tight')
plt.close()

root_file.Close()
print("Gráficas creadas")
