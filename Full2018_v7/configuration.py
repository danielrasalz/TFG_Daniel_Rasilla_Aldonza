"""
Código que incluye la configuración de mkShapes

Adaptado de: https://github.com/piedraj/HEP/blob/main/Full2018_v7/configuration.py
"""
treeName = 'Events'

# Tag used to identify the configuration folder version
tag = 'cambio_mll_puppimet'

# File to use as runner script, default uses mkShapesRDF.shapeAnalysis.runner, otherwise specify path to script
runnerFile = "default"

# Output file name
outputFile = "mkShapes__{}.root".format(tag)

# Path to ouput folder
outputFolder  = "cambio_mll_puppimet"

# Path to batch folder (used for condor submission)
batchFolder = "condor"

# Path to configuration folder (will contain all the compiled configuration files)
configsFolder = "configs"

# File with TTree aliases
aliasesFile = 'aliases.py'

# File with list of variables
variablesFile = 'variables.py'

# File with list of cuts
cutsFile = 'cuts_emu.py'

# File with list of samples
samplesFile = 'samples.py'

# File with colors of samples
plotFile = 'plot_estudio.py'

# Luminosity to normalize to (in 1/fb)
lumi = 59.83

# Used by mkDatacards to define output directory for datacards
outputDirDatacard = "datacards__{}".format(tag)

# Structure file for datacard
structureFile = 'structure.py'

# Nuisances file for mkDatacards and for mkShape
nuisancesFile = 'nuisances.py'

# Path to folder where to save plots
plotPath = "plots__{}".format(tag)

# List of imports to import when compiling the whole configuration folder, it should not contain imports used by config>
imports = ["os", "glob", ("collections", "OrderedDict"), "ROOT"]

# List of files to compile
filesToExec = [
    samplesFile,
    aliasesFile,
    variablesFile,
    cutsFile,
    plotFile,
    nuisancesFile,
    structureFile,
]

# List of variables to keep in the compiled configuration folder
varsToKeep = [
    "batchVars",
    "outputFolder",
    "batchFolder",
    "configsFolder",
    "outputFile",
    "runnerFile",
    "tag",
    "samples",
    "aliases",
    "variables",
    ("cuts", {"cuts": "cuts", "preselections": "preselections"}),
    ("plot", {"plot": "plot", "groupPlot": "groupPlot", "legend": "legend"}),
    "nuisances",
    "structure",
    "lumi",
]

# List of variables to keep in the batch submission script (script.py)
batchVars = varsToKeep[varsToKeep.index("samples") :]

varsToKeep += ['plotPath']
