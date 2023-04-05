#!/usr/bin env python3
# -*- coding: utf-8 -*-

"""
Creator : MOUIGNI Hadji

Programme réalisant l'aggrégation des différents flux RSS et générant une page HTML présentant l'aggrégation de ces flux.
"""
#import des modules nécessaires pour l'aggrégateur
import feedparser 
import time 
import yaml 



def charge_urls(liste_url):
     """
     Programme qui récupère  n flux RSS à partir de leurs
     urls passées en ligne de commande.
     """
     #création d'une liste vide qui va contenir les docs RSS
     liste = []
     #on parcours chaque url passée en paramètre
     for url in liste_url:
          #décodage du flux
          feed = feedparser.parse(url)
          #vérification de la validité de l'url
          if feed["bozo"]== False :
               liste.append(feed)
          else :
               liste.append(None)
     
     return liste


def fusion_flux(liste_url,liste_flux):
     """
     Programme qui produit une liste unique d'événements
     contenant les événements de n flux
     """
     #liste qui va contenir des dictionnaires
     #qui von eux-même contenir le contenu des évènements
     liste = []
     c = 0
     #on parcours la liste renvoyée par la fonction charge_urls
     for i in liste_flux:

          #traite seulement les url valides
          if i != None:
               #on récupere les informations dont on a besoin pour chaque flux
               for entry in i['entries']:
                    titre = entry['title']
                    categorie = entry['tags'][0]['term']
                    url = liste_url[c]
                    serveur = url[7:15]
                    date_publi = entry['published']
                    lien = entry['link']
                    description = entry['summary']
                    guid = entry['guid']

                    #liste qui recense les infos des chaque flux           
                    liste.append({'titre':titre,'categorie':categorie,'serveur':serveur,'date_publi':date_publi,'lien':lien,'description':description,'guid':guid})
          c+=1
     print(liste)
     return liste
     



def genere_html(liste_evenements, chemin_html):
     """
     Programme qui produit une page html qui va contenir
     les flux mais seulement leurs infos pricipales (fonction fusion_flux)
     + on y applique une feuille CSS pour une présentation claire et sobre
     """

     #Création de la page HTML en respectant la 
     #syntaxe nécessaire
     with open(chemin_html, "w+") as page:
          #Partie commune
          page.write("<!DOCTYPE html> \n")
          page.write("<html lang='en'> \n")
          page.write("\t <head> \n")
          page.write("\t\t <meta charset='utf-8'> \n")
          page.write("\t\t <meta name='viewport' content='width=device-width, initial-scale=1'>\n")
          page.write("\t\t <title>Events log</title> \n")
          page.write("\t\t <link rel='stylesheet' href='style.css' type='text/css'/> \n")
          page.write("\t </head> \n")
          page.write("\t <body> \n")
          page.write("\t\t <article> \n")
          page.write("\t\t\t <header> \n")
          page.write("\t\t\t\t <h1>Events log</h1> \n")
          page.write("\t\t\t </header> \n")
          page.write("\t\t\t<p>"+ time.strftime("%a, %d %b %Y %H:%M:%S")+"</p> \n")
          
          #Pour chaque évènement on génère une partie de page 
          #qui recensera toutes les infos
          for i in liste_evenements:
               
               page.write("\t\t\t <article> \n")
               page.write("\t\t\t\t <header> \n")
               page.write("\t\t\t\t\t<h2>"+i['titre']+"\n")
               page.write("\t\t\t\t </header> \n")
               page.write("\t\t\t\t <p>From : "+ i['serveur']+"</p>\n")
               page.write("\t\t\t\t <p>Date : "+ i['date_publi']+"</p>\n")
               page.write("\t\t\t\t <p class=\""+ i['categorie']+"\">Category : "+ i['categorie']+"</p>\n")
               page.write("\t\t\t\t <p>GUID : "+ i['guid']+"</p>\n")
               page.write("\t\t\t\t <p><a href='"+i['lien']+"'>"+i['lien']+"</a></p>\n")
               page.write("\t\t\t\t <p>Description : "+ i['description']+"</p>\n")
               page.write("\t\t\t </article> \n")

          #Fin de la page HTML
          page.write("\t\t </article> \n")     
          page.write("\t </body> \n")
          page.write("</html> \n")

               
     return "ok"
     


def yaml_conf():
     """
     Fonction qui va seulement ouvrir le fichier conf.yaml 
     et le charger afin de pouvoir utiliser son contenu
     """
     with open("test.yaml", "r") as conf:
        conf = yaml.safe_load(conf)

     return conf

def main():
     """
     Dans le main(), on va initaliser les différents paramètres qui permettent
     le fonctionnement des fonctions et enfin appeler la fonction qui gènère 
     la page HTML  
     """    
     a = yaml_conf()
     #liste_url
     li = a['sources']
     #chemin_html
     dest = a['destination']
     #nom du fichier.rss
     rss = a['rss-name']
     #différentes fonctions stockée dans des variables
     #pour simplifier la commande finale
     charge = charge_urls(li)
     fusion = fusion_flux(li,charge)
     genere = genere_html(fusion,dest)
     for i in range (0,len(li)):

          li[i] = li[i]+rss
     print(genere_html(fusion_flux(li, charge_urls(li)),a['destination']))
     
if __name__ == '__main__':
    main()

