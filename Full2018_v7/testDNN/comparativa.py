'''
Código empleado en la obtención de la figura 4.20
Permite calcular la ROC considerando una única variable y compararla con la obtenida a través del entrenamiento multivariante del método Pykeras
'''
import os
import ROOT


ROOT.gROOT.SetBatch(True)

# Rutas de entrada y salida 
eos_input = "root://eosuser.cern.ch//eos/user/d/drasilla/Entrenamientos_red/archivos_ROOT/TMVA_mth_puppimet_eqnum.root"
eos_output = "root://eosuser.cern.ch//eos/user/d/drasilla/Entrenamientos_red/archivos_ROOT/comparacion_ROCs_pares_Puppi>
local_file = "comparacion_ROCs_pares_PuppiMET.png"

# 1. Abrir archivo y extraer datos 
f_in = ROOT.TFile.Open(eos_input)
df = ROOT.RDataFrame("dataset_mth_puppimet_eqnum/TestTree", eos_input)

df_sig = df.Filter("classID == 0")
df_bkg = df.Filter("classID == 1")

vec_met_sig = df_sig.Take[ROOT.Float_t]("PuppiMET_pt")
vec_w_sig   = df_sig.Take[ROOT.Float_t]("weight")
vec_met_bkg = df_bkg.Take[ROOT.Float_t]("PuppiMET_pt")
vec_w_bkg   = df_bkg.Take[ROOT.Float_t]("weight")

# 2. Calcular la ROC de la variable (TGraph)
roc_puppimet = ROOT.TMVA.ROCCurve(vec_met_sig, vec_met_bkg, vec_w_sig, vec_w_bkg)
graph_puppimet = roc_puppimet.GetROCCurve()
graph_puppimet.SetLineColor(ROOT.kRed)
graph_puppimet.SetLineWidth(2)


# 3. Crear el Canvas
canvas = ROOT.TCanvas("canvas", "Comparación de ROCs", 800, 600)
canvas.SetGrid()


# 4. Extraer y dibujar la ROC de PyKeras 
obj_keras = f_in.Get("dataset_mth_puppimet_eqnum/Method_PyKeras/PyKeras/MVA_PyKeras_rejBvsS")

obj_keras.Draw("HIST L")

# Estilos
ROOT.gROOT.ProcessLine("auto h = (TH1D*)gPad->GetPrimitive(\"MVA_PyKeras_rejBvsS\");")
ROOT.gROOT.ProcessLine("h->SetLineColor(kBlue);")
ROOT.gROOT.ProcessLine("h->SetLineWidth(2);")
ROOT.gROOT.ProcessLine("h->GetXaxis()->SetTitle(\"Signal Efficiency\");")
ROOT.gROOT.ProcessLine("h->GetYaxis()->SetTitle(\"Background Rejection\");")
ROOT.gROOT.ProcessLine("h->SetTitle(\"\");")

# 5. Se incluye la ROC de la variable
graph_puppimet.Draw("L SAME")

# Actualizamos el lienzo para asegurar que aplique todos los cambios de C++
canvas.Update()

# 6. Leyenda 
legend = ROOT.TLegend(0.15, 0.15, 0.55, 0.45)
legend.SetTextSize(0.035)                      
legend.SetBorderSize(0)  
legend.SetFillStyle(0)
legend.AddEntry(graph_puppimet, f"Solo PuppiMET_pt (AUC: {roc_puppimet.GetROCIntegral():.3f})", "l")
legend.AddEntry(obj_keras, "Red Neuronal PyKeras 2 var. (AUC: 0.707)", "l")
legend.Draw()

# 8. Guardado
canvas.SaveAs(local_file)
os.system(f"xrdcp -f {local_file} {eos_output}")

if os.path.exists(local_file):
    os.remove(local_file)

f_in.Close()
os._exit(0)
