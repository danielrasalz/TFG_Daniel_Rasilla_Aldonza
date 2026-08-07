'''
Código usado para la obtención de la figura 4.4 (Derecha)
'''

import ROOT as r
import os


r.gROOT.SetBatch(True)


# 1. CONFIGURACIÓN DE RUTA Y TCHAIN (Muestra ttH)
chain_tth = r.TChain("Events")
ruta_tth = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/nanoLatino_ttHToNonbb_M125__part*.root"
chain_tth.Add(ruta_tth)

# 2. INICIALIZACIÓN DE HISTOGRAMAS 
texto_eje_x = "p_{T}^{miss} [GeV]"
texto_eje_y = "Densidad de eventos / 15 GeV"

n_bins = 20
x_min = 0
x_max = 300

h_met_higgs_zz  = r.TH1D("h_met_higgs_zz",  f";{texto_eje_x};{texto_eje_y}", n_bins, x_min, x_max)
h_met_solo_top   = r.TH1D("h_met_solo_top",   f";{texto_eje_x};{texto_eje_y}", n_bins, x_min, x_max)
h_met_combinado  = r.TH1D("h_met_combinado",  f";{texto_eje_x};{texto_eje_y}", n_bins, x_min, x_max)

# 3. BUCLE DE PROCESAMIENTO
n_entries = chain_tth.GetEntries()
print(f"Analizando {n_entries} eventos de la muestra ttHToNonbb...")

eventos_4nu_y_tt_dileptonico  = 0

for i, event in enumerate(chain_tth):
    if i % 20000 == 0:
        print(f"  > Procesando evento {i}/{n_entries}...")

    nGen = len(event.GenPart_pdgId)

    nu_solo_zz_indices  = []
    nu_solo_top_indices = []

    for j in range(nGen):
        # Filtro IsLastCopy (bit 13) para seleccionar el estado final del neutrino
        if not (bool(event.GenPart_statusFlags[j] & (1 << 13))):
            continue

        if abs(event.GenPart_pdgId[j]) in [12, 14, 16]:
            current_mother_idx = event.GenPart_genPartIdxMother[j]

            pasa_por_Z = False
            viene_de_higgs = False
            viene_de_top = False

            # Rastreo genealógico (máximo 15 generaciones)
            visited = set()
            for _ in range(15):
                if current_mother_idx < 0 or current_mother_idx >= nGen or current_mother_idx in visited:
                    break
                visited.add(current_mother_idx)

                ancestro_pdg = abs(event.GenPart_pdgId[current_mother_idx])

                if ancestro_pdg == 23:      # Bosón Z
                    pasa_por_Z = True
                elif ancestro_pdg == 25:    # Bosón de Higgs
                    viene_de_higgs = True
                elif ancestro_pdg == 6:     # Quark Top
                    viene_de_top = True

                current_mother_idx = event.GenPart_genPartIdxMother[current_mother_idx]

            # Asignación del neutrino según procedencia
            if viene_de_higgs and pasa_por_Z:
                nu_solo_zz_indices.append(j)
            elif viene_de_top:
                nu_solo_top_indices.append(j)

   
    # CÁLCULO VECTORIAL Y FILTRADO POR CANAL PURO H -> ZZ -> 4nu

    # Se exigen 4 neutrinos provenientes de Z(H) para aislar H -> ZZ -> 4nu y 2 provenientes de los top
    es_canal_4nu = (len(nu_solo_zz_indices) == 4)
    es_top_dileptonico = (len(nu_solo_top_indices) == 2) # EXACTAMENTE 2 neutrinos de los Tops

    if es_canal_4nu and es_top_dileptonico:
        eventos_4nu_y_tt_dileptonico += 1

        # 1. Curva ROJA: pTmiss de los 4 neutrinos del Higgs
        sum_px_h = sum(event.GenPart_pt[idx] * r.TMath.Cos(event.GenPart_phi[idx]) for idx in nu_solo_zz_indices)
        sum_py_h = sum(event.GenPart_pt[idx] * r.TMath.Sin(event.GenPart_phi[idx]) for idx in nu_solo_zz_indices)
        h_met_higgs_zz.Fill(r.TMath.Sqrt(sum_px_h**2 + sum_py_h**2))

        # 2. Curva AZUL: pTmiss de los 2 neutrinos de los Tops
        sum_px_t = sum(event.GenPart_pt[idx] * r.TMath.Cos(event.GenPart_phi[idx]) for idx in nu_solo_top_indices)
        sum_py_t = sum(event.GenPart_pt[idx] * r.TMath.Sin(event.GenPart_phi[idx]) for idx in nu_solo_top_indices)
        h_met_solo_top.Fill(r.TMath.Sqrt(sum_px_t**2 + sum_py_t**2))

        # 3. Curva NEGRA: combinación de las curvas anteriores
        indices_totales = nu_solo_zz_indices + nu_solo_top_indices
        sum_px_tot = sum(event.GenPart_pt[idx] * r.TMath.Cos(event.GenPart_phi[idx]) for idx in indices_totales)
        sum_py_tot = sum(event.GenPart_pt[idx] * r.TMath.Sin(event.GenPart_phi[idx]) for idx in indices_totales)
        h_met_combinado.Fill(r.TMath.Sqrt(sum_px_tot**2 + sum_py_tot**2))

print(f"[RESUMEN] Eventos aislados del canal puro H -> ZZ -> 4nu: {eventos_4nu_y_tt_dileptonico}")

# 4. Normalizaión (área = 1)
print("\n[INFO] Normalizando histogramas por unidad de área...")
for h in [h_met_higgs_zz, h_met_solo_top, h_met_combinado]:
    if h.Integral() > 0:
        h.Scale(1.0 / h.Integral())

# 5. Guardado
ruta_guardado = "/eos/user/d/drasilla/MET"
os.makedirs(ruta_guardado, exist_ok=True)

canvas = r.TCanvas("canvas_tth_4nu", "Estudio H->ZZ->4nu en ttH", 800, 600)
canvas.SetLeftMargin(0.15)

# Estilos cromáticos
h_met_higgs_zz.SetLineColor(r.kRed)
h_met_higgs_zz.SetLineWidth(2)
h_met_solo_top.SetLineColor(r.kBlue)
h_met_solo_top.SetLineWidth(2)
h_met_combinado.SetLineColor(r.kBlack)
h_met_combinado.SetLineWidth(2)

for h in [h_met_higgs_zz, h_met_solo_top, h_met_combinado]:
    h.SetStats(0)
    h.GetYaxis().SetTitleOffset(1.4)

# Escala automática dejando un 20% de margen superior para la leyenda
max_global = max(h_met_higgs_zz.GetMaximum(), h_met_solo_top.GetMaximum(), h_met_combinado.GetMaximum())
h_met_higgs_zz.SetMaximum(max_global * 1.15)

# Dibujo
h_met_higgs_zz.Draw("HIST")
h_met_solo_top.Draw("HIST SAME")
h_met_combinado.Draw("HIST SAME")

# Leyenda
leyenda = r.TLegend(0.40, 0.68, 0.88, 0.88)
leyenda.AddEntry(h_met_higgs_zz,  "p_{T}^{miss} (#nu_{H #rightarrow ZZ #rightarrow 4#nu})", "l")
leyenda.AddEntry(h_met_solo_top,   "p_{T}^{miss} (#nu_{t#bar{t} #rightarrow dilep})", "l")
leyenda.AddEntry(h_met_combinado,  "p_{T}^{miss} (#nu_{4#nu} + #nu_{dilep})", "l")
leyenda.SetBorderSize(0)
leyenda.SetTextSize(0.032)
leyenda.Draw()

# Guardado 
canvas.SaveAs(f"{ruta_guardado}/comparacion_ptmiss_3c_h_zz_4nu_2.png")
canvas.SaveAs(f"{ruta_guardado}/comparacion_ptmiss_3c_h_zz_4nu_2.pdf")

f_out = r.TFile(f"{ruta_guardado}/analisis_3componentes_h_zz_4nu.root", "RECREATE")
h_met_higgs_zz.Write()
h_met_solo_top.Write()
h_met_combinado.Write()
f_out.Close()

print(f"\n[INFO] ¡Proceso finalizado! Los gráficos y el archivo ROOT se guardaron en: {ruta_guardado}")
