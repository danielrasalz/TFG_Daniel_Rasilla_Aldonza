"""
Código empleado para obtener los BR del Higgs mostrados en la tabla 4.2
"""
import ROOT as r

# 1. TChain para unir los 23 archivos
chain = r.TChain("Events")
ruta =  "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/nanoLatino_ttHToNonbb_M125__part*.root"
chain.Add(ruta)

# 2. Archivo de salida
fOut = r.TFile("/eos/user/d/drasilla/www/fout_check_skim.root", "RECREATE")

# 2. Diccionario de contadores
counts = {"WW": 0, "ZZ": 0, "tautau": 0, "cc": 0, "otros": 0}
total_higgs = 0

# Diccionario para identificar qué son los "others"
ids_en_otros = {}

print(f"Analizando la señal ttH en {chain.GetEntries()} eventos...")

# 3. Bucle principal sobre los archivos
for i, event in enumerate(chain):
    # Impresión del progreso cada 10k eventos
    if i % 10000 == 0:
        print(f"Procesando evento {i}...")

    nGen = len(event.GenPart_pdgId)
    for j in range(nGen):
        # búsqueda de la última copia
        isLastCopy = bool(event.GenPart_statusFlags[j] & (1 << 13))
        if event.GenPart_pdgId[j] == 25 and isLastCopy:
            total_higgs += 1
            higgs_idx = j

            # Lista para guardar los hijos del Higgs
            hijos = []
            for k in range(nGen):
                if event.GenPart_genPartIdxMother[k] == higgs_idx:
                    hijos.append(abs(event.GenPart_pdgId[k]))

            # 4. Clasificación de la desintegración
            if 24 in hijos:
                counts["WW"] += 1
            elif 23 in hijos:
                counts["ZZ"] += 1
            elif 15 in hijos:
                counts["tautau"] += 1
            elif 4 in hijos:
                counts["cc"] += 1
            else:
                counts["otros"] += 1
                
                for id_hijo in hijos:
                    if id_hijo not in ids_en_otros:
                        ids_en_otros[id_hijo] = 1
                    else:
                        ids_en_otros[id_hijo] += 1
            break  # Encontrado el Higgs, saltamos al siguiente evento

fOut.Write()
fOut.Close()

# 5. Informe final 
if total_higgs > 0:
    print("\n" + "=" * 40)
    print("   VALIDACIÓN DE BRANCHING RATIOS (BR)")
    print("=" * 40)
    print(f"Total Higgs encontrados (isLastCopy): {total_higgs}")
    print("-" * 40)

    for decay, num in counts.items():
        porcentaje = (num / total_higgs) * 100
        print(f" Canal H -> {decay:7} | Eventos: {num:6} | BR: {porcentaje:6.2f}%")

    print("-" * 40)
    print("Nota: H -> bb debería ser 0% en esta muestra 'Nonbb'.")
    print("\n" + "-" * 50)
    print("INVESTIGACIÓN DE LA CATEGORÍA 'OTROS' (Hijos del Higgs):")
    if not ids_en_otros:
        print("No hay eventos en 'otros'.")
    else:
        for pid, cant in ids_en_otros.items():
            print(f" PDG ID: {pid:4} | Cantidad: {cant}")
    print("=" * 50)
else:
    print("No se encontraron Higgs.")
