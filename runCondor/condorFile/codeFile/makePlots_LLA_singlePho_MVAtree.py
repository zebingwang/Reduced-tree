#! /usr/bin/env python

import argparse
parser = argparse.ArgumentParser(description="A simple ttree plotter")
parser.add_argument("-i", "--inputfiles", dest="inputfiles", default=["Sync_1031_2018_ttH_v2.root"], nargs='*', help="List of input ggNtuplizer files")
parser.add_argument("-o", "--outputfile", dest="outputfile", default="plots.root", help="Output file containing plots")
parser.add_argument("-m", "--maxevents", dest="maxevents", type=int, default=-1, help="Maximum number events to loop over")
parser.add_argument("-t", "--ttree", dest="ttree", default="Ana/passedEvents", help="TTree Name")
parser.add_argument("-xs", "--cross_section", dest="cross_section", default="1.0", help="the cross section of samples")
parser.add_argument("-L", "--Lumi", dest="Lumi", default="35.9", help="the luminosities to normalized")
args = parser.parse_args()

import numpy as np
import ROOT
import os
import random

###########################
from deltaR import *
from array import array


###########################
if os.path.isfile('~/.rootlogon.C'): ROOT.gROOT.Macro(os.path.expanduser('~/.rootlogon.C'))
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(000000)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gStyle.UseCurrentStyle()

sw = ROOT.TStopwatch()
sw.Start()

# Input ggNtuple
tchain = ROOT.TChain(args.ttree)
for filename in args.inputfiles: tchain.Add(filename)
print 'Total number of events: ' + str(tchain.GetEntries())

# Event weights
isMC = True
if 'Run2018' in filename:
    isMC = False
elif 'Run2017' in filename:
    isMC = False
elif 'Run2016' in filename:
    isMC = False
else:
    isMC = True

# get nEvents
nEvents = 0
for filename in args.inputfiles:

    files = ROOT.TFile(filename)
    n_his = files.Ana.Get('sumWeights')
    nEvents = nEvents + n_his.GetBinContent(1)
    print "filename:",filename


if isMC:
    cross_section = float(args.cross_section)
    lumi = float(args.Lumi)
    weight = cross_section * lumi * 1000.0 / nEvents
else:
    cross_section = 1.0
    weight = 1.0



print 'events weight: '+str(weight)
print 'events : '+str(tchain.GetEntries())


# Output file and any histograms we want
file_out = ROOT.TFile(args.outputfile, 'recreate')

nEvents_total = ROOT.TH1D('nEvents_total', 'nEvents_total', 2, 0, 2)
nEvents_total.SetBinContent(1,nEvents)
h_weight = ROOT.TH1D('Events_weight', 'Events_weight', 2, 0, 2)
h_weight.SetBinContent(1,weight)
h_cross_section = ROOT.TH1D('cross_section', 'cross_section', 2, 0, 2)
h_cross_section.SetBinContent(1,cross_section)

# pass triger
h_n = ROOT.TH1D('nEvents_ntuple', 'nEvents_ntuple', 2, 0, 2)
h_n_trig = ROOT.TH1D('nEvents_trig', 'nEvents_trig', 2, 0, 2)



npho = ROOT.TH1D('npho', 'npho', 10, 0., 10)
nlep = ROOT.TH1D('nlep', 'nlep', 10, 0., 10)

################################################################################################
Z_e_nocut = ROOT.TH1D('Z_e_nocut', 'Z_e_nocut', 100, 0, 500)
Z_mu_nocut = ROOT.TH1D('Z_mu_nocut', 'Z_mu_nocut', 100, 0, 500)

l1_id_lIso = ROOT.TH1D('l1_id_lIso', 'l1_id_lIso', 40, -20., 20.)
Z_e_lIso = ROOT.TH1D('Z_e_lIso', 'Z_e_lIso', 100, 0, 500)
Z_mu_lIso = ROOT.TH1D('Z_mu_lIso', 'Z_mu_lIso', 100, 0, 500)

Z_e_lIso_lTight = ROOT.TH1D('Z_e_lIso_lTight', 'Z_e_lIso_lTight', 100, 0, 500)
Z_mu_lIso_lTight = ROOT.TH1D('Z_mu_lIso_lTight', 'Z_mu_lIso_lTight', 100, 0, 500)

Z_50 = ROOT.TH1D('Z_50', 'Z_50', 100, 0, 500)

################################################################################################
checkRandom = ROOT.TH1D('checkRandom', 'checkRandom', 100, -1., 2.)
################################################################################################




h_n.SetStats(1)
h_n_trig.SetStats(1)

Z_e_nocut.SetStats(1)
Z_mu_nocut.SetStats(1)
Z_e_lIso.SetStats(1)
Z_mu_lIso.SetStats(1)
Z_e_lIso_lTight.SetStats(1)
Z_mu_lIso_lTight.SetStats(1)

Z_50.SetStats(1)

################################################################################################

# photon cut tree
Run = array('l',[0])
LumiSect = array('l',[0])
Event = array('l',[0])

# photon var
pho1eta = array('f',[0.])
pho1Pt = array('f',[0.])
pho1EBEE = array('l',[0])
pho1IetaIeta = array('f',[0.])
pho1NIso = array('f',[0.])

pho1HOE = array('f',[0.])

# MVA vars
pho1e2x2Overe5x5 = array('f',[0.])
pho1covIEtaIPhi = array('f',[0.])
pho1IetaIeta55 = array('f',[0.])
pho1R9 = array('f',[0.])
pho1etaWidth = array('f',[0.])
pho1phiWidth = array('f',[0.])
pho1esEffSigmaRR = array('f',[0.])

pho1PIso = array('f',[0.])
pho1CIso = array('f',[0.])
pho1CIsoWorst = array('f',[0.])

pho1SCEta = array('f',[0.])
pho1SCRawE = array('f',[0.])
pho1esEnergyOverRawE = array('f',[0.])
pho1rho = array('f',[0.])




pho1PIsoOverPt = array('f',[0.])
pho1matchNpho = array('f',[0.])

dR_gl1 = array('f',[0.])
dR_gl2 = array('f',[0.])
dR_gZ = array('f',[0.])
pho1_matchedPdgId = array('f',[0.])
pho1_matchedmomId = array('f',[0.])
pho1_matchedR = array('f',[0.])
l1_id = array('f',[0.])
l2_id = array('f',[0.])
l1_pt = array('f',[0.])
l2_pt = array('f',[0.])
l1_matchedPdgId = array('f',[0.])
l1_matchedMomId = array('f',[0.])
l1_matchedMomMomId = array('f',[0.])
Z_m = array('f',[0.])
gen_Z_m = array('f',[0.])
gen_match_Z_m = array('f',[0.])
l1_GenIndex = array('l',[0])
l2_GenIndex = array('l',[0])


pho2eta = array('f',[0.])
pho2Pt = array('f',[0.])
pho2R9 = array('f',[0.])
pho2IetaIeta = array('f',[0.])
pho2IetaIeta55 = array('f',[0.])
pho2HOE = array('f',[0.])
pho2CIso = array('f',[0.])
pho2NIso = array('f',[0.])
pho2PIso = array('f',[0.])


# photon cut
H_twopho = array('f',[-1.])

event_weight = array('f',[0.])

passedEvents = ROOT.TTree("passedEvents","passedEvents")

################################################################################################
passedEvents.Branch("Run",Run,"Run/L")
passedEvents.Branch("LumiSect",LumiSect,"LumiSect/L")
passedEvents.Branch("Event",Event,"Event/L")


passedEvents.Branch("pho1eta",pho1eta,"pho1eta/F")
passedEvents.Branch("pho1Pt",pho1Pt,"pho1Pt/F")
passedEvents.Branch("pho1EBEE",pho1EBEE,"pho1EBEE/L")
passedEvents.Branch("pho1IetaIeta",pho1IetaIeta,"pho1IetaIeta/F")
passedEvents.Branch("pho1HOE",pho1HOE,"pho1HOE/F")
passedEvents.Branch("pho1NIso",pho1NIso,"pho1NIso/F")
passedEvents.Branch("pho1PIsoOverPt",pho1PIsoOverPt,"pho1PIsoOverPt/F")
passedEvents.Branch("pho1matchNpho",pho1matchNpho,"pho1matchNpho/F")


# MVA vars
passedEvents.Branch("pho1e2x2Overe5x5",pho1e2x2Overe5x5,"pho1e2x2Overe5x5/F")
passedEvents.Branch("pho1covIEtaIPhi",pho1covIEtaIPhi,"pho1covIEtaIPhi/F")
passedEvents.Branch("pho1IetaIeta55",pho1IetaIeta55,"pho1IetaIeta55/F")
passedEvents.Branch("pho1R9",pho1R9,"pho1R9/F")
passedEvents.Branch("pho1etaWidth",pho1etaWidth,"pho1etaWidth/F")
passedEvents.Branch("pho1phiWidth",pho1phiWidth,"pho1phiWidth/F")
passedEvents.Branch("pho1esEffSigmaRR",pho1esEffSigmaRR,"pho1esEffSigmaRR/F")
passedEvents.Branch("pho1PIso",pho1PIso,"pho1PIso/F")
passedEvents.Branch("pho1CIso",pho1CIso,"pho1CIso/F")
passedEvents.Branch("pho1CIsoWorst",pho1CIsoWorst,"pho1CIsoWorst/F")
passedEvents.Branch("pho1SCEta",pho1SCEta,"pho1SCEta/F")
passedEvents.Branch("pho1SCRawE",pho1SCRawE,"pho1SCRawE/F")
passedEvents.Branch("pho1esEnergyOverRawE",pho1esEnergyOverRawE,"pho1esEnergyOverRawE/F")
passedEvents.Branch("pho1rho",pho1rho,"pho1rho/F")


passedEvents.Branch("dR_gl1",dR_gl1,"dR_gl1/F")
passedEvents.Branch("dR_gl2",dR_gl2,"dR_gl2/F")
passedEvents.Branch("dR_gZ",dR_gZ,"dR_gZ/F")
passedEvents.Branch("pho1_matchedPdgId",pho1_matchedPdgId,"pho1_matchedPdgId/F")
passedEvents.Branch("pho1_matchedmomId",pho1_matchedmomId,"pho1_matchedmomId/F")
passedEvents.Branch("pho1_matchedR",pho1_matchedR,"pho1_matchedR/F")
passedEvents.Branch("l1_id",l1_id,"l1_id/F")
passedEvents.Branch("l2_id",l2_id,"l2_id/F")
passedEvents.Branch("l1_pt",l1_pt,"l1_pt/F")
passedEvents.Branch("l2_pt",l2_pt,"l2_pt/F")
passedEvents.Branch("l1_matchedPdgId",l1_matchedPdgId,"l1_matchedPdgId/F")
passedEvents.Branch("l1_matchedMomId",l1_matchedMomId,"l1_matchedMomId/F")
passedEvents.Branch("l1_matchedMomMomId",l1_matchedMomMomId,"l1_matchedMomMomId/F")
passedEvents.Branch("Z_m",Z_m,"Z_m/F")
passedEvents.Branch("gen_Z_m",gen_Z_m,"gen_Z_m/F")
passedEvents.Branch("gen_match_Z_m",gen_match_Z_m,"gen_match_Z_m/F")
passedEvents.Branch("l1_GenIndex",l1_GenIndex,"l1_GenIndex/L")
passedEvents.Branch("l2_GenIndex",l2_GenIndex,"l2_GenIndex/L")

passedEvents.Branch("pho2eta",pho2eta,"pho2eta/F")
passedEvents.Branch("pho2Pt",pho2Pt,"pho2Pt/F")
passedEvents.Branch("pho2R9",pho2R9,"pho2R9/F")
passedEvents.Branch("pho2IetaIeta",pho2IetaIeta,"pho2IetaIeta/F")
passedEvents.Branch("pho2IetaIeta55",pho2IetaIeta55,"pho2IetaIeta55/F")
passedEvents.Branch("pho2HOE",pho2HOE,"pho2HOE/F")
passedEvents.Branch("pho2CIso",pho2CIso,"pho2CIso/F")
passedEvents.Branch("pho2NIso",pho2NIso,"pho2NIso/F")
passedEvents.Branch("pho2PIso",pho2PIso,"pho2PIso/F")




passedEvents.Branch("H_twopho",H_twopho,"H_twopho/F")

passedEvents.Branch("event_weight",event_weight,"event_weight/F")


Nmatch_lep = 0
Nmatch_genpho = 0

#Loop over all the events in the input ntuple
for ievent,event in enumerate(tchain):#, start=650000):
    if ievent > args.maxevents and args.maxevents != -1: break
    if ievent == 3000000: break
    if ievent % 10000 == 0: print 'Processing entry ' + str(ievent)


    # Loop over all the electrons in an event

    # pho parameters
    foundpho1 = False
    foundpho2 = False
    pho1_maxPt = 0.0
    pho2_maxPt = 0.0
    pho1_index = 0
    pho2_index = 0
    pho_passEleVeto = True
    pho_passPreSelection = False


    pho_match = False
    pho_matchIndex = []
    pho_matchIndex_loose = []

    # initialise Z parameters
    Nlep = 0
    lep=0

    Zmass = 91.1876
    dZmass = 9999.0
    n_Zs = 0
    Z_pt = []
    Z_eta = []
    Z_phi = []
    Z_mass = []
    Z_index = 0
    Z_lepindex1 = []
    Z_lepindex2 = []
    foundZ = False
    lep_leadindex = [] # lepindex[0] for leading, lepindex[1] for subleading

    # pass trigger
################################################################################################
    h_n.Fill(event.passedTrig)
    if (not event.passedTrig): continue
    h_n_trig.Fill(event.passedTrig)

    # find all Z candidates
################################################################################################
    Nlep = event.lep_pt.size()
    nlep.Fill(Nlep)


    for i in range(Nlep):

        for j in range(i+1,Nlep):

            if ((event.lep_id[i] + event.lep_id[j]) != 0): continue

            lifsr = ROOT.TLorentzVector()
            ljfsr = ROOT.TLorentzVector()
            lifsr.SetPtEtaPhiM(event.lepFSR_pt[i], event.lepFSR_eta[i], event.lepFSR_phi[i], event.lepFSR_mass[i])
            ljfsr.SetPtEtaPhiM(event.lepFSR_pt[j], event.lepFSR_eta[j], event.lepFSR_phi[j], event.lepFSR_mass[j])

            Z = ROOT.TLorentzVector()
            Z = (lifsr + ljfsr)

            if (Z.M()>0.0):
                n_Zs = n_Zs + 1
                Z_pt.append(Z.Pt())
                Z_eta.append(Z.Eta())
                Z_phi.append(Z.Phi())
                Z_mass.append(Z.M())
                Z_lepindex1.append(i)
                Z_lepindex2.append(j)

                foundZ = True
        # lep j
    # lep i

    if (not foundZ): continue

    # find Z
    for i in range(n_Zs):
        if (abs(Z_mass[i] - Zmass) <= dZmass):
            dZmass = abs(Z_mass[i] - Zmass)
            Z_index = i

    # find Z end

    if (event.lepFSR_pt[Z_lepindex1[Z_index]] >= event.lepFSR_pt[Z_lepindex2[Z_index]]):
        lep_leadindex.append(Z_lepindex1[Z_index])
        lep_leadindex.append(Z_lepindex2[Z_index])
    else:
        lep_leadindex.append(Z_lepindex2[Z_index])
        lep_leadindex.append(Z_lepindex1[Z_index])
################################################################################################



    l1_find = ROOT.TLorentzVector()
    l2_find = ROOT.TLorentzVector()
    Z_find = ROOT.TLorentzVector()

    l1_find.SetPtEtaPhiM(event.lepFSR_pt[lep_leadindex[0]], event.lepFSR_eta[lep_leadindex[0]], event.lepFSR_phi[lep_leadindex[0]], event.lepFSR_mass[lep_leadindex[0]])
    l2_find.SetPtEtaPhiM(event.lepFSR_pt[lep_leadindex[1]], event.lepFSR_eta[lep_leadindex[1]], event.lepFSR_phi[lep_leadindex[1]], event.lepFSR_mass[lep_leadindex[1]])

    Z_find = (l1_find + l2_find)

    if (abs(event.lep_id[lep_leadindex[0]]) == 11):
        Z_e_nocut.Fill(Z_find.M())
    if (abs(event.lep_id[lep_leadindex[0]]) == 13):
        Z_mu_nocut.Fill(Z_find.M())

        # Leptons Cuts
################################################################################################
    # pass lep isolation

    if (abs(event.lep_id[lep_leadindex[0]]) == 11):
        if (event.lep_RelIsoNoFSR[lep_leadindex[0]] > 0.35): continue
        if (event.lep_RelIsoNoFSR[lep_leadindex[1]] > 0.35): continue

        # pt Cut
        if (event.lepFSR_pt[lep_leadindex[0]] <= 25): continue
        if (event.lepFSR_pt[lep_leadindex[1]] <= 15): continue

    if (abs(event.lep_id[lep_leadindex[0]]) == 13):
        if (event.lep_RelIsoNoFSR[lep_leadindex[0]] > 0.35): continue
        if (event.lep_RelIsoNoFSR[lep_leadindex[1]] > 0.35): continue

        # pt Cut
        if (event.lepFSR_pt[lep_leadindex[0]] <= 20): continue
        if (event.lepFSR_pt[lep_leadindex[1]] <= 10): continue


    if (abs(event.lep_id[lep_leadindex[0]]) == 11):
        Z_e_lIso.Fill(Z_find.M())
    if (abs(event.lep_id[lep_leadindex[0]]) == 13):
        Z_mu_lIso.Fill(Z_find.M())

    # lep Tight ID Cut
    if (not (event.lep_tightId[lep_leadindex[0]])): continue
    if (not (event.lep_tightId[lep_leadindex[1]])): continue

    if (abs(event.lep_id[lep_leadindex[0]]) == 11):
        Z_e_lIso_lTight.Fill(Z_find.M())
    if (abs(event.lep_id[lep_leadindex[0]]) == 13):
        Z_mu_lIso_lTight.Fill(Z_find.M())
################################################################################################

    '''
    # m_Z > 50 GeV
################################################################################################
    if (Z_find.M() < 50): continue
    Z_50.Fill(Z_find.M())
################################################################################################


    # Find photon
############################################################


    npho.Fill(event.pho_pt.size())
    if (event.pho_pt.size() < 1): continue


    for i in range(event.pho_pt.size()):
        if (event.pho_hasPixelSeed[i] == 1): continue
        if (event.pho_pt[i] > pho1_maxPt):
            pho1_maxPt = event.pho_pt[i]
            pho1_index = i
            foundpho1 = True

    for j in range(event.pho_pt.size()):
        if (event.pho_hasPixelSeed[j] == 1): continue
        if j == pho1_index: continue
        if (event.pho_pt[j] > pho2_maxPt):
            pho2_maxPt = event.pho_pt[j]
            pho2_index = j
            foundpho2 = True

    if (not (foundpho1 and foundpho2)): continue

    Run[0] = event.Run
    LumiSect[0] = event.LumiSect
    Event[0] = event.Event
    event_weight[0] = weight

################################################################################################

    pho1_find = ROOT.TLorentzVector()
    pho2_find = ROOT.TLorentzVector()

    #pho1_find.SetPtEtaPhiE(event.pho_pt[pho1_index], event.pho_eta[pho1_index], event.pho_phi[pho1_index], event.pho_pt[pho1_index] * np.cosh(event.pho_eta[pho1_index]))
    #pho2_find.SetPtEtaPhiE(event.pho_pt[pho2_index], event.pho_eta[pho2_index], event.pho_phi[pho2_index], event.pho_pt[pho2_index] * np.cosh(event.pho_eta[pho2_index]))

    pho1_find.SetPtEtaPhiM(event.pho_pt[pho1_index], event.pho_eta[pho1_index], event.pho_phi[pho1_index], 0.0)
    pho2_find.SetPtEtaPhiM(event.pho_pt[pho2_index], event.pho_eta[pho2_index], event.pho_phi[pho2_index], 0.0)

    ALP_find = ROOT.TLorentzVector()
    ALP_find = (pho1_find + pho2_find)
#######################################################################################################

    # Higgs Candidates
#######################################################################################################
    H_find = ROOT.TLorentzVector()
    H_find = (Z_find + ALP_find)
#######################################################################################################
    H_twopho[0] = H_find.M()
    # Photon Cuts
#######################################################################################################

    if (((abs(event.pho_eta[pho1_index]) >1.4442) and (abs(event.pho_eta[pho1_index]) < 1.566)) or (abs(event.pho_eta[pho1_index]) >2.5)): continue
    if (((abs(event.pho_eta[pho2_index]) >1.4442) and (abs(event.pho_eta[pho2_index]) < 1.566)) or (abs(event.pho_eta[pho2_index]) >2.5)): continue

    if (event.pho_EleVote[pho1_index] == 0 ): pho_passEleVeto = False
    if (event.pho_EleVote[pho2_index] == 0 ): pho_passEleVeto = False

    if deltaR(pho1_find.Eta(),pho1_find.Phi(),pho2_find.Eta(),pho2_find.Phi()) < 0.3:
        pho1_phoIso = event.pho_photonIso[pho1_index] - pho2_find.Pt()
        pho2_phoIso = event.pho_photonIso[pho2_index] - pho1_find.Pt()
    else:
        pho1_phoIso = event.pho_photonIso[pho1_index]
        pho2_phoIso = event.pho_photonIso[pho2_index]


    if not pho_passEleVeto: continue





    if (abs(event.lep_matchedR03_PdgId[lep_leadindex[0]]) == abs(event.lep_id[lep_leadindex[0]])) and (abs(event.lep_matchedR03_PdgId[lep_leadindex[1]]) == abs(event.lep_id[lep_leadindex[1]])): Nmatch_lep += 1

    for i in range(event.GENpho_pt.size()):
        if (event.GENpho_MomId[i] == 9000005 and event.GENpho_MomMomId[i] == 25):
            if (deltaR(pho1_find.Eta(),pho1_find.Phi(),event.GENlep_pt[i],event.GENlep_eta[i]) < 0.3) or (deltaR(pho2_find.Eta(),pho2_find.Phi(),event.GENlep_pt[i],event.GENlep_eta[i]) < 0.3):
            Nmatch_genpho += 1


    if 'DYJet' in filename:# select Jet fake photon events
        if (event.pho_matchedR03_PdgId[pho1_index] == 22 and event.pho_matchedR[pho1_index] < 0.3) and (event.pho_matchedR03_PdgId[pho2_index] == 22 and event.pho_matchedR[pho2_index] < 0.3): continue
    else:# select true photon from signal sample
        #if (not (event.pho_matchedR03_PdgId[pho1_index] == 22 and event.pho_matchedR[pho1_index] < 0.3)) or (not (event.pho_matchedR03_PdgId[pho2_index] == 22 and event.pho_matchedR[pho2_index] < 0.3)): continue
        if (not (event.pho_matchedR03_PdgId[pho1_index] == 22 and event.pho_matchedR[pho1_index] < 0.3)) and (not (event.pho_matchedR03_PdgId[pho2_index] == 22 and event.pho_matchedR[pho2_index] < 0.3)): continue

    '''
    if not (event.lep_genindex[lep_leadindex[0]]>=0 and event.lep_genindex[lep_leadindex[1]]>=0): continue
    ##################################################
    n_match_pho = 0
    if (event.pho_pt.size() < 1): continue
    #print "match momID size: "+str(event.pho_matchedR03_MomId.size())+", match mommomID size: "+str(event.GENpho_MomMomId.size())+", match PdgID size: " + str(event.pho_matchedR03_PdgId.size())+" "+str(event.pho_matchedR.size())+    ", pt size: "+str(event.pho_pt.size())
    #print "size pt: " + str(event.pho_pt.size()) + " ; size EleVote: " + str(event.pho_EleVote.size())

    for i in range(event.pho_pt.size()):
        if 'DYJet' in filename:
            if event.pho_hasPixelSeed[i] == 1: continue
            if (event.pho_EleVote[i] == 0 ): continue
            if (event.pho_matchedR03_PdgId[i] == 22 and event.pho_matchedR[i] < 0.3) and (abs(event.pho_matchedR03_MomId[i]) < 6 or event.pho_matchedR03_MomId[i] == 21 or event.pho_matchedR03_MomId[i] == 22): continue
            #if (abs(event.pho_matchedR03_PdgId[i]) == 11 and event.pho_matchedR[i] < 0.3) and (event.pho_matchedR03_MomId[i] == 23): continue
            pho_match = True
            pho_matchIndex.append(i)
            n_match_pho += 1

        else:
            if event.pho_hasPixelSeed[i] == 1: continue
            if (event.pho_EleVote[i] == 0 ): continue
            if not (event.pho_matchedR03_PdgId[i] == 22 and event.pho_matchedR[i] < 0.3): continue
            if not (event.pho_matchedR03_MomId[i] == 9000005 ): continue
            pho_match = True
            pho_matchIndex.append(i)
            n_match_pho += 1


    if not pho_match: continue


    # Pre-selection
    for i in range(len(pho_matchIndex)):

        # barrel
        if (abs(event.pho_eta[pho_matchIndex[i]]) < 1.4442):
            if event.pho_R9[pho_matchIndex[i]] > 0.85:
                if event.pho_hadronicOverEm[pho_matchIndex[i]] < 0.08 and event.pho_full5x5_R9[pho_matchIndex[i]] > 0.5: pho_passPreSelection = True
            else:
                if event.pho_hadronicOverEm[pho_matchIndex[i]] < 0.08 and event.pho_full5x5_R9[pho_matchIndex[i]] > 0.5 and event.pho_full5x5_sigmaIetaIeta[pho_matchIndex[i]] < 0.015 and event.pho_trackIso[pho_matchIndex[i]] < 6.0 and event.pho_photonIso[pho_matchIndex[i]] < 4.0: pho_passPreSelection = True

        # endcap
        else:
            if event.pho_R9[pho_matchIndex[i]] > 0.90:
                if event.pho_hadronicOverEm[pho_matchIndex[i]] < 0.08 and event.pho_full5x5_R9[pho_matchIndex[i]] > 0.8: pho_passPreSelection = True
            else:
                if event.pho_hadronicOverEm[pho_matchIndex[i]] < 0.08 and event.pho_full5x5_R9[pho_matchIndex[i]] > 0.8 and event.pho_full5x5_sigmaIetaIeta[pho_matchIndex[i]] < 0.035 and event.pho_trackIso[pho_matchIndex[i]] < 6.0 and event.pho_photonIso[pho_matchIndex[i]] < 4.0: pho_passPreSelection = True

        if 'DYJet' in filename:
            #if pho_passPreSelection:
            pho_matchIndex_loose.append(pho_matchIndex[i])
        else:
            #if pho_passPreSelection:
            pho_matchIndex_loose.append(pho_matchIndex[i])

    # end pre-selection

    if (len(pho_matchIndex_loose) == 0): continue


    if 'DYJet' in filename:
        if len(pho_matchIndex_loose) == 2:
            if event.pho_pt[pho_matchIndex_loose[0]] < event.pho_pt[pho_matchIndex_loose[1]]:
                temp_index = pho_matchIndex_loose[0]
                pho_matchIndex_loose[0] = pho_matchIndex_loose[1]
                pho_matchIndex_loose[1] = temp_index

            #### select photon frome leading and sub-leading photon randomly
            r = random.random()
            checkRandom.Fill(r)
            if r > 0.5:
                pho_index = pho_matchIndex_loose[0]
            else:
                pho_index = pho_matchIndex_loose[1]
        else:
            pho_index = pho_matchIndex_loose[0]

    else:

        if len(pho_matchIndex_loose) != 2: continue
        '''

        if event.pho_pt[pho_matchIndex_loose[0]] < event.pho_pt[pho_matchIndex_loose[1]]:
            temp_index = pho_matchIndex_loose[0]
            pho_matchIndex_loose[0] = pho_matchIndex_loose[1]
            pho_matchIndex_loose[1] = temp_index

        if deltaR(event.pho_eta[pho_matchIndex_loose[0]],event.pho_phi[pho_matchIndex_loose[0]],event.pho_eta[pho_matchIndex_loose[1]],event.pho_phi[pho_matchIndex_loose[1]]) < 0.3:
            pho1_phoIso = event.pho_photonIso[pho_matchIndex_loose[0]] - event.pho_pt[pho_matchIndex_loose[1]]
            pho2_phoIso = event.pho_photonIso[pho_matchIndex_loose[1]] - event.pho_pt[pho_matchIndex_loose[0]]
        else:
            pho1_phoIso = event.pho_photonIso[pho_matchIndex_loose[0]]
            pho2_phoIso = event.pho_photonIso[pho_matchIndex_loose[1]]

        if (abs(event.pho_eta[pho_matchIndex_loose[0]]) < 1.4442):
            if (pho1_phoIso > (2.876 + event.pho_pt[pho_matchIndex[i]]*0.004017)): continue
        # endcap
        else:
            if (pho1_phoIso > (4.162 + event.pho_pt[pho_matchIndex[i]]*0.0037)): continue

        if (abs(event.pho_eta[pho_matchIndex_loose[1]]) < 1.4442):
            if (pho2_phoIso > (2.876 + event.pho_pt[pho_matchIndex[i]]*0.004017)): continue
        # endcap
        else:
            if (pho2_phoIso > (4.162 + event.pho_pt[pho_matchIndex[i]]*0.0037)): continue
        '''
        #### select photon frome leading and sub-leading photon randomly
        r = random.random()
        checkRandom.Fill(r)
        if r > 0.5:
            pho_index = pho_matchIndex_loose[0]
        else:
            pho_index = pho_matchIndex_loose[1]


    ##################################################

    pho1e2x2Overe5x5[0] = event.pho_e2x2[pho_index]/event.pho_e5x5[pho_index]
    pho1covIEtaIPhi[0] = event.pho_covIEtaIPhi[pho_index]
    pho1IetaIeta55[0] = event.pho_full5x5_sigmaIetaIeta[pho_index]
    pho1R9[0] = event.pho_R9[pho_index]
    pho1etaWidth[0] = event.pho_etaWidth[pho_index]
    pho1phiWidth[0] = event.pho_phiWidth[pho_index]
    pho1esEffSigmaRR[0] = event.pho_esEffSigmaRR[pho_index]

    pho1PIso[0] = event.pho_photonIso[pho_index]
    pho1CIso[0] = event.pho_chargedHadronIso[pho_index]
    pho1CIsoWorst[0] = event.pho_chgIsoWrtWorstVtx[pho_index]

    pho1SCEta[0] = event.pho_scEta[pho_index]
    pho1SCRawE[0] = event.pho_SCRawE[pho_index]
    pho1esEnergyOverRawE[0] = event.pho_esEnergyOverRawE[pho_index]
    pho1rho[0] = event.pho_rho[pho_index]



    if (abs(event.pho_eta[pho_index]) < 1.4442):
        pho1EBEE[0] = 1
    if (abs(event.pho_eta[pho_index]) < 2.5 and abs(event.pho_eta[pho_index]) > 1.556):
        pho1EBEE[0] = -1
    pho1eta[0] = event.pho_eta[pho_index]
    pho1Pt[0] = event.pho_pt[pho_index]
    pho1IetaIeta[0] = event.pho_sigmaIetaIeta[pho_index]
    pho1HOE[0] = event.pho_hadronicOverEm[pho_index]
    pho1NIso[0] = event.pho_neutralHadronIso[pho_index]
    pho1PIsoOverPt[0] = event.pho_photonIso[pho_index]/event.pho_pt[pho_index]
    pho1matchNpho[0] = n_match_pho

    dR_gl1[0] = deltaR(event.pho_eta[pho_index], event.pho_phi[pho_index], l1_find.Eta(), l1_find.Phi())
    dR_gl2[0] = deltaR(event.pho_eta[pho_index], event.pho_phi[pho_index], l2_find.Eta(), l2_find.Phi())
    dR_gZ[0] = deltaR(event.pho_eta[pho_index], event.pho_phi[pho_index], Z_find.Eta(), Z_find.Phi())
    pho1_matchedPdgId[0] = event.pho_matchedR03_PdgId[pho_index]
    pho1_matchedmomId[0] = event.pho_matchedR03_MomId[pho_index]
    pho1_matchedR[0] = event.pho_matchedR[pho_index]
    l1_id[0] = event.lep_id[lep_leadindex[0]]
    l2_id[0] = event.lep_id[lep_leadindex[1]]
    l1_pt[0] = event.lepFSR_pt[lep_leadindex[0]]
    l2_pt[0] = event.lepFSR_pt[lep_leadindex[1]]
    l1_matchedPdgId[0] = event.GENlep_id[event.lep_genindex[lep_leadindex[0]]]
    l1_matchedMomId[0] = event.GENlep_MomId[event.lep_genindex[lep_leadindex[0]]]
    l1_matchedMomMomId[0] = event.GENlep_MomMomId[event.lep_genindex[lep_leadindex[0]]]


    gen_l1 = ROOT.TLorentzVector()
    gen_l2 = ROOT.TLorentzVector()

    gen_match_l1 = ROOT.TLorentzVector()
    gen_match_l2 = ROOT.TLorentzVector()
    gen_match_Z = ROOT.TLorentzVector()
    #gen_match_l1.SetPtEtaPhiE(event.lep_matchedR03_pt[lep_leadindex[0]], event.lep_matchedR03_eta[lep_leadindex[0]], event.lep_matchedR03_phi[lep_leadindex[0]], event.lep_matchedR03_E[lep_leadindex[0]])
    #gen_match_l2.SetPtEtaPhiE(event.lep_matchedR03_pt[lep_leadindex[1]], event.lep_matchedR03_eta[lep_leadindex[1]], event.lep_matchedR03_phi[lep_leadindex[1]], event.lep_matchedR03_E[lep_leadindex[1]])
    gen_match_Z = gen_match_l1 + gen_match_l2


    gen_l1.SetPtEtaPhiM(event.GENlep_pt[event.lep_genindex[lep_leadindex[0]]], event.GENlep_eta[event.lep_genindex[lep_leadindex[0]]], event.GENlep_phi[event.lep_genindex[lep_leadindex[0]]], event.GENlep_mass[event.lep_genindex[lep_leadindex[0]]])
    gen_l2.SetPtEtaPhiM(event.GENlep_pt[event.lep_genindex[lep_leadindex[1]]], event.GENlep_eta[event.lep_genindex[lep_leadindex[1]]], event.GENlep_phi[event.lep_genindex[lep_leadindex[1]]], event.GENlep_mass[event.lep_genindex[lep_leadindex[1]]])

    gen_Z = gen_l1 + gen_l2
    gen_Z_m[0] = gen_Z.M()


    Z_m[0] = Z_find.M()
    gen_match_Z_m[0] = gen_match_Z.M()
    l1_GenIndex[0] = event.lep_genindex[lep_leadindex[0]]
    l2_GenIndex[0] = event.lep_genindex[lep_leadindex[1]]


    '''
    pho2eta[0] = event.pho_eta[pho2_index]
    pho2Pt[0] = event.pho_pt[pho2_index]
    pho2R9[0] = event.pho_R9[pho2_index]
    pho2IetaIeta[0] = event.pho_sigmaIetaIeta[pho2_index]
    pho2IetaIeta55[0] = event.pho_full5x5_sigmaIetaIeta[pho2_index]
    pho2HOE[0] = event.pho_hadronicOverEm[pho2_index]
    pho2CIso[0] = event.pho_chargedHadronIso[pho2_index]
    pho2NIso[0] = event.pho_neutralHadronIso[pho2_index]
    pho2PIso[0] = event.pho_photonIso[pho2_index]
    '''
#######################################################################################################

    passedEvents.Fill()










file_out.Write()
file_out.Close()

sw.Stop()
print 'Real time: ' + str(round(sw.RealTime() / 60.0,2)) + ' minutes'
print 'CPU time:  ' + str(round(sw.CpuTime() / 60.0,2)) + ' minutes'