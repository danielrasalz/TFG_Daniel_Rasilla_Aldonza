"""
Código para el primer entrenamiento de la muestra al completo sin filtrar
"""
#!/usr/bin/env python
## \file
## \ingroup tutorial_tmva_keras
## \notebook -nodraw
## This tutorial shows how to do classification in TMVA with neural networks
## trained with keras.
##
## \macro_code
##
## \date 2017
## \author TMVA Team
import ROOT as r
from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
from tensorflow.keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.optimizers import Adam
# Setup TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('TMVA_primer_entrenamiento2.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output,
                       '!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')

# Load data
if not isfile('tmva_class_example.root'):
    call(['curl', '-L', '-O', 'http://root.cern.ch/files/tmva_class_example.root'])

# 1. Ruta
path = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/"

# 2. Cadenas
signal = r.TChain("Events")
background = r.TChain("Events")

# 3. Señal 
signal.Add(path + "nanoLatino_ttHToNonbb_M125__part*.root")

# 4. Fondos
background.Add(path + "nanoLatino_TTTo2L2Nu__part*.root")
dataloader = TMVA.DataLoader('dataset_segun_ttH')

dataloader.AddVariable("mll", "F")
dataloader.AddVariable("mpmet", "F")
dataloader.AddVariable("mtw2", "F")
dataloader.AddVariable("mth", "F")
dataloader.AddVariable("PuppiMET_pt", "F")
dataloader.AddSignalTree(signal, 1.0)
dataloader.AddBackgroundTree(background, 1.0)

# Lista de cortes 
cortes_lista = [
    'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13', # Canal e-mu
    'nLepton == 2',                              # Al menos 2 leptones
    'Lepton_pt[0] > 25.',                        # PT leptón 1
    'Lepton_pt[1] > 20.',                        # PT leptón 2
    'mll > 20.',                                 # Masa dileptónica
    'mpmet > 20.',                               # MET proyectado
    'PuppiMET_pt > 20.'                          # MET Puppi
]


my_cut = " && ".join(cortes_lista)
dataloader.PrepareTrainingAndTestTree(
    my_cut,
    'nTrain_Signal=60000:'
    'nTrain_Background=60000:'
    'nTest_Signal=7546:'
    'nTest_Background=7546:'
    'SplitMode=Random:'
    'NormMode=NumEvents:!V'
)
print("Señal tras cortes =", signal.GetEntries(my_cut))
print("Fondo tras cortes =", background.GetEntries(my_cut))
print("Ratio B/S =", background.GetEntries(my_cut)/signal.GetEntries(my_cut))

# Generate model

model = Sequential([
    Input(shape=(5,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(2, activation='softmax')
])
# Set loss and optimizer
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(learning_rate=1e-3), weighted_metrics=['accuracy'])

# Store model to file
model.save('modelClassification_segun_ttH.h5')
model.summary()

# Book methods
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
                   '!H:!V:Fisher:VarTransform=D,G')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
                   'H:!V:VarTransform=D,G:FilenameModel=modelClassification_segun_ttH.h5:FilenameTrainedModel=trainedModelClassification.h5:NumEpochs=40:BatchSize=100')

# Run training, test and evaluation
factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()
