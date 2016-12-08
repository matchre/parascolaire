#!/usr/bin/env python3
import sys
assert sys.version_info >= (3,0)

TR = {
  "Th\\u00e9orie 1":     "theorie1_egal_if.py.html",                  
  "Base 1 : =":         "theorie1_egal_if.py.html",                  
  "Base 2 : if":        "theorie1_egal_if.py.html",                  
  "Th\\u00e9orie 2":     "theorie2_liste_while.py.html",              
  "Base 3 : while":     "theorie2_liste_while.py.html",              
  "Base 4 : list":      "theorie2_liste_while.py.html",              
  "Th\\u00e9orie 3":     "theorie3_fonctions_et_objets.py.html",      
  "Base 5 : Objets":    "theorie3_fonctions_et_objets.py.html",      
  "Base 6 : Fonctions": "theorie3_fonctions_et_objets.py.html",      
  "Exercice 0":         "exercice0_trier_deux_nombres.py.html",      
  "1":                  "exercice1_minute_suivante.py.html",         
  "2":                  "exercice2_minute_suivante_un_print.py.html",
  "3":                  "exercice3_trier_trois_nombres.py.html",     
  "4":                  "exercice4_le_sept_parfait.py.html",         
  "Exercice 5":         "exercice5_max_list.py.html",                
  "6":                  "exercice6_in_list.py.html",                 
  "7":                  "exercice7_filtre_des_grands.py.html",       
  "8":                  "exercice8_somme.py.html",                   
  "9":                  "exercice9_doublons",                        
  "[0] Code minimal":   "pygame0_code_minimal.py.html",              
  "[1] Draw":           "pygame1_dessin.py.html",                    
  "[2] Tick":           "pygame2_tick.py.html",                      
  "[3] Events":         "pygame3_events.py.html",                    
  "[4] Animation":      "pygame4_animations.py.html",                
  "[5] Clavier-Souris": "pygame5_clavier_souris_events.py.html",     
  "(Events)":           "pygame5_clavier_souris_events.py.html",     
  "[6] Clavier-Souris": "pygame6_clavier_souris_state.py.html",      
  "(\\u00c9tats)":       "pygame6_clavier_souris_state.py.html",      
  "[7] Images":         "pygame7_images.py.html",                    
  "[8] Texte":          "pygame8_texte.py.html",                     
  "Projet":             "projets.html"                               
}                             

with open('flow.svg') as f:
    A = f.read()

for a,b in list(TR.items()):
    A = A.replace('>' + a + '<', '>' + "<a xlink:href=\"{1}\">{0}</a>".format(a,b) + '<')

with open('flow-translated.svg', 'w') as f:
    f.write(A)