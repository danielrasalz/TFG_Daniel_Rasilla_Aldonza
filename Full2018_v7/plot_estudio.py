groupPlot = {}
plot = {}


groupPlot['DY'] = {
    'nameHR' : "DY",
    'isSignal' : 0,
    'color': 418,    # kGreen+2
    'samples'  : ['DY']
}

groupPlot['TOP'] = {
    'nameHR' : "TOP",
    'isSignal' : 0,
    'color': 400,    # Amarillo
    'samples'  : ['ttbar', 'tt_semileptonic', 'SingleTop', 'ttV'] 
}

groupPlot['Other'] = {
    'nameHR' : 'Other',
    'isSignal' : 0,
    'color': 920,    # Gris
    'samples'  : ['Other','WW', 'VZ' ] 

groupPlot['ttH_ZZ4nu'] = { # O el nombre que le hayas dado
    'nameHR' : 'ttH_ZZ4nu',
    'isSignal' : 1,      # 2 para que sea una línea
    'color'    : 632,    # Rojo (kRed)
    'samples'  : ['ttH_ZZ4nu'] # Asegúrate de que estos nombres coinciden con samples.py
}



plot['DY'] = {'nameHR':"DY",'color':418,'isSignal':0,'isData':0,'scale':1.0}




plot['WW'] = {'nameHR':"WW",'color':851,'isSignal':0,'isData':0,'scale':1.0}
plot['VZ'] = {'nameHR':"VZ",'color':851,'isSignal':0,'isData':0,'scale':1.0}

plot['ttbar'] = {'nameHR':"t#bar{t}",'color':400,'isSignal':0,'isData':0,'scale':1.0}
plot['tt_semileptonic'] = {'nameHR':'Semi Leptonic','color':616,'isSignal':0,'isData':0,'scale':1.0}
plot['ttV'] = {'nameHR':'ttV','color':620,'isSignal':0,'isData':0,'scale':1.0}
plot['SingleTop'] = {'nameHR':'Single top','color':606,'isSignal':0,'isData':0,'scale':1.0}
plot['Other'] = {'nameHR':'Other','color':920,'isSignal':0,'isData':0,'scale':1.0}

plot['ttH_ZZ4nu'] = {
    'nameHR' : 'ttH_ZZ4nu',
    'color'  : 632,    # Rojo (KRed)
    'isSignal' : 1,    # 
    'isData'   : 0,
    'scale'    : 100   # ¡IMPORTANTE! Multiplicar por 100 para que se vea en la gráfica,
                       # si no, será una línea invisible en el suelo.
}


# --- Opciones adicionales ---
legend = {}
legend['lumi'] = 'L = 59.74/fb'
legend['sqrt'] = '#sqrt{s} = 13 TeV'
