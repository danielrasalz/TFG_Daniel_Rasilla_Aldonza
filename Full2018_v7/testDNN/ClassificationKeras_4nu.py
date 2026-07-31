'''
Código empleado para el entrenamiento de los métodos de Pykeras y Fisher. En él primero se filtra la muestra de señal considerando únicamente aquellos eventos
en los que el Higgs decaiga en 4 neutrinos
'''
import ROOT as r
from ROOT import TMVA, TFile, TCut
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import SGD
from tensorflow.keras import Input
from tensorflow.keras.optimizers import Adam

# 1.Introducción de la lógica de HdecayProducer.cc
r.gInterpreter.Declare("""
#include <ROOT/RVec.hxx>
#include <vector>
#include <cmath>

int getHdecayCode(unsigned int nGenPart,
                  const ROOT::VecOps::RVec<int>& GenPart_pdgId,
                  const ROOT::VecOps::RVec<int>& GenPart_statusFlags,
                  const ROOT::VecOps::RVec<int>& GenPart_genPartIdxMother) {

    for (unsigned int j = 0; j < nGenPart; j++) {
        // Bit 13: isLastCopy
        bool isLastCopy = (GenPart_statusFlags[j] & (1 << 13)) != 0;

        if (std::abs(GenPart_pdgId[j]) == 25 && isLastCopy) {
            int nZ = 0;
            std::vector<int> z_indices;

            for (unsigned int k = 0; k < nGenPart; k++) {
                if (GenPart_genPartIdxMother[k] == (int)j) {
                    int absPdg = std::abs(GenPart_pdgId[k]);
                    if (absPdg == 23) {
                        z_indices.push_back((int)k);
                        nZ++;
                    }
                    else if (absPdg == 24) return 3; // WW
                    else if (absPdg == 15) return 4; // tau tau
                }
            }

            if (nZ == 2) {
                bool solo_neutrinos = true;
                for (int z_idx : z_indices) {
                    for (unsigned int m = 0; m < nGenPart; m++) {
                        if (GenPart_genPartIdxMother[m] == z_idx) {
                            int absPdgNieto = std::abs(GenPart_pdgId[m]);
                            if (absPdgNieto != 12 && absPdgNieto != 14 && absPdgNieto != 16) {
                                solo_neutrinos = false;
                                break;
                            }
                        }
                    }
                    if (!solo_neutrinos) break;
                }
                return solo_neutrinos ? 1 : 2;
            }
            return 6;
        }
    }
    return 0;
}
""")

# 2. Pre-filtrado de señal con RDataFrame 
path = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Autumn18_102X_nAODv7_Full2018v7/MCl1loose2018v7__MCCorr2018v7__l2loose__l2tightOR2018v7/"

print(">>> Iniciando RDataFrame para filtrar la señal (hDecay == 1)...")
df_signal = r.RDataFrame("Events", path + "nanoLatino_ttHToNonbb_M125__part*.root")

# Filtrado
df_signal = df_signal.Define("hDecay", "getHdecayCode(nGenPart, GenPart_pdgId, GenPart_statusFlags, GenPart_genPartIdxMother)")
df_signal_filtered = df_signal.Filter("hDecay == 1")

# Columnas necesarias para el entrenamiento 
columnas = ["mll", "mtw2", "mth", "mpmet", "PuppiMET_pt","Lepton_pt", "Lepton_pdgId", "nLepton", "CleanJet_pt", "nCleanJet", "CleanJet_eta", "Jet_btagDeepB", "CleanJet_jetIdx"]

# Guardado del Snapshot localmente 
df_signal_filtered.Snapshot("Events", "signal_ZZ4nu_filtered.root", columnas)
print(">>> Señal filtrada guardada en: signal_ZZ4nu_filtered.root")

# 3. CARGA DE DATOS PARA TMVA
TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()

output = TFile.Open('TMVA_4cap_noemu_cortesjets_eqnum.root', 'RECREATE')
factory = TMVA.Factory('TMVAClassification', output, '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')

dataloader = TMVA.DataLoader('dataset_4cap_noemu_cortesjets_eqnum')

# Carga de la señal filtrada y los fondos originales
signal_tree = r.TChain("Events")
signal_tree.Add("signal_ZZ4nu_filtered.root")

background_tree = r.TChain("Events")
background_tree.Add(path + "nanoLatino_TTTo2L2Nu__part*.root")
# background_tree.Add(path + "nanoLatino_WWTo2L2Nu__part*.root")

# Variables 

dataloader.AddVariable("mll", "F")
dataloader.AddVariable("mpmet", "F")
dataloader.AddVariable("mtw2", "F")
dataloader.AddVariable("mth", "F")
dataloader.AddVariable("PuppiMET_pt", "F")
dataloader.AddSignalTree(signal_tree, 1.0)
dataloader.AddBackgroundTree(background_tree, 1.0)

# 4. CORTES Y PREPARACIÓN 
# cortes en jets (al final no se emplearon)
corte_jets = "Sum$((CleanJet_pt > 30) && (abs(CleanJet_eta) < 2.4)) >= 1"
corte_bjet = "Sum$((CleanJet_pt > 20) && (abs(CleanJet_eta) < 2.4) && (Jet_btagDeepB[CleanJet_jetIdx] > 0.4184)) >= 1"
# resto de cortes
cortes_lista = [
    # 'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'nLepton >= 2',
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 20.',
    'mll > 20.',
    'mpmet > 20.',
    'PuppiMET_pt > 20.',
    corte_bjet,
    corte_jets
]
my_cut = r.TCut(" && ".join(cortes_lista))

# Configuración de eventos para entrenamiento y test
# Primera configuración:
# dataloader.PrepareTrainingAndTestTree(
#     my_cut,
#     'nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V'
# )
#segunda configuración (EqualNumEvents):
dataloader.PrepareTrainingAndTestTree(
    my_cut,
    'nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=EqualNumEvents:!V'
)

# 5. MODELO KERAS (input_dim=11)
model = Sequential([
    Input(shape=(5,)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    # Dense(64, activation='relu'),
    Dense(2, activation='softmax')
])
# Set loss and optimizer
model.compile(loss='categorical_crossentropy',
              optimizer=Adam(learning_rate=1e-3), weighted_metrics=['accuracy'])
model.save('model_4cap_noemu_cortesjets_eqnum.h5')
factory.BookMethod(dataloader, TMVA.Types.kFisher, 'Fisher',
                   '!H:!V:Fisher:VarTransform=D,G')
factory.BookMethod(dataloader, TMVA.Types.kPyKeras, 'PyKeras',
                   'H:!V:VarTransform=G:FilenameModel=model_4cap_noemu_cortesjets_eqnum.h5:NumEpochs=30:BatchSize=128')

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()
print("\n[OK] Entrenamiento completado.")
