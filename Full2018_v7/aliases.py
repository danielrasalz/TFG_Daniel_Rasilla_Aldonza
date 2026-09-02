"""
Código con los alias empleados em mkShapes

Adaptado de: https://github.com/piedraj/HEP/blob/main/Full2018_v7/aliases.py
"""

import os
import copy
import inspect
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
aliases = {}
#r.gSystem.Load("/afs/cern.ch/user/d/drasilla/mkShapesRDF/HEP/Full2018_v7/macros/HdecayProducer_cc.so")
# --- 1. Definición de muestras de MC ---
# Esto identifica automáticamente qué muestras no son datos reales para aplicarles pesos.
mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# --- 2. Working Points (Estándares de 2018) ---
eleWP = 'mvaFall17V1Iso_WP90'
muWP  = 'cut_Tight_HWWW'

# --- 3. Definición de B-tagging (Basado en la tabla de Nico) ---
bAlgo = 'DeepB'   # Algoritmo DeepCSV
bWP   = '0.4184'  # Medium Working Point para 2018
bSF   = 'deepcsv' # Nombre del Scale Factor oficial

# Alias para las categorías de los cortes
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, bWP)
}
# --- Definición de bIndexing (asegúrate de que solo esté una vez) ---
aliases['bIndexing'] = {
    'expr': 'Nonzero(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btagDeepB, CleanJet_jetIdx) > 0.4184)'
  }

# --- Aliases para extraer los valores individuales ---
aliases['pt_b1'] = {
    'expr': 'bIndexing.size() > 0 ? CleanJet_pt[bIndexing[0]] : -9999.0'
}

aliases['eta_b1'] = {
    'expr': 'bIndexing.size() > 0 ? CleanJet_eta[bIndexing[0]] : -9999.0'
}

aliases['pt_b2'] = {
    'expr': 'bIndexing.size() > 1 ? CleanJet_pt[bIndexing[1]] : -9999.0'
}

aliases['eta_b2'] = {
    'expr': 'bIndexing.size() > 1 ? CleanJet_eta[bIndexing[1]] : -9999.0'
}
aliases['bReq'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, bWP)
aliases['bReq_2bj'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 2'.format(bAlgo, bWP)
}

aliases['bReq_eq1bj'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 1'.format(bAlgo, bWP)
}

aliases['bIn'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.4 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 0'.format(bAlgo, bWP)
}

# --- 4. Scale Factors de B-tagging

aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF)
    'samples': mc
}


aliases['btagSF'] = {
    'expr': '(bVeto * bVetoSF) + (bReq * bReqSF) + (!bVeto && !bReq)',
    'samples': mc
}
# --- 5. Re-pesado del Top  ---
aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0..973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)'
    'samples': ['ttbar', 'ST']
}

# --- 6. Pesos de Leptones y Jet Pileup ---
aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

aliases['JetPUID_SF'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose)))',
  'samples': mc
}
# --- (SFweight) ---

aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSF', 'JetPUID_SF']),
    'samples': mc
}

# --- 8. Matching de Leptones ---
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched,0,0)*Alt(Lepton_promptgenmatched,1,0)',
    'samples': mc
}

# Para jets genéricos (pt > 30)
aliases['nJets_pt30'] = {
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.4)'
}


for shift in ['jes', 'lf', 'hf', 'lfstats1', 'lfstats2', 'hfstats1', 'hfstats2', 'cferr1', 'cferr2']:
    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepcsv_shape', 'btagSF_deepcsv_shape_up_%s' % shift)

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepcsv_shape', 'btagSF_deepcsv_shape_down_%s' % shift)

    aliases['btagSF%sup' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
        'samples': mc
    }

    aliases['btagSF%sdown' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
        'samples': mc
    }

# Pesos para los diferentes tipos de decaimientos de la señal:

aliases['Hdecay'] = {
    'linesToAdd': [f'#include "/afs/cern.ch/user/d/drasilla/mkShapesRDF/HEP/Full2018_v7/macros/HdecayProducer.cc"'],
    'class': 'HdecayProducer',
    'args': 'GenPart_pdgId, GenPart_statusFlags, GenPart_genPartIdxMother',
    'samples': ['ttH_nonbb', 'ttH_ZZ4nu', 'ttH_ZZ']
}
'''
# Los alias derivados se quedan igual
aliases['HtoZZ_inv'] = {
    'expr': 'Hdecay == 1',
    'samples': ['ttH_nonbb']
}

aliases['HtoZZ_total'] = {
    'expr': 'Hdecay == 1 || Hdecay == 2',
    'samples': ['ttH_nonbb']
}
''',
