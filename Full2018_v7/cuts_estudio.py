'''
Archivo con los cortes en forma secuecnial para poder comprobar el poder discriminante de cada uno
'''
preselections = '1'
cuts = {}


cuts['step0_skim'] = 'nLepton >= 2'

cuts['ch_3lep'] = cuts['step0_skim'] + ' && Lepton_pdgId[0]*Lepton_pdgId[1] < 0'+ ' && nLepton >= 2 && Alt(Lepton_pt,2,>

cuts['pt_cuts'] = cuts['ch_3lep'] + ' && Lepton_pt[0] > 25 && Lepton_pt[1] > 20'

cuts['mll>20'] = cuts['pt_cuts'] + ' && mll > 20'

cuts['mpmet>20'] = cuts['mll>20'] + ' && mpmet > 20'

cuts['PuppiMET_pt>20'] = cuts['mpmet>20'] + ' && PuppiMET_pt > 20'

cuts['ZVeto'] = cuts['PuppiMET_pt>20'] + ' && ((abs(Lepton_pdgId[0]*Lepton_pdgId[1]) != 11*11 && abs(Lepton_pdgId[0]*Lepton_pdgId[1]) != 13*13) || abs(mll - 91.1876) > 15.)'

# Regiones de señal

base_emu = cuts['ZVeto'] + ' && abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && nJets_pt30 >= 1'

cuts['emu_tDM'] = base_emu + ' && bReq_eq1bj'     # n_bJ = 1
cuts['emu_ttDM'] = base_emu + ' && bReq_2bj'      # n_bJ >= 2
cuts['emu_tttDM'] = base_emu + ' && (bReq_eq1bj || bReq_2bj)'  # n_bJ >= 1
