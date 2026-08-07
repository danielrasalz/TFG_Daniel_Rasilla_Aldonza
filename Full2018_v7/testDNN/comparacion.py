'''
Código empleado para representar en una misma figura las ROC correspondientes a los métodos de Fisher y Pykeras resultantes de un mismo o de diferentes entrenamientos
(figuras 4.12, 4.13, 4.14, 4.16 (abajo) y 4.18)
'''
import ROOT

# Rutas 
output_path = "/eos/user/d/drasilla/"
input_path  = "/eos/user/d/drasilla/Entrenamientos_red/archivos_ROOT/"

# 1. Primer archivo
file1 = ROOT.TFile.Open(input_path + "TMVA_ttH_ZZ4nu_Result_5var_4cap.root")
dataset1 = file1.Get("dataset_ZZ4nu_5var_4cap")

roc_pykeras_4cap = dataset1.Get("Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")
roc_fisher_4cap  = dataset1.Get("Method_Fisher/Fisher/MVA_Fisher_rejBvsS")

# 2. Segundo archivo
file2 = ROOT.TFile.Open(input_path + "TMVA_ttH_ZZ4nu_Result_5var_4cap_noemu.root")
dataset2 = file2.Get("dataset_ZZ4nu_5var_4cap_noemu")

roc_pykeras_2cap = dataset2.Get("Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")
roc_fisher_2cap  = dataset2.Get("Method_Fisher/Fisher/MVA_Fisher_rejBvsS")


# Crear canvas
canvas = ROOT.TCanvas("roc_comparison", "Comparacion curvas ROC", 800, 600)
canvas.SetGrid()

# Estilos primer archivo
roc_pykeras_4cap.SetLineColor(ROOT.kBlue)
roc_pykeras_4cap.SetLineWidth(2)
roc_pykeras_4cap.SetTitle(";Signal Efficiency;Background Rejection")

roc_fisher_4cap.SetLineColor(ROOT.kRed)
roc_fisher_4cap.SetLineWidth(2)

# Estilos segundo archivo
roc_pykeras_2cap.SetLineColor(ROOT.kGreen + 2) # Verde oscuro
roc_pykeras_2cap.SetLineWidth(2)

roc_fisher_2cap.SetLineColor(ROOT.kOrange + 7) # Naranja oscuro/Rojizo
roc_fisher_2cap.SetLineWidth(2)


# Dibujar las curvas en la misma gráfica
roc_pykeras_4cap.Draw("C")
roc_fisher_4cap.Draw("C SAME")
roc_pykeras_2cap.Draw("C SAME")
roc_fisher_2cap.Draw("C SAME")


# Leyenda 
legend = ROOT.TLegend(0.15, 0.15, 0.55, 0.45)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
legend.SetTextSize(0.035)
legend.AddEntry(roc_pykeras_4cap, "PyKeras (AUC = 0.683)", "l")
legend.AddEntry(roc_pykeras_2cap, "PyKeras (sin emu) (AUC = 0.697)", "l")
legend.AddEntry(roc_fisher_4cap,  "Fisher (AUC = 0.735)", "l")
legend.AddEntry(roc_fisher_2cap,  "Fisher (sin emu) (AUC = 0.704)", "l")
legend.Draw()

canvas.Update()

canvas.SaveAs(output_path + "ROC_Fisher_vs_PyKeras_Comparativa_2vs4.png")

print(f"Graficas guardadas en {output_path}")

# Cierre de archivos 
file1.Close()
#file2.Close()
