'''
Código empleado para obtener los BR de los decaimientos del Z mostrados en la tabla 4.3
'''

import ROOT as r

chain = r.TChain("Events")
ruta = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr>
chain.Add(ruta)


# Contadores
z_macro_counts = {
    "hadronic": 0,
    "leptonic": 0,
    "invisible": 0,
    "otros": 0
}

# Contadores específicos para cada tipo de neutrino
nu_counts = {
    "nu_e": 0,    # PDG 12
    "nu_mu": 0,   # PDG 14
    "nu_tau": 0   # PDG 16
}

total_Z_analizados = 0
ids_en_otros_z = {}
print(f"Analizando desintegraciones macro del Z en {chain.GetEntries()} eventos...")

# 3. Bucle principal
for i, event in enumerate(chain):
    if i % 10000 == 0:
        print(f"Procesando evento {i}...")


    nGen = len(event.GenPart_pdgId)
    for j in range(nGen):
        # Identificación del Higgs final (isLastCopy)
        isLastCopy = bool(event.GenPart_statusFlags[j] & (1 << 13))

        if event.GenPart_pdgId[j] == 25 and isLastCopy:
            higgs_idx = j

            # Búsqueda de hijos directos del Higgs
            for k in range(nGen):
                if event.GenPart_genPartIdxMother[k] == higgs_idx:

                    # Si el hijo es un Z (PDG 23), se inicia el rastreo
                    if abs(event.GenPart_pdgId[k]) == 23:
                        current_z_idx = k

                        # --- ALGORITMO RASTREADOR DE COPIAS DEL Z ---
                        # Si este Z se desintegra en OTRO Z (radiación), bajamos el escalón
                        mientras_haya_copias = True
                        while mientras_haya_copias:
                            found_next_z = False
                            for m in range(nGen):
                                # Buscamos si algún hijo de la partícula actual es OTRA VEZ un Z
                                if event.GenPart_genPartIdxMother[m] == current_z_idx and abs(event.GenPart_pdgId[m]) =>
                                    current_z_idx = m  # Actualizamos al Z más moderno
                                    found_next_z = True
                                    break  # Salimos del bucle para volver a comprobar desde este nuevo Z

                            if not found_next_z:
                                mientras_haya_copias = False  # Ya no hay más copias, estamos en el Z terminal

                        # Ahora 'current_z_idx' es el Z final real antes de romperse en fermiones
                        hijos_del_z = []
                        for m in range(nGen):
                            if event.GenPart_genPartIdxMother[m] == current_z_idx:
                                hijos_del_z.append(abs(event.GenPart_pdgId[m]))

                        total_Z_analizados += 1

                        # 4. Clasificación (.count() >= 2)
                        n_quarks = sum(hijos_del_z.count(q) for q in [1, 2, 3, 4, 5])

                        has_charged_leptons = (hijos_del_z.count(11) >= 2 or
                                               hijos_del_z.count(13) >= 2 or
                                               hijos_del_z.count(15) >= 2)

                        has_neutrinos = (hijos_del_z.count(12) >= 2 or
                                         hijos_del_z.count(14) >= 2 or
                                         hijos_del_z.count(16) >= 2)

                        if n_quarks >= 2:
                            z_macro_counts["hadronic"] += 1
                        elif has_charged_leptons:
                            z_macro_counts["leptonic"] += 1
                        elif has_neutrinos:
                            z_macro_counts["invisible"] += 1
                            
                            if hijos_del_z.count(12) >= 2:
                                nu_counts["nu_e"] += 1
                            elif hijos_del_z.count(14) >= 2:
                                nu_counts["nu_mu"] += 1
                            elif hijos_del_z.count(16) >= 2:
                                nu_counts["nu_tau"] += 1
                        else:
                            z_macro_counts["otros"] += 1
                            for id_hijo in hijos_del_z:
                                if id_hijo not in ids_en_otros_z:
                                    ids_en_otros_z[id_hijo] = 1
                                else:
                                    ids_en_otros_z[id_hijo] += 1

            break 


# Presentación de resultados 
if total_Z_analizados > 0:
    print("\n" + "="*45)
    print("     VALIDACIÓN DE BR DEL Z (CON RASTREO FSR)")
    print("="*45)
    print(f"Total bosones Z procedentes del H analizados: {total_Z_analizados}")
    print("-" * 45)

    for decay, num in z_macro_counts.items():
        porcentaje = (num / total_Z_analizados) * 100
        print(f" Canal Z -> {decay:9} | Eventos: {num:6} | BR: {porcentaje:6.2f}%")


    print("-" * 45)
    print(" DESGLOSE DEL CANAL INVISIBLE (NEUTRINOS):")
    total_nu = z_macro_counts["invisible"]
    if total_nu > 0:
        for nu_type, num in nu_counts.items():
            porc_sobre_Z = (num / total_Z_analizados) * 100
            porc_sobre_nu = (num / total_nu) * 100
            print(f"  * Z -> {nu_type:6} | Eventos: {num:6} | BR total: {porc_sobre_Z:5.2f}% (Del canal nu: {porc_sobre_nu:5.1f}%)")
    else:
        print("  No se registraron desintegraciones a neutrinos.")
    print("-" * 45)
    print("\n" + "-"*50)
    print("CONTENIDO EN 'OTROS':")
    if not ids_en_otros_z:
        print("La categoría 'Otros' está limpia.")
    else:
        for pid, cant in ids_en_otros_z.items():
            print(f" PDG ID en 'Otros': {pid:4} | Cantidad: {cant}")
    print("="*50)
else:
    print("No se encontraron bosones Z asociados al Higgs.")
          
