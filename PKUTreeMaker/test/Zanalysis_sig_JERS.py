import FWCore.ParameterSet.Config as cms

process = cms.Process( "TEST" )
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
				     SkipEvent = cms.untracked.vstring('ProductNotFound'))
corrJetsOnTheFly = True
runOnMC = True #False
chsorpuppi = True  # AK4Chs or AK4Puppi
#****************************************************************************************************#
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_condDBv2_cff')
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("RecoTracker.CkfPattern.CkfTrackCandidates_cff")
process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
from Configuration.AlCa.GlobalTag import GlobalTag
if runOnMC:
#   process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v7'
   process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_miniAODv2_v1'
elif not(runOnMC):
   process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v6'

##########					                                                             
hltFiltersProcessName = 'RECO'
if runOnMC:
   hltFiltersProcessName = 'PAT' #'RECO'
reducedConversionsName = 'RECO'
if runOnMC:
   reducedConversionsName= 'PAT' #'RECO'

process.load("VAJets.PKUCommon.goodMuons_cff")
process.load("VAJets.PKUCommon.goodElectrons_cff")
process.load("VAJets.PKUCommon.goodJets_cff")
process.load("VAJets.PKUCommon.goodPhotons_cff")
process.load("VAJets.PKUCommon.leptonicZ_cff")

#for egamma smearing

from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights
process = regressionWeights(process)
process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')

process.load('Configuration.StandardSequences.Services_cff')
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
   calibratedPatElectrons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
      engineName = cms.untracked.string('TRandom3'),
   ),
   calibratedPatPhotons  = cms.PSet( initialSeed = cms.untracked.uint32(81),
      engineName = cms.untracked.string('TRandom3'),
   ),
)
process.load('EgammaAnalysis.ElectronTools.calibratedPatElectronsRun2_cfi')
process.load('EgammaAnalysis.ElectronTools.calibratedPatPhotonsRun2_cfi')
process.calibratedPatElectrons.electrons = cms.InputTag("slimmedElectrons")
process.calibratedPatElectrons.isMC = cms.bool(runOnMC)
process.calibratedPatPhotons.photons = cms.InputTag('slimmedPhotons')
process.calibratedPatPhotons.isMC = cms.bool(runOnMC)

#for egamma smearing

# If Update
process.goodMuons.src = "slimmedMuons"
#process.goodElectrons.src = "slimmedElectrons"
#process.goodPhotons.src = "slimmedPhotons"
process.goodElectrons.src = "calibratedPatElectrons"
process.goodPhotons.src = "calibratedPatPhotons"

# jerc uncer 2017/5/7
if chsorpuppi:
        jLabel = "slimmedJets"
        jetAlgo    = 'AK4PFchs'
else:
      jLabel = "slimmedJetsPuppi"
      jetAlgo    = 'AK4PFPuppi'

jer_era = "Summer16_23Sep2016V3_MC"
triggerResultsLabel      = "TriggerResults"
triggerSummaryLabel      = "hltTriggerSummaryAOD"
hltProcess = "HLT"

#begin------------JEC on the fly--------
if runOnMC:
   jecLevelsAK4chs = [
          'Summer16_23Sep2016V3_MC_L1FastJet_AK4PFchs.txt',
          'Summer16_23Sep2016V3_MC_L2Relative_AK4PFchs.txt',
          'Summer16_23Sep2016V3_MC_L3Absolute_AK4PFchs.txt'
    ]
   jecLevelsAK4puppi = [
          'Summer16_23Sep2016V3_MC_L1FastJet_AK4PFPuppi.txt',
          'Summer16_23Sep2016V3_MC_L2Relative_AK4PFPuppi.txt',
          'Summer16_23Sep2016V3_MC_L3Absolute_AK4PFPuppi.txt'
    ]
else:
   jecLevelsAK4chs = [
          'Summer16_23Sep2016BCDV3_DATA_L1FastJet_AK4PFchs.txt',
          'Summer16_23Sep2016BCDV3_DATA_L2Relative_AK4PFchs.txt',
          'Summer16_23Sep2016BCDV3_DATA_L3Absolute_AK4PFchs.txt',
          'Summer16_23Sep2016BCDV3_DATA_L2L3Residual_AK4PFchs.txt'
    ]
   jecLevelsAK4puppi = [
          'Summer16_23Sep2016BCDV3_DATA_L1FastJet_AK4PFPuppi.txt',
          'Summer16_23Sep2016BCDV3_DATA_L2Relative_AK4PFPuppi.txt',
          'Summer16_23Sep2016BCDV3_DATA_L3Absolute_AK4PFPuppi.txt',
          'Summer16_23Sep2016BCDV3_DATA_L2L3Residual_AK4PFPuppi.txt'
    ]
#end------------JEC on the fly--------

process.JetUserData = cms.EDProducer(
   'JetUserData',
   jetLabel          = cms.InputTag(jLabel),
   rho               = cms.InputTag("fixedGridRhoFastjetAll"),
   coneSize          = cms.double(0.4),
   getJERFromTxt     = cms.bool(False),
   jetCorrLabel      = cms.string(jetAlgo),
   jerLabel          = cms.string(jetAlgo),
   resolutionsFile   = cms.string(jer_era+'_PtResolution_'+jetAlgo+'.txt'),
   scaleFactorsFile  = cms.string(jer_era+'_SF_'+jetAlgo+'.txt'),
   ### TTRIGGER ###
   triggerResults = cms.InputTag(triggerResultsLabel,"",hltProcess),
   triggerSummary = cms.InputTag(triggerSummaryLabel,"",hltProcess),
   hltJetFilter       = cms.InputTag("hltPFHT"),
   hltPath            = cms.string("HLT_PFHT800"),
   hlt2reco_deltaRmax = cms.double(0.2),
   candSVTagInfos         = cms.string("pfInclusiveSecondaryVertexFinder"), 
   jecAK4chsPayloadNames_jetUserdata = cms.vstring( jecLevelsAK4chs ),
   vertex_jetUserdata = cms.InputTag("offlineSlimmedPrimaryVertices")
   )
#jerc uncer Meng

process.load("VAJets.PKUCommon.goodJets_cff") 
if chsorpuppi:
#      process.goodAK4Jets.src = "slimmedJets"
	process.goodAK4Jets.src = "JetUserData"
	# jerc uncer Meng
else:
      process.goodAK4Jets.src = "slimmedJetsPuppi"

#process.goodOfflinePrimaryVertex = cms.EDFilter("VertexSelector",
#                                       src = cms.InputTag("offlineSlimmedPrimaryVertices"),
#                                       cut = cms.string("chi2!=0 && ndof >= 4.0 && abs(z) <= 24.0 && abs(position.Rho) <= 2.0"),
#                                       filter = cms.bool(False)
#                                       )

ZBOSONCUT = "pt > 0.0"

process.leptonicVSelector = cms.EDFilter("CandViewSelector",
                                       src = cms.InputTag("leptonicV"),
                                       cut = cms.string( ZBOSONCUT ), 
                                       filter = cms.bool(False)
                                       )

process.leptonicVFilter = cms.EDFilter("CandViewCountFilter",
                                       src = cms.InputTag("leptonicV"),
                                       minNumber = cms.uint32(0),
                                       filter = cms.bool(False)
                                       )


process.leptonSequence = cms.Sequence(process.muSequence +
				      process.regressionApplication* process.calibratedPatElectrons* process.calibratedPatPhotons +
                                      process.eleSequence +
                                      process.leptonicVSequence +
                                      process.leptonicVSelector +
                                      process.leptonicVFilter )

process.jetSequence = cms.Sequence(process.NJetsSequence)

process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.load("RecoMET.METFilters.BadChargedCandidateFilter_cfi")
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")
process.metfilterSequence = cms.Sequence(process.BadPFMuonFilter+process.BadChargedCandidateFilter)

if chsorpuppi:
      ak4jecsrc = jecLevelsAK4chs
else:
      ak4jecsrc = jecLevelsAK4puppi

process.load("RecoEgamma/PhotonIdentification/PhotonIDValueMapProducer_cfi")
   
process.treeDumper = cms.EDAnalyzer("ZPKUTreeMaker",
                                    originalNEvents = cms.int32(1),
                                    crossSectionPb = cms.double(1),
                                    targetLumiInvPb = cms.double(1.0),
                                    PKUChannel = cms.string("VW_CHANNEL"),
                                    isGen = cms.bool(False),
				    RunOnMC = cms.bool(runOnMC), 
                                    generator =  cms.InputTag("generator"),
				    genJet =  cms.InputTag("slimmedGenJets"),
                                    pileup  =   cms.InputTag("slimmedAddPileupInfo"),
                                    leptonicVSrc = cms.InputTag("leptonicV"),
                                    rho = cms.InputTag("fixedGridRhoFastjetAll"),   
                                    ak4jetsSrc = cms.InputTag("cleanAK4Jets"),      
                                    photonSrc = cms.InputTag("calibratedPatPhotons"),
                                    #photonSrc = cms.InputTag("slimmedPhotons"),
                                    genSrc =  cms.InputTag("prunedGenParticles"),       
                                    jecAK4chsPayloadNames = cms.vstring( jecLevelsAK4chs ),
                                    jecAK4PayloadNames = cms.vstring( ak4jecsrc ),
                                    metSrc = cms.InputTag("slimmedMETs"),
                                    vertex = cms.InputTag("offlineSlimmedPrimaryVertices"),  
                                    t1jetSrc_user = cms.InputTag("JetUserData"),
				    t1jetSrc = cms.InputTag("slimmedJets"),      
                                    t1muSrc = cms.InputTag("slimmedMuons"),       
                                    #looseelectronSrc = cms.InputTag("vetoElectrons"),
                                    looseelectronSrc = cms.InputTag("calibratedPatElectrons"),
                                    electrons = cms.InputTag("slimmedElectrons"),
                                    conversions = cms.InputTag("reducedEgamma","reducedConversions",reducedConversionsName),
                                    beamSpot = cms.InputTag("offlineBeamSpot","","RECO"),
                                    loosemuonSrc = cms.InputTag("looseMuons"),
				    goodmuonSrc = cms.InputTag("goodMuons"),# station2 retrieve, 2017/3/26
                                    hltToken    = cms.InputTag("TriggerResults","","HLT"),
				    elPaths1     = cms.vstring("HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v*"),
                                    elPaths2     = cms.vstring("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*"),
				    muPaths1	= cms.vstring("HLT_Mu17_TrkIsoVVL_v*"),
                                    muPaths2     = cms.vstring("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v*", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*"),
				    muPaths3    = cms.vstring("HLT_IsoMu24_v*"), 
				    muPaths4    = cms.vstring("HLT_Mu17_v*"),
				    muPaths5     = cms.vstring("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v*", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v*"),
				    muPaths6     = cms.vstring("HLT_IsoMu22_v*", "HLT_IsoTkMu22_v*"),
				    muPaths7     = cms.vstring("HLT_IsoMu24_v*", "HLT_IsoTkMu24_v*"),
				    muPaths8     = cms.vstring("HLT_IsoMu27_v*", "HLT_IsoTkMu27_v*"),
				    noiseFilter = cms.InputTag('TriggerResults','', hltFiltersProcessName),
				    noiseFilterSelection_HBHENoiseFilter = cms.string('Flag_HBHENoiseFilter'),
                                    noiseFilterSelection_HBHENoiseIsoFilter = cms.string("Flag_HBHENoiseIsoFilter"),
                                    noiseFilterSelection_globalTightHaloFilter = cms.string('Flag_globalTightHalo2016Filter'),
                                    noiseFilterSelection_EcalDeadCellTriggerPrimitiveFilter = cms.string('Flag_EcalDeadCellTriggerPrimitiveFilter'),
				    noiseFilterSelection_goodVertices = cms.string('Flag_goodVertices'),
				    noiseFilterSelection_eeBadScFilter = cms.string('Flag_eeBadScFilter'),
                                    noiseFilterSelection_badMuon = cms.InputTag('BadPFMuonFilter'),
                                    noiseFilterSelection_badChargedHadron = cms.InputTag('BadChargedCandidateFilter'),
                #Meng
                                    badMuonFilterSelection = cms.string('Flag_badMuons'),
                                    duplicateMuonFilterSelection = cms.string('Flag_duplicateMuons'),
                #Lu
				    full5x5SigmaIEtaIEtaMap   = cms.InputTag("photonIDValueMapProducer:phoFull5x5SigmaIEtaIEta"),
                                    phoChargedIsolation = cms.InputTag("photonIDValueMapProducer:phoChargedIsolation"),
                                    phoNeutralHadronIsolation = cms.InputTag("photonIDValueMapProducer:phoNeutralHadronIsolation"),
                                    phoPhotonIsolation = cms.InputTag("photonIDValueMapProducer:phoPhotonIsolation"),
                                    effAreaChHadFile = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfChargedHadrons_25ns_NULLcorrection.txt"),
                                    effAreaNeuHadFile= cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfNeutralHadrons_25ns_90percentBased.txt"),
                                    effAreaPhoFile   = cms.FileInPath("RecoEgamma/PhotonIdentification/data/Spring15/effAreaPhotons_cone03_pfPhotons_25ns_90percentBased.txt")
                                    )


process.analysis = cms.Path(
			    process.JetUserData +
#                            process.goodOfflinePrimaryVertex +
                            process.leptonSequence +
                            process.jetSequence +
                            process.metfilterSequence +
#                           process.photonSequence +
                            process.photonIDValueMapProducer*process.treeDumper)

### Source
process.load("VAJets.PKUCommon.data.RSGravitonToWW_kMpl01_M_1000_Tune4C_13TeV_pythia8")
process.source.fileNames = [
#"file:/eos/uscms/store/mc/RunIISummer16MiniAODv2/TprimeTprimeToTHTH_HToGammaGamma_M-600_TuneCUETP8M2T4_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/60000/641784F0-2BD8-E611-ABC5-02163E013616.root"
#"/store/mc/RunIISummer16MiniAODv2/LLAJJ_EWK_MLL-50_MJJ-120_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/08DCD9BB-2C25-E711-90C9-C454449229AF.root"
"/store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/70000/041A166C-B53F-E611-BF34-5CB90179CCC0.root"
]
                       
process.maxEvents.input = 1

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.cerr.FwkReport.limit = 99999999

process.TFileService = cms.Service("TFileService",
                                    fileName = cms.string("ZtreePKU.root")
                                   )
