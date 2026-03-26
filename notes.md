# Axes d'amélioration sans éclater en plusieurs fichiers

Sur le nommage : quelques incohérences comme TR_Titre_Argnet (faute de frappe), dic_Total_Par_Clasee (double faute). Pour les fonctions, tu mélanges français et anglais (perf_globale, Evolution_totale_classe_stackplot), mieux vaut choisir une langue.

Sur les magic values : les dates "2025-01-26", "2025-04-15" dans performance_ligne_bar sont codées en dur. Les sortir en constantes ou paramètres rendrait la fonction réutilisable.

Sur la signature des fonctions : le pattern (ax, nb=0) est un peu fragile — passer ax[nb] directement en paramètre serait plus propre et plus testable.
Sur le code dupliqué : perf_par_classe et perf_globale partagent la même logique (valeur / invest - 1) * 100, tu pourrais avoir une fonction calcul_perf(valeur, invest) commune.

# Bordel qui étais dans keep

premier étape :
manière simple d'import mes données à Python et génère un
pie chart (étape 2 : interactif, qunqd je clique sur une partie ca rentre dans le détail OU PLUS SIMPLE faire un pie chart par type d'actif et un autre par ligne) pour voir répartition invest
graphique en bar pour voir l'évolution de chaque partie de l'invest (par ligne et par produit (plutot pas type d'actif)) plutot en courbe superoposé en fait, c'est plus logique
(gaphique à courbe pour voir l'évolution, un peu redondant avec le précédent mais on peut ajouter des prévisions et des courbes de tendances)
(aller scrapper les infos de mon etf pour MaJ tout seul le truc, mais étape 2)
https://docs.google.com/spreadsheets/d/1ISOOIaM-vlhgjB6OkcOT_eGsYnwT1RY6ljlG1NzGkHU/edit?gid=190570130#gid=190570130
faire deux graphs en bar : pour le rendement de chaque ligne et par produit (on peut y inclure la volatilité en incertitude avec un trait !)
Faire en sorte que tout s'édite sur le meme graphique

Bien diviser le code !
Une partie visualisation ! (Comme ça je pourrai réutiliser si je change de support) 
Une partie conversion vers le bon dataframe ! 

Dans une partie plus longue encore pk pas configuré des alertes si certaines constantes ne sont pas bonnes ! Si certains trucs sont a faire !

Pk pas connectée sur une API WhatsApp ou telegerzm ou autre si avant jrv a connecter e direct mes tableaux avec des donnes en ligne 

Refaire avec plotly et pas matplotlib pour pouvoir Scroll dans les dates !
En fait franchement mon dashboard est déja très clean, il faut plus que je clean la forme, pour bien mettre les labels, mettre des couleurs jolies.
Ajouter la Valeur net au jour, et la date du jour en gros surtout !
Faire que je sauvegarde tout au meme endroit ! Faire un seul dossier dans Drive, avec un main fichier, stocker les anciennes versions ailleurs et faire un historique de mes dashboards
Une fois que j'aurais fais tout ca pk pas mettre sur github. Mais ca suppose de changer les valeurs à des trucs arbitraires. En vrai c simple, tu divise tout par le net worth du début pour avoir des valeurs proche de 1 etc

En fait tout simplement clean qq graphique utile. Faire deux dashboards. Ou alors bien séparé un pour l'évolution et un autre pour l'état actuel ! 

La mesure du 13 juin 2025 semble, bizarre, voir fausse ?

En gros : 
1. Clean les plots pour que ca soit beau et interactif dans un html scrolable
1.1 Faire le graphique bilan en bien, juste avec les benefs ! (valeur actuel - investi dedans). (Le goaaaal ca serait de faire un truc avec menue déroulant (mais la c'est un vrai app web) pour séléctionner chaque ligne du protefeuille pour avoir 3 corubes sur le meme graphs, perf etf, valeur position, benef fait. Mais ca c'est pour plus tard)
2. Inclure données marchées comme MSCI World, et le mieux connecter mes ETFs pour voir leur perf en temps réél

# Boredel qui étais dans notes apprentissage : Feature à rajouter !
## notes à la voler pas trié
Sur [le forum finary](https://community.finary.com/t/remplacer-le-msci-world-par-un-fond-plus-performant/32632) le premier commentaire a fait un graphique qui me fait simplement réver !! (courbes qui sépare : -montant investit -performance du fond -gain effectif) J4avais jamais vue et ptn c'est exactement ce qu'il faut damn 

1. Calculer la perf moyenne de tous mes invest dans performance ligne bar (vrm pas dur mais prends 15min et la faut je passe a autre chose)
Faire une V2 si je rajoute des trucs, histoire de pas tout baise
1. Rendement par ligne (historique, sur 6mois, 1an etc) et rendement total ! INTERESSANT
2. Rentrer dans le détail du PEA et PEA PME
3. Améliorer la disposition, l'élégance du graphique !
4. Faire des projections de patrimoine ! Entre 4 et 8% par an
4. Mettre le Net Worth plus en évidence !
5. Import vers HTML pour ouvrir dans un navigateur pk pas

je peux ameliiorer la grille avec https://matplotlib.org/stable/gallery/subplots_axes_and_figures/gridspec_multicolumn.html#sphx-glr-gallery-subplots-axes-and-figures-gridspec-multicolumn-py
En profitere pour mettre titre au dashboard incluant la date la plus récente

le pie chart, ajouter valeur total au milieu et améliorer design
stackplot en dessous, ajouter vlaurs
pk pas ajouter une prévision de performance
et un graph fait a la mano pour les perrfs des livrets et FE mais bonnn pas obligé

Ne pas essayer de connecter les fonds en ligne, complexification inutile a mon gout ! Il va y avoir des MaJ, moi je vais j=changer de fond tout ca trop compliqué i think

# Le dashboard idéal
Un mondrian de toutes les lignes !

# les noms 
Conventions pour pas s'embrouiller

classe actifs (actions, monétaire)
Courtier (TR, HB)
support (AV, PEA)
ligne (MSCI World)

# Bonus
Alleluia ! Ca marche !!
Mon premier projet Python qui a un interet, c'est cool

Mais à améliorer, il y a plein de trucs a faire pour que ca soit vrm le prime
