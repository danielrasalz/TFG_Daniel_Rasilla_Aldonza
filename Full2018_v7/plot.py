"""
Código empleado para configurar los diferentes histogramas de mkShapes

Adaptado de: https://github.com/piedraj/HEP/blob/main/Full2018_v7/plot.py
"""

groupPlot = {}
plot = {}

#Agrupación de las muestras definidas en samples 
groupPlot['DY'] = {
    'nameHR' : "DY",
    'isSignal' : 0,
    'color': 418,    # kGreen+2
    'samples'  : ['DY']
}

groupPlot['tt_semileptonic'] = {
    'nameHR' : "Semi Leptonic",
    'isSignal' : 0,
    'color' : 632,
    'samples' : ['tt_semileptonic']
}

groupPlot['VV'] = {
    'nameHR' : 'VV',
    'isSignal' : 0,
    'color': 851,    # Azul Azure
    'samples' : ['WW', 'VZ'] 
}

groupPlot['ttbar'] = {
    'nameHR' : "t#bar{t}",
    'isSignal' : 0,
    'color': 400,    # Amarillo
    'samples'  : ['ttbar']
}

groupPlot['SingleTop'] = {
    'nameHR' : 'Single top',
    'isSignal' : 0,
    'color': 606,    # Rosa fucsia
    'samples'  : ['SingleTop']
}

groupPlot['ttV'] = {
    'nameHR' : 'ttV',
    'isSignal' : 0,
    'color': 620,    # Violeta oscuro
    'samples'  : ['ttV']
}

groupPlot['Other'] = {
    'nameHR' : 'Other',
    'isSignal' : 0,
     'color': 920,    # Gris
    'samples'  : ['Other'] 
}

### señal ###
groupPlot['ttH_nonbb'] = { 
    'nameHR' : 'ttH non-bb',
    'isSignal' : 2,      # estilo de línea
    'color'    : 632,    # Rojo (kRed)
    'samples'  : ['ttH_nonbb'] 
}

#Definición individual

plot['DY'] = {
  'nameHR':"DY",
  'color':418,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['WW'] = {
  'nameHR':"WW",
  'color':851,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['VZ'] = {
  'nameHR':"VZ",
  'color':851,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['ttbar'] = {
  'nameHR':"t#bar{t}",
  'color':400,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['tt_semileptonic'] = {
  'nameHR':'Semi Leptonic',
  'color':616,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['ttV'] = {
  'nameHR':'ttV',
  'color':620,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['SingleTop'] = {
  'nameHR':'Single top',
  'color':606,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['Other'] = {
  'nameHR':'Other',
  'color':920,
  'isSignal':0,
  'isData':0,
  'scale':1.0
}

plot['ttH_nonbb'] = {
    'nameHR' : 'ttH non-bb',
    'color'  : 632,    # Rojo (KRed)
    'isSignal' : 2,    
    'isData'   : 0,
    'scale'    : 1.0   
}

plot['DATA']  = {
    'nameHR' : 'Data',
    'color': 1 ,
    'isSignal' : 0,
    'isData'   : 1 ,
    'isBlind'  : 0
}


legend = {}
legend['lumi'] = 'L = 59.74/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'

