
cuts = {}

# --- 1. Definición de la Preselección (Criterios Base) ---
# Estos cortes se aplican a TODOS los eventos antes de dividirlos en categorías.
_tmp = [

    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',  # 1. Al menos dos leptones, el tercero con pt < 10 GeV
    'Lepton_pdgId[0]*Lepton_pdgId[1] < 0',  # 2. Conservación de carga: uno positivo y otro negativo.
    'Lepton_pt[0] > 25.',                   # 3. El leptón líder debe tener energía suficiente (> 25 GeV).
    'Lepton_pt[1] > 20.',                   # 4. El segundo leptón debe tener > 20 GeV.
    'mll > 20.',                            # 6. Masa invariante de los dos leptones > 20 GeV para evitar resonancias b>
    'mpmet > 20.',                          # 7. Energía faltante proyectada mínima (característica de neutrinos/DM).
    'PuppiMET_pt > 20.',                    # 8. Energía faltante usando el algoritmo PUPPI > 20 GeV.
]

# --- 2. Z-Veto (Filtro para el proceso Drell-Yan) ---
# Si los dos leptones tienen el mismo sabor (ee o mumu), su masa no puede estar cerca de la del Z.
# Esto limpia el fondo donde un bosón Z decae a dos leptones sin materia oscura real.
z_veto = '((abs(Lepton_pdgId[0]*Lepton_pdgId[1]) != 11*11 && abs(Lepton_pdgId[0]*Lepton_pdgId[1]) != 13*13) || abs(mll >
_tmp.append(z_veto)

preselections = ' && '.join(_tmp)

# --- 3. Definición de Categorías Finales ---
cuts['ttDM_2018'] = {
    'expr': preselections,
    'categories' : {
        # --- Inclusivas ---
        'in_ee'   : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11',
        'in_mumu' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13',
        'in_emu'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13',

        #### Selección del análisis ####
        # tDM: Exactamente 1 b-jet (n_bJ = 1)
        'emu_ttDM': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && bReq_2bj && Sum((CleanJet_pt > 30) && (abs(CleanJ>

        'emu_tDM': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && bReq_eq1bj && Sum((CleanJet_pt > 30) && (abs(Clean>

        'emu_tttDM': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && ((bReq_eq1bj && Sum((CleanJet_pt > 30) && (abs(C>
    }
}
