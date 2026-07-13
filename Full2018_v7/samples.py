import os, glob
import inspect
from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()
redirector = ""


################################################
################# SKIMS ########################
################################################

mcProduction = 'Autumn18_102X_nAODv7_Full2018v7'
dataReco = 'Run2018_102X_nAODv7_Full2018v7'
fakeReco = 'Run2018_102X_nAODv7_Full2018v7'
mcSteps = 'MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7{var}'
fakeSteps = 'DATAl1loose2018v7__l2loose__fakeW'
dataSteps = 'DATAl1loose2018v7__l2loose__l2tightOR2018v7'

samples = {}

##############################################
###### Tree base directory for the site ######
##############################################

##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1
'''
signalDirectory = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose201>
'''
def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))


mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, fakeReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)


def nanoGetSampleFiles(path, name):
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]

def CombineBaseW(samples, proc, samplelist):
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]["name"]))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame("Runs", leastFiles)
    s = dfSmall.Sum("genEventSumw").GetValue()
    f = ROOT.TFile(leastFiles[0])
    t = f.Get("Events")
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame("Runs", __files)
    s = df.Sum("genEventSumw").GetValue()
    newbaseW = str(xs / s)
    weight = newbaseW + "/baseW"

    for iSample in samplelist:
        addSampleWeight(samples, proc, iSample, weight)
      
def addSampleWeight(samples, sampleName, sampleNameType, weight):
    obj = list(filter(lambda k: k[0] == sampleNameType, samples[sampleName]["name"]))[0]
    samples[sampleName]["name"] = list(
        filter(lambda k: k[0] != sampleNameType, samples[sampleName]["name"])
    )
    if len(obj) > 2:
        samples[sampleName]["name"].append(
            (obj[0], obj[1], obj[2] + "*(" + weight + ")")
        )
    else:
        samples[sampleName]["name"].append((obj[0], obj[1], "(" + weight + ")"))




################################################
############ Data DECLARATION ##################
################################################
DataRun = [
            ['A','Run2018A-02Apr2020-v1'] ,
            ['B','Run2018B-02Apr2020-v1'] ,
            ['C','Run2018C-02Apr2020-v1'] ,
            ['D','Run2018D-02Apr2020-v1'] ,
          ]

DataSets = ['MuonEG','DoubleMuon','SingleMuon','EGamma']

DataTrig = {
            'MuonEG'         : 'Trigger_ElMu' ,
            'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
            'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
            'EGamma'         : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)' ,
           }


#########################################
############ MC COMMON ##################
#########################################

mcCommonWeightNoMatch = 'XSWeight*SFweight*METFilter_MC'
mcCommonWeight = 'XSWeight*SFweight*PromptGenLepMatch2l*METFilter_MC'

###########################################
#############  BACKGROUNDS  ###############
###########################################
###### DY #######

#ptllDYW_NLO = '(0.87*(gen_ptll<10)+(0.379119+0.099744*gen_ptll-0.00487351*gen_ptll**2+9.19509e-05*gen_ptll**3-6.0212e->
#ptllDYW_LO = '((0.632927+0.0456956*gen_ptll-0.00154485*gen_ptll*gen_ptll+2.64397e-05*gen_ptll*gen_ptll*gen_ptll-2.1937>

"""
useDYtt = True

files=[]
if useDYtt:
  files = nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50') + \
          nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO_ext1')

else:
  files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50') + \
          nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO_ext1')


samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*( !(Sum$(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0 &&\
                                     Sum$(LeptonGen_isPrompt==1 && LeptonGen_pt>15)>=2) )',
    'FilesPerJob': 6,
}
#addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50','DY_NLO_pTllrw')
#addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO_ext1','DY_LO_pTllrw')
"""

filesDYHT = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO_ext1') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-4to50_HT-100to200') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-4to50_HT-200to400') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-4to50_HT-400to600') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-4to50_HT-600toInf') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-70to100') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-100to200') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-200to400') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-400to600') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-600to800') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-800to1200') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-1200to2500') + \
nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_HT-2500toInf')

samples['DY'] = {
    'name': filesDYHT,
    'weight': mcCommonWeight + '*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0 && Sum>
    'FilesPerJob': 2,
}

addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO_ext1',  'LHE_HT<100.0')
addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50',  'LHE_HT<70.0')

###### VV (Dibosones) ######
files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu_ext1') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Q') + \
    nanoGetSampleFiles(mcDirectory, 'ZZTo4L_ext1') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo2L2Q')

samples['VZ'] = {
    'name': files,
    'weight': mcCommonWeight + '*1.11',
    'FilesPerJob': 4
}

samples['WW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
    'weight': mcCommonWeight + '*nllW',
    'FilesPerJob': 3
}

########### Single Top ############

filesST = nanoGetSampleFiles(mcDirectory, 'ST_s-channel_ext1') + \
          nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
          nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
          nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop_ext1') + \
          nanoGetSampleFiles(mcDirectory, 'ST_tW_top_ext1')

samples['SingleTop'] = {
    'name': filesST,
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

####### TTbar ########
samples['ttbar'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu'),
    'weight': mcCommonWeight + '* Top_pTrw', # <--- Lo metes directamente aquí
    'FilesPerJob': 1,
}

###### Semileptonico ######
samples['tt_semileptonic'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')
            + nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic_ext3'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4,
}

####### tt mas boson #####
samples['ttV'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'TTWJetsToLNu')
            + nanoGetSampleFiles(mcDirectory, 'TTWjets')
            + nanoGetSampleFiles(mcDirectory, 'TTZToLLNuNu_M-10')
            + nanoGetSampleFiles(mcDirectory, 'TTZjets')
            + nanoGetSampleFiles(mcDirectory, 'ttH_H0PM_ToWWTo2L2Nu')
            + nanoGetSampleFiles(mcDirectory, 'ttH_H0M_ToWWTo2L2Nu')
            + nanoGetSampleFiles(mcDirectory, 'ttH_H0Mf05_ToWWTo2L2Nu'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

###### other ######
filesOther = nanoGetSampleFiles(mcDirectory,'tZq_ll') + \
    nanoGetSampleFiles(mcDirectory,'ZGToLLG') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + \
    nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HZJ_HToWWTo2L2Nu_M125') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125') + \
    nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HZJ_HToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToTauTau_M125')

samples['Other'] = {
    'name': filesOther,
    'weight': mcCommonWeight,
    'FilesPerJob': 10
}

samples['ttH_nonbb'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

samples['ttH_ZZ4nu'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),  # Mismos archivos
    'weight': mcCommonWeight + '* (Hdecay == 1)',  # Peso adicional para filtrar
    'FilesPerJob': 1,
}

samples['ttH_ZZ'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight + '* (Hdecay == 1 || Hdecay == 2)',
    'FilesPerJob': 1,
}
###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    tag_data = pd + '_' + sd

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v1','v2')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(fakeDirectory, tag_data)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', tag_data, DataTrig[pd])

samples['Fake']['subsamples'] = {
    'em': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13',
    'mm': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13',
    'ee': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11'
}

###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'METFilter_DATA*LepWPCut',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:

      tag = pd + '_' + sd

      files = nanoGetSampleFiles(dataDirectory, tag)
      samples['DATA']['name'].extend(files)
      addSampleWeight(samples, 'DATA', tag, DataTrig[pd])


   
