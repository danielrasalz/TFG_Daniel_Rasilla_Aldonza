"""
Código empleado para obtener las diferentes gráficas de la significancia en función de los cortes establecidos dentro del rango de energías para 
una variable dada. En él se emplean los histogramas creados con mkShapes además de permitir elegir la dirección del corte. Así mismo, el código devuelve
tanto el corte que permite maximizar el valor de la figura de mérito, como el valor de esta.
"""

import ROOT
import math

# --- CONFIGURACIÓN ---
file_path = "cambio_mll_puppimet/mkShapes__cambio_mll_puppimet.root"
cut_name  = "emu_tttDM"
variable  = "mth"
# ---------------------

def scan_bins_con_grafica():
    opcion = input("\nElige opción (1 (derecha) o 2 (izquierda): ")
    f = ROOT.TFile.Open(file_path)
    h_sig = f.Get(f"{cut_name}/{variable}/histo_ttH_ZZ4nu")

    muestras_fondo = ["DY", "VZ", "WW", "SingleTop", "ttbar", "tt_semileptonic", "ttV", "Other"]
    h_bkg = None
    for b in muestras_fondo:
        h = f.Get(f"{cut_name}/{variable}/histo_{b}")
        if h:
            if h_bkg is None: h_bkg = h.Clone("h_bkg_total")
            else: h_bkg.Add(h)

    nbins = h_sig.GetNbinsX()

    # Listas para guardar los datos de la gráfica
    x_values = []
    y_values = []

    max_fom = -1
    best_bin_edge = 0

    print(f"\n{'Corte [GeV]':>12} | {'S':>10} | {'B':>10} | {'FOM':>10}")
    print("-" * 50)

    for i in range(1, nbins + 1):
        edge = h_sig.GetBinLowEdge(i)

        if opcion == "1":
            # Caso > : Integral desde el bin i hasta el final
            s = h_sig.Integral(i, nbins + 1)
            b = h_bkg.Integral(i, nbins + 1)
            tipo_corte = ">"
        else:
            # Caso < : Integral desde el principio hasta el bin i
            s = h_sig.Integral(1, i)
            b = h_bkg.Integral(1, i)
            tipo_corte = "<"

        fom = s / math.sqrt(s + b) if (s + b) > 0 else 0


        # Guardado de puntos
        x_values.append(edge)
        y_values.append(fom)

        print(f"{edge:12.1f} | {s:10.2f} | {b:10.2f} | {fom:10.5f}")

        if fom > max_fom:
            max_fom = fom
            best_bin_edge = edge

    # --- CREACIÓN DE LA GRÁFICA ---
    graph = ROOT.TGraph(len(x_values))
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        graph.SetPoint(i, x, y)

    # Configuración estética de la gráfica
    canvas = ROOT.TCanvas("c1", "Optimización", 500, 500)
    
    canvas.SetLeftMargin(0.18)
    canvas.SetRightMargin(0.05)  
    canvas.SetBottomMargin(0.12)
    canvas.SetTopMargin(0.08)   
    graph.SetTitle(f";Corte en {variable} [GeV] ;Significancia (S/#sqrt{{S+B}})")
    graph.SetMarkerStyle(20)
    graph.SetMarkerSize(1.0)
    graph.SetLineColor(ROOT.kBlue)
    graph.SetLineWidth(2)
    graph.Draw("AL") 
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)

    # Guardar la imagen
    canvas.SaveAs(f"/eos/user/d/drasilla/optimización_cortes_ZZto4nunu/correcion_shapes fom_emu_bien_{variable}_{cut_na>

    print("-" * 50)
    print(f"GRÁFICA GUARDADA: fom_emu_{variable}_{cut_name}.png")
    print(f"Mejor corte: {best_bin_edge} GeV (FOM: {max_fom:.5f})")

if __name__ == "__main__":
    scan_bins_con_grafica()
