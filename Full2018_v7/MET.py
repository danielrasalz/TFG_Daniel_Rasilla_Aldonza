"""
Código empleado para la obtención de la figura 4.4 (izquierda). En él se obtiene el momento transversal faltante de los neutrinos procedentes 
del fondo dominante top dileptónico y se compara con el de los procedentes de la muestra de señal ttH, para la que se pide la consición de que 
el par de tops decaiga de forma dileptónica y el Higgs a través del canal invisible.
"""

import ROOT as r
import os

r.gROOT.SetBatch(True)


# 1. Configuración de rutas
chain_tth = r.TChain("Events")
ruta_tth = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/nanoLatino_ttHToNonbb_M125__part*.root"
chain_tth.Add(ruta_tth)

chain_ttbar = r.TChain("Events")
ruta_ttbar = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__>
chain_ttbar.Add(ruta_ttbar) # Nota: Asegúrate de añadir la ruta correcta a chain_ttbar si la tienes separada


# 2. Inicialización de histogramas (15 GeV por bin)
texto_eje_x = "p_{T}^{miss} [GeV]"
texto_eje_y = "Densidad de eventos / 15 GeV"

n_bins = 20
x_min = 0
x_max = 300

h_met_tth_combinado = r.TH1D("h_met_tth_combinado", f";{texto_eje_x};{texto_eje_y}", n_bins, x_min, x_max)
h_met_ttbar_puro    = r.TH1D("h_met_ttbar_puro",    f";{texto_eje_x};{texto_eje_y}", n_bins, x_min, x_max)


# 3. Procesamiento de la muestra ttH (Exclusivo: H->ZZ->4nu + tt->dilep)
print(f"Analizando {chain_tth.GetEntries()} eventos de la muestra ttH...")
eventos_seleccionados_tth = 0

for i, event in enumerate(chain_tth):
    if i % 20000 == 0:
        print(f"  > ttH: Procesando evento {i}...")

    nGen = len(event.GenPart_pdgId)
    nu_zz_indices = []
    nu_top_indices = []

    for j in range(nGen):
        if not (bool(event.GenPart_statusFlags[j] & (1 << 13))):
            continue

        if abs(event.GenPart_pdgId[j]) in [12, 14, 16]:
            current_mother_idx = event.GenPart_genPartIdxMother[j]
            viene_de_higgs = False
            pasa_por_Z = False
            viene_de_top = False

            visited = set()
            for _ in range(15):
                if current_mother_idx < 0 or current_mother_idx >= nGen or current_mother_idx in visited:
                    break
                visited.add(current_mother_idx)

                ancestro_pdg = abs(event.GenPart_pdgId[current_mother_idx])
                if ancestro_pdg == 23:
                    pasa_por_Z = True
                elif ancestro_pdg == 25:
                    viene_de_higgs = True
                elif ancestro_pdg == 6:
                    viene_de_top = True

                current_mother_idx = event.GenPart_genPartIdxMother[current_mother_idx]

            if viene_de_higgs and pasa_por_Z:
                nu_zz_indices.append(j)
            elif viene_de_top:
                nu_top_indices.append(j)

    # REQUISITOS: 4 neutrinos del Higgs + 2 neutrinos de los tops (dileptónico)
    es_canal_higgs_4nu = (len(nu_zz_indices) == 4)
    es_top_dileptonico = (len(nu_top_indices) == 2)

    if es_canal_higgs_4nu and es_top_dileptonico:
        eventos_seleccionados_tth += 1
        # Suma vectorial combinada de TODOS los neutrinos del evento (4 del Higgs + 2 del top)
        indices_totales_tth = nu_zz_indices + nu_top_indices
        sum_px = sum(event.GenPart_pt[idx] * r.TMath.Cos(event.GenPart_phi[idx]) for idx in indices_totales_tth)
        sum_py = sum(event.GenPart_pt[idx] * r.TMath.Sin(event.GenPart_phi[idx]) for idx in indices_totales_tth)
        h_met_tth_combinado.Fill(r.TMath.Sqrt(sum_px**2 + sum_py**2))

print(f"[INFO] Eventos ttH que cumplen la topología exclusiva: {eventos_seleccionados_tth}")


# 4. Procesamiento limitado de la muestra TTTo2L2Nu 
max_eventos_ttbar = 1000000
print(f"\nAnalizando un subconjunto de {max_eventos_ttbar} eventos de la muestra TTTo2L2Nu...")

for i, event in enumerate(chain_ttbar):
    if i >= max_eventos_ttbar:
        print(f"  > [INFO] Alcanzado el límite de {max_eventos_ttbar} eventos. Deteniendo lectura.")
        break

    if i % 100000 == 0:
        print(f"  > TTbar: Procesando evento {i}...")

    nGen = len(event.GenPart_pdgId)
    nu_ttbar_indices = []

    for j in range(nGen):
        if not (bool(event.GenPart_statusFlags[j] & (1 << 13))):
            continue
        if abs(event.GenPart_pdgId[j]) in [12, 14, 16]:
            nu_ttbar_indices.append(j)

    if nu_ttbar_indices:
        sum_px = sum(event.GenPart_pt[idx] * r.TMath.Cos(event.GenPart_phi[idx]) for idx in nu_ttbar_indices)
        sum_py = sum(event.GenPart_pt[idx] * r.TMath.Sin(event.GenPart_phi[idx]) for idx in nu_ttbar_indices)
        h_met_ttbar_puro.Fill(r.TMath.Sqrt(sum_px**2 + sum_py**2))


# 5. Normalización de las curvas 
if h_met_tth_combinado.Integral() > 0:
    h_met_tth_combinado.Scale(1.0 / h_met_tth_combinado.Integral())
if h_met_ttbar_puro.Integral() > 0:
    h_met_ttbar_puro.Scale(1.0 / h_met_ttbar_puro.Integral())

# 6. Dibujo
ruta_eos = "/eos/user/d/drasilla/MET"
if not os.path.exists(ruta_eos):
    ruta_eos = "./"
os.makedirs(ruta_eos, exist_ok=True)

canvas = r.TCanvas("canvas_cross_samples", "Comparacion Inter-Muestras Normalizada", 800, 600)
canvas.SetLeftMargin(0.15)

h_met_tth_combinado.SetLineColor(r.kBlack)
h_met_tth_combinado.SetLineWidth(3)
h_met_ttbar_puro.SetLineColor(r.kBlue+2)
h_met_ttbar_puro.SetLineWidth(3)

h_met_tth_combinado.SetStats(0)
h_met_ttbar_puro.SetStats(0)

h_met_tth_combinado.GetYaxis().SetTitleOffset(1.4)
h_met_ttbar_puro.GetYaxis().SetTitleOffset(1.4)

max_global = max(h_met_tth_combinado.GetMaximum(), h_met_ttbar_puro.GetMaximum())
h_met_tth_combinado.SetMaximum(max_global * 1.25)

h_met_tth_combinado.Draw("HIST")
h_met_ttbar_puro.Draw("HIST SAME")

leyenda = r.TLegend(0.35, 0.68, 0.88, 0.88)
leyenda.AddEntry(h_met_tth_combinado, "p_{T}^{miss} (#nu_{4#nu} + #nu_{dilep}) [ttH]", "l")
leyenda.AddEntry(h_met_ttbar_puro,    "p_{T}^{miss} (#nu_{top}) [TTTo2L2Nu]", "l")
leyenda.SetBorderSize(0)
leyenda.SetTextSize(0.032)
leyenda.Draw()

canvas.SaveAs(os.path.join(ruta_eos, "comparacion_ptmiss_tth_vs_ttbar_NORMALIZADO.png"))
canvas.SaveAs(os.path.join(ruta_eos, "comparacion_ptmiss_tth_vs_ttbar_NORMALIZADO.pdf"))

f_out = r.TFile(os.path.join(ruta_eos, "analisis_intermuestras_normalizado.root"), "RECREATE")
h_met_tth_combinado.Write()
h_met_ttbar_puro.Write()
f_out.Close()

print(f"Gráfico completado y guardado en: {ruta_eos}")
