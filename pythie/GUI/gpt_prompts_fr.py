summary_template = """
Fournissez un résumé d'environ deux phrases pour la critique suivante de {product}:

{transcript_chunk}

Résumé:
"""

video_likes_dislikes_prompt = """
A partir d'un paragraphe sur une critique de produit, extrayez les points forts et les points faibles du produit.
Les points forts et faibles extraites doivent être présentées sous forme de puces.
Si le paragraphe ne mentionne aucun avis défavorable, la section des points faibles doit être vide.
Si le paragraphe ne mentionne pas de points forts, la section des appréciations doit être vide.

Voici un exemple où le produit est la Mazda 2:
```
Extrayez les informations importantes du résumé suivant de Mazda 2 sous forme de puces:

Paragraphe:
La Mazda 2 est une voiture compacte qui impressionne par son design élégant, sa tenue de route sportive et ses performances efficaces. Avec ses lignes audacieuses et sa calandre agressive, la Mazda 2 dégage une impression de dynamisme et de sophistication. L'intérieur est bien conçu, avec des matériaux de haute qualité et des technologies modernes, créant un habitacle confortable et élégant. La maniabilité de la voiture et la réactivité de la direction en font une voiture agréable à conduire, en particulier dans les environnements urbains où sa taille compacte est mise en valeur. La Mazda 2 offre également un rendement énergétique impressionnant, ce qui en fait un choix pratique pour les trajets quotidiens. Bien qu'elle n'offre pas les places arrière ou la capacité de chargement les plus spacieuses de sa catégorie, la Mazda 2 compense par son agrément de conduite général et son souci du détail. Dans l'ensemble, la Mazda 2 est une option convaincante pour ceux qui recherchent une petite voiture alliant style, agilité et efficacité énergétique.

Mazda 2 points forts et faibles:
Points forts:
- Design épuré avec des lignes audacieuses et une calandre agressive
- Tenue de route sportive et maniabilité agile
- Intérieur confortable et élégant avec des matériaux de haute qualité
- Caractéristiques technologiques modernes
- Efficacité énergétique impressionnante

Points faibles:
- Places arrière et capacité de chargement limitées par rapport à certains concurrents.
```

Extrayez les informations importantes du résumé suivant de {product} sous forme de puces:

Paragraphe:
{combined_chunks_summary}

{product} points forts et faibles:
"""

topics_generation_prompt = """
A partir d'un paragraphe sur une critique de produit, votre tâche est d'extraire les sujets généraux discutés sur le produit.
Les sujets doivent être d'un ou deux mots maximum.
Vous pouvez générer 6 sujets au maximum.
Les sujets doivent être aussi généraux que possible.
Votre réponse doit être une liste de sujets, formatée comme une liste à puces.

Voici un exemple où le produit est Mazda 2:
```
Fournissez une liste des sujets généraux discutés à propos de la Mazda 2 en vous basant sur le texte suivant.
Les sujets doivent comporter un ou deux mots.
Vous pouvez générer 6 sujets au maximum.

Texte :
La Mazda 2 est un véhicule fiable et efficace. Elle offre une bonne économie de carburant et possède un design petit et agile. La voiture se manie bien et offre une expérience de conduite souple. L'intérieur est confortable et bien conçu. Elle dispose d'un système d'infodivertissement convivial. La Mazda 2 possède des caractéristiques de sécurité avancées pour sa catégorie. Le design extérieur de la voiture est élégant et moderne. Elle offre un bon rapport qualité-prix dans sa gamme de prix. La Mazda 2 a la réputation d'être fiable et durable. Son moteur est réactif et efficace. La Mazda 2 dispose d'un espace de chargement limité, surtout par rapport aux véhicules plus grands. Elle peut se sentir sous-motorisée sur autoroute ou lors de dépassements. La banquette arrière est un peu exiguë pour les passagers de grande taille. Le système d'infodivertissement peut manquer de certaines fonctions avancées que l'on trouve chez les concurrents. La qualité de conduite peut être légèrement ferme sur les routes accidentées. L'équipement de série de la Mazda 2 n'est pas aussi généreux que celui de ses concurrentes. Elle ne dispose pas des dernières technologies d'aide à la conduite disponibles sur les modèles plus haut de gamme. Le bruit du moteur peut être perceptible lors de fortes accélérations. La Mazda 2 n'est pas disponible avec la transmission intégrale. Certains clients peuvent trouver la visibilité arrière limitée.

Liste des sujets généraux (6 maximum):
- Design
- L'intérieur
- Sécurité
- Intérieur
- Technologie
- Performances
```

Fournissez une liste des sujets généraux discutés à propos de {product} en vous basant sur le texte suivant.
Les sujets doivent comporter un ou deux mots.
Vous pouvez générer 6 sujets au maximum.

Texte :
{likes_dislikes_bullet_points}

Liste de sujets généraux (6 au maximum):
"""

assign_specific_topics = """
À partir d'une liste de points forts et faibles concernant un produit et d'une liste de sujets, attribuez chaque point fort et chaque point faible à un ou plusieurs sujets.
Les sujets attribués doivent figurer dans la liste de sujets fournie.

Voici un exemple où le produit est Mazda 2:
```
Mazda 2 points forts et faibles:
Points forts:
- La Mazda 2 est un véhicule fiable et efficace.
- Elle offre une bonne économie de carburant et a un design petit et agile.
- La voiture se manie bien et offre une expérience de conduite souple.
- L'intérieur est confortable et bien conçu.
- Elle dispose d'un système d'infodivertissement convivial.
- La Mazda 2 possède des caractéristiques de sécurité avancées pour sa catégorie.
- Le design extérieur de la voiture est élégant et moderne.
- Elle offre un bon rapport qualité-prix dans sa gamme de prix.
- La Mazda 2 a la réputation d'être fiable et durable.
- Elle dispose d'un moteur réactif et efficace.

Points faibles:
- La Mazda 2 dispose d'un espace de chargement limité, surtout par rapport aux véhicules plus grands.
- Elle peut sembler sous-motrice sur autoroute ou lors de dépassements.
- La banquette arrière est un peu exiguë pour les passagers de grande taille.
- Le système d'infodivertissement peut manquer de certaines fonctions avancées que l'on trouve chez les concurrents.
- La qualité de conduite peut être légèrement ferme sur les routes accidentées.
- L'équipement de série de la Mazda 2 n'est pas aussi généreux que celui de ses concurrentes.
- Elle ne dispose pas des dernières technologies d'aide à la conduite disponibles sur les modèles plus haut de gamme.
- Le bruit du moteur peut être perceptible lors de fortes accélérations.
- La Mazda 2 n'est pas disponible avec la transmission intégrale.
- Certains clients peuvent trouver la visibilité arrière limitée.

Attribuez à chaque points forts et faibles de Mazda 2, un ou plusieurs sujets de la liste suivante : 
- Économie de carburant
- Sécurité
- Infotainment
- Intérieur
- Prix
- Moteur
- Conduite
- Extérieur
- Autre

Sujets attribués:
Points forts:
- La Mazda 2 est un véhicule fiable et efficace. (Autre)
- Elle offre une bonne économie de carburant et a un design petit et agile. (Économie de carburant)
- La voiture se manie bien et offre une expérience de conduite souple. (Conduite)
- L'intérieur est confortable et bien conçu. (Intérieur)
- Elle dispose d'un système d'infodivertissement convivial. (Infotainment)
- La Mazda 2 possède des caractéristiques de sécurité avancées pour sa catégorie. (Sécurité)
- Le design extérieur de la voiture est élégant et moderne. (Extérieur)
- Elle offre un bon rapport qualité-prix dans sa gamme de prix. (Prix)
- La Mazda 2 a la réputation d'être fiable et durable. (Autre)
- Elle dispose d'un moteur réactif et efficace. (Moteur, économie de carburant)

Points faibles:
- La Mazda 2 dispose d'un espace de chargement limité, surtout par rapport aux véhicules plus grands. (Intérieur)
- Elle peut sembler sous-motrice sur autoroute ou lors de dépassements. (Moteur)
- La banquette arrière est un peu exiguë pour les passagers de grande taille. (Intérieur)
- Le système d'infodivertissement peut manquer de certaines fonctions avancées que l'on trouve chez les concurrents. (Infotainment)
- La qualité de conduite peut être légèrement ferme sur les routes accidentées. (Conduite)
- L'équipement de série de la Mazda 2 n'est pas aussi généreux que celui de ses concurrentes. (Autres)
- Elle ne dispose pas des dernières technologies d'aide à la conduite disponibles sur les modèles plus haut de gamme. (Conduite)
- Le bruit du moteur peut être perceptible lors de fortes accélérations. (Moteur)
- La Mazda 2 n'est pas disponible avec la transmission intégrale. (Conduite)
- Certains clients peuvent trouver la visibilité arrière limitée. (Conduite)
```

{product} points forts et faibles:
{combined_likes_dislikes}

Attribuez à chaque points forts et faibles de {product}, un ou plusieurs sujets de la liste suivante : 
{topics_str}

Sujets attribués:
"""

condense_points = """
À partir d'une liste de puces, votre tâche consiste à détecter et à fusionner les puces qui représentent les mêmes idées.
Lors de la fusion des puces, vous devez indiquer le nombre de puces fusionnées à l'origine.
Ainsi, à la fin, le nombre total attribué aux nouvelles puces doit être égal au nombre de puces d'origine.

Voici un exemple où le produit est écran HP :
```
Détectez et fusionnez les puces qui représentent les mêmes idées sur le Display de écran HP. Pour chaque nouvelle puce, indiquez le nombre de puces fusionnées d'origine. Le nombre total attribué aux nouvelles puces doit être égal au nombre de puces originales.
Puces:
- Couleurs vives et précises.
- Haute résolution.
- L'écran dispose d'une large gamme de couleurs, ce qui permet une reproduction précise des couleurs.
- Revêtement antireflet.
- Résolution permettant de capturer les détails avec précision.

Nouvelles puces:
- L'écran dispose d'une large gamme de couleurs, ce qui permet une reproduction vibrante et précise des couleurs (2).
- Haute résolution permettant de capturer les détails avec précision. (2)
- Revêtement antireflet. (1)
Nombre de points originaux = 5
Nombre total de nouveaux puces = 2 + 2 + 1 = 5
```

Voici un exemple où le produit est Mazda 2 :
```
Détectez et fusionnez les puces qui représentent les mêmes idées sur le Moteur de Mazda 2. Pour chaque nouvelle puce, indiquez le nombre de puces fusionnées à l'origine. Le nombre total de nouvelles puces doit être égal au nombre de puces d'origine.
Puces:
- Le niveau de bruit produit par le moteur peut être assez élevé.
- Il peut donner l'impression d'être sous-motorisé sur autoroute ou lors des dépassements.
- Le bruit du moteur peut être perceptible en cas de forte accélération.
- Le moteur peut être très bruyant. 

Nouvelles puces:
- Le moteur peut être bruyant, surtout en cas de forte accélération. (3)
- Il peut sembler sous-motorisé sur autoroute ou lors des dépassements. (1)
Nombre de puces originales = 4
Nombre total de nouveaux puces = 3 + 1 = 4
```

Détectez et fusionnez les puces qui représentent les mêmes idées sur le {topic} de {product}. Pour chaque nouvelle puce, indiquez le nombre de puces fusionnées à l'origine. Le nombre total de nouvelles puces doit être égal au nombre de puces d'origine.
{related_points}

Nouvelles puces:
"""

global_summary = """
Fournissez un résumé de la liste suivante des points forts et faibles de {product}. Le résumé doit consister en deux paragraphes, un pour les points forts et l'autre pour les points faibles, de 2 à 3 phrases chacun.
{local_summary}

Résumé:
"""



########### Competitors ###########
chunk_competitors_prompt = """
A partir d'un paragraphe, votre tâche consiste à extraire les informations de comparaison mentionnées dans ce paragraphe, si elles existent.
Si aucune information comparative n'est mentionnée dans le paragraphe, vous devez répondre par "Aucune information comparative trouvée".
Sur la base du paragraphe ci-dessous, extrayez les informations de comparaison entre {product} et d'autres produits.
Les autres produits doivent être des produits spécifiques et pas seulement des marques.

Paragraphe:
{transcript_chunk}

Sur la base du paragraphe ci-dessus, extrayez les informations de comparaison entre {product} et d'autres produits:
"""

competitors_summary_prompt = """
A partir d'informations extraites de vidéos de critique sur YouTube, votre tâche consiste à fournir un résumé d'environ trois phrases.
Le résumé doit être axé sur la comparaison des produits.

Voici un exemple où le produit est Mazda 2 :
```
Paragraphe :
La Mazda 2 est une voiture compacte qui tient la route lorsqu'on la compare à ses rivales, la Ford Focus et la Fiat 500. Bien que ces trois voitures appartiennent au même segment, la Mazda 2 se distingue par ses performances dynamiques et son comportement agile. Avec un design sportif et moderne, elle dégage une présence confiante sur la route. En termes d'espace intérieur, la Mazda 2 offre un habitacle confortable et bien conçu, avec suffisamment d'espace pour la tête et les jambes des passagers. En ce qui concerne l'efficacité énergétique, la Mazda 2 excelle grâce à ses options de moteurs efficaces, permettant une conduite économique et respectueuse de l'environnement. Alors que la Ford Focus et la Fiat 500 ont leurs propres charmes, la Mazda 2 trouve un équilibre entre praticité et plaisir, ce qui en fait un choix attrayant pour ceux qui recherchent une expérience de conduite vivante dans un format compact.

Résumé axé sur la comparaison du Mazda 2 avec d'autres produits :
Par rapport à ses rivales, la Ford Focus et la Fiat 500, la Mazda 2 se distingue par ses performances vives, son comportement agile et son design sportif. Elle offre un habitacle confortable et bien conçu avec suffisamment d'espace pour les passagers, et sa consommation de carburant est impressionnante avec des options de moteur efficaces. Alors que la Ford Focus et la Fiat 500 ont leurs propres caractéristiques, la Mazda 2 trouve un équilibre entre praticité et plaisir, ce qui en fait un choix attrayant pour ceux qui recherchent une expérience de conduite agréable dans une voiture compacte.
```

Paragraphe :
{concat_competitors_info}

Résumé axé sur la comparaison du {product} avec d'autres produits :
"""

competitors_products_detection_prompt = """
A partir d'un paragraphe, votre tâche consiste à détecter les produits (autres que le produit principal) mentionnés dans ce paragraphe, s'ils existent.
Vous pouvez détecter 2 produits au maximum (s'il y en a d'autres, ne les incluez pas dans votre réponse).

Voici un exemple où le produit principal est Mazda 2 :
```
A partir d'un paragraphe comparant Mazda 2 à d'autres produits. Détectez les produits mentionnés dans le paragraphe. Votre réponse doit être présentée sous forme de puces.
N'incluez pas Mazda 2 dans les produits détectés.

Paragraphe :
Par rapport à ses rivales, la Ford Focus et la Fiat 500, la Mazda 2 se distingue par ses performances dynamiques, son comportement agile et son design sportif. Elle offre un habitacle confortable et bien conçu avec suffisamment d'espace pour les passagers, et sa consommation de carburant est impressionnante grâce à des options de moteur efficaces. Alors que la Ford Focus et la Fiat 500 ont leurs propres caractéristiques, la Mazda 2 trouve un équilibre entre praticité et plaisir, ce qui en fait un choix attrayant pour ceux qui recherchent une expérience de conduite agréable dans une voiture compacte.

Produits détectés (pas les marques) :
- Ford Focus
- Fiat 500
```

A partir d'un paragraphe comparant {product} à d'autres produits.Détectez les produits mentionnés dans le paragraphe. Votre réponse doit être présentée sous forme de puces.
N'incluez pas {product} dans les produits détectés.

Paragraphe :
{concat_competitors_info}

Produits détectés (pas les marques) :
"""

comparison_prompt = """
A partir de deux paragraphes décrivant chacun les caractéristiques d'un produit, vous devez comparer les deux produits en vous basant sur les informations fournies.

Paragraphe de {main_product} :
{combined_chunks_summary_main_product}

Paragraphe de {product}:
{combined_chunks_summary_product}

Comparez {main_product} à {product} sur la base des informations fournies :
"""


########### Topics rating ###########
rate_topics_prompt = """
À partir d'une liste de points forts et faibles d'un produit et d'une liste de sujets, votre tâche consiste à attribuer une note comprise entre 0 et 10 à chacun des sujets proposés.
La note doit être basée sur les points forts et faibles attribuées à chaque sujet.

Voici un exemple où le produit est Mazda 2 :
```
Points forts et faibles de Mazda 2 :
Points forts:
- La Mazda 2 est un véhicule fiable et efficace. (Autre)
- Elle offre une bonne économie de carburant et a un design petit et agile. (Économie de carburant)
- La voiture se manie bien et offre une expérience de conduite souple. (Conduite)
- L'intérieur est confortable et bien conçu. (Intérieur)
- Elle dispose d'un système d'infodivertissement convivial. (Infotainment)
- La Mazda 2 possède des caractéristiques de sécurité avancées pour sa catégorie. (Sécurité)
- Le design extérieur de la voiture est élégant et moderne. (Extérieur)
- Elle offre un bon rapport qualité-prix dans sa gamme de prix. (Prix)
- La Mazda 2 a la réputation d'être fiable et durable. (Autre)
- Elle dispose d'un moteur réactif et efficace. (Moteur, économie de carburant)

Points faibles:
- La Mazda 2 dispose d'un espace de chargement limité, surtout par rapport aux véhicules plus grands. (Intérieur)
- Elle peut sembler sous-motrice sur autoroute ou lors de dépassements. (Moteur)
- La banquette arrière est un peu exiguë pour les passagers de grande taille. (Intérieur)
- Le système d'infodivertissement peut manquer de certaines fonctions avancées que l'on trouve chez les concurrents. (Infotainment)
- La qualité de conduite peut être légèrement ferme sur les routes accidentées. (Conduite)
- L'équipement de série de la Mazda 2 n'est pas aussi généreux que celui de ses concurrentes. (Autres)
- Elle ne dispose pas des dernières technologies d'aide à la conduite disponibles sur les modèles plus haut de gamme. (Conduite)
- Le bruit du moteur peut être perceptible lors de fortes accélérations. (Moteur)
- La Mazda 2 n'est pas disponible avec la transmission intégrale. (Conduite)
- Certains clients peuvent trouver la visibilité arrière limitée. (Conduite)

En vous basant sur les points forts et faibles de Mazda 2, attribuez une note de 0 à 10 à chacun des sujets suivants :
- Économie de carburant
- Sécurité
- Infotainment
- Intérieur
- Prix
- Moteur

Notes des sujets :
- Économie de carburant: 9/10
- Sécurité: 8/10
- Infotainment: 6/10
- Intérieur: 6/10
- Prix: 8/10
- Moteur: 7/10
```

Points forts et faibles de {product} :
{assigned_topics_list}

En vous basant sur les points forts et faibles de {product}, attribuez une note de 0 à 10 à chacun des sujets suivants :
{topics_list}

Notes des sujets :
"""


questions_generation_prompt = """
Remplace les "REMPLIR ICI" dans les questions incomplètes ci-dessous par les mots appropriés pour créer de nouvelles questions. Pour le contexte, utilisez le contexte ci-dessous.

Contexte :
La Mazda 2 est un véhicule fiable et efficace. Elle offre une bonne économie de carburant et se caractérise par sa petite taille et son agilité. La voiture se manie bien et offre une conduite souple. L'intérieur est confortable et bien conçu. Elle dispose d'un système d'infodivertissement convivial. La Mazda 2 possède des caractéristiques de sécurité avancées pour sa catégorie. Le design extérieur de la voiture est élégant et moderne. Elle offre un bon rapport qualité-prix dans sa gamme de prix. La Mazda 2 a la réputation d'être fiable et durable. Son moteur est réactif et efficace. La Mazda 2 dispose d'un espace de chargement limité, surtout par rapport aux véhicules plus grands. Elle peut se sentir sous-motorisée sur autoroute ou lors de dépassements. La banquette arrière est un peu exiguë pour les passagers de grande taille. Le système d'infodivertissement peut manquer de certaines fonctions avancées que l'on trouve chez les concurrents. La qualité de conduite peut être légèrement ferme sur les routes accidentées. L'équipement de série de la Mazda 2 n'est pas aussi généreux que celui de ses concurrentes. Elle ne dispose pas des dernières technologies d'aide à la conduite disponibles sur les modèles plus haut de gamme. Le bruit du moteur peut être perceptible lors de fortes accélérations. La Mazda 2 n'est pas disponible avec la transmission intégrale. Certains clients peuvent trouver la visibilité arrière limitée.

Questions incomplètes :
Q1 : Génère moi un paragraphe de blog SEO, qui présente REMPLIR ICI de Mazda 2.
Q2 : Génère moi 3 ad-copies présentant REMPLIR ICI de Mazda 2, avec des titres et des corps, et inclure des mots-clés à longue traîne sur lesquels je peux enchérir.
Q3 : Crée moi un script publicitaire sur Mazda 2 destiné à REMPLIR ICI.

Nouvelles questions :
Q1 : Génère moi un paragraphe de blog SEO, qui présente la technologie du système d'infodivertissement de la Mazda 2.
Q2 : Génère moi 3 ad-copies présentant la sécurité de Mazda 2, avec des titres et des corps, et inclure des mots-clés à longue traîne sur lesquels je peux enchérir.
Q3 : Crée moi un script publicitaire sur la Mazda 2 destiné aux clients à budget limité.

Remplace les "REMPLIR ICI" dans les questions incomplètes ci-dessous par les mots appropriés pour créer de nouvelles questions. Pour le contexte, utilisez le contexte ci-dessous.

Contexte :
{global_summary}

Questions incomplètes :
Q1 : Génère moi un paragraphe de blog SEO, qui présente REMPLIR ICI de {product}.
Q2 : Génère moi 3 ad-copies présentant REMPLIR ICI de {product}, avec des titres et des corps, et inclure des mots-clés à longue traîne sur lesquels je peux enchérir.
Q3 : Crée moi un script publicitaire sur {product} destiné à REMPLIR ICI.

Nouvelles questions :
"""

repsonse_prompts = """
A partir des extraits suivants d'un long document et d'une DEMANDE DE L'UTILISATEUR, créez une RÉPONSE finale avec des références ("SOURCES"). 
Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas. N'essayez pas d'inventer une réponse.
Renvoyez TOUJOURS une partie "SOURCES" dans votre réponse.
La RÉPONSE doit comporter plusieurs phrases.

DEMANDE DE L'UTILISATEUR : {question}
=========
{summaries}
=========
RÉPONSE :
"""