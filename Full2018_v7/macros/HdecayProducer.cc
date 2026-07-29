'''
Código empleado para la separación de la muestra ttH_ToNonbb según el canal de desintegración del H
'''

#ifndef HdecayProducer_CC      
#define HdecayProducer_CC      

#include "ROOT/RVec.hxx"       
#include <cmath>               

using namespace ROOT;          
using namespace ROOT::VecOps;

// Clasificación del decaimiento del Higgs:
//   0: No se encontró Higgs en el evento
//   1: H -> ZZ -> 4ν (invisible)  ← Señal ideal para materia oscura
//   2: H -> ZZ visible (cualquier otro decay de los Z)
//   3: H -> WW
//   4: H -> ττ
//   5: H -> cc
//   6: H -> otros (gg, γγ, etc.)

int HdecayProducer(
    const RVec<int>& GenPart_pdgId,           // PDG ID de cada partícula (25=Higgs, 23=Z, 24=W, 15=τ, 4=c, 12/14/16=ν)
    const RVec<int>& GenPart_statusFlags,     // Flags de estado (bit 13 = última copia antes de decaer)
    const RVec<int>& GenPart_genPartIdxMother // Índice de la madre de cada partícula 
) {

    // 1. Número de partículas del evento
    int nGen = GenPart_pdgId.size();   // size() devuelve cuántas partículas hay

    // 2. Búsqueda del Higgs
    for (int j = 0; j < nGen; j++) {
        bool isLastCopy = (GenPart_statusFlags[j] & (1 << 13)) != 0;

        if (std::abs(GenPart_pdgId[j]) == 25 && isLastCopy) {
            RVec<int> hijos_ZZ;   // Vector para guardar los índices de los bosones Z encontrados

            // Recorrido sobre las partículas para encontrar las que tienen como madre al Higgs
            for (int k = 0; k < nGen; k++) {

                if (GenPart_genPartIdxMother[k] == j) {

                    int absPdg = std::abs(GenPart_pdgId[k]);  // Valor absoluto del PDG ID

                    // Clasificación
                    if (absPdg == 23) {
                        hijos_ZZ.push_back(k);
                    }
                    else if (absPdg == 24) return 3;  // H->WW (W bosón)
                    else if (absPdg == 15) return 4;  // H->ττ (tau leptón)
                    else if (absPdg == 4)  return 5;  // H->cc (quark charm)
                }
            }
      
            // 4. Verificación si es H->ZZ (exactamente 2 bosones Z)
            if (hijos_ZZ.size() == 2) {

                // 5: Comprobar si ambos Z decaen solo a neutrinos
                bool solo_neutrinos = true;  // Empezamos asumiendo que es invisible

                // Bucle sobre cada Z encontrado
                for (int z_idx : hijos_ZZ) {

                    // Búsqueda de sus hijos
                    for (int m = 0; m < nGen; m++) {

                        if (GenPart_genPartIdxMother[m] == z_idx) {

                            int absPdgNieto = std::abs(GenPart_pdgId[m]);

                            // Si algún nieto NO es neutrino -> es visible
                            // Neutrinos tienen PDG ID: 12 (νe), 14 (νμ), 16 (ντ)
                            if (absPdgNieto != 12 && absPdgNieto != 14 && absPdgNieto != 16) {
                                solo_neutrinos = false;  
                                break;  
                            }
                        }
                    }
                    if (!solo_neutrinos) break;  
                }

                // 6. Clasificación
                if (solo_neutrinos) return 1;  // H->ZZ->4ν (invisible)
                else return 2;                  // H->ZZ visible
            }

            return 6;  // H->otros (gg, γγ, etc.)
        }
    }
  
    return 0;
}

#endif
