quests = [
    # Chap 1: goal 3
    {
        "quest_type": 1,
        "goal_nbr": 0,
        "name": "chap1q0",
        "statement": "Aller retrouver ta tante à l'hôpital de Beauville",
        "dialogue": [
            "Ah te voilà, ta tante m'a demandé de t'attendre ici et de t'envoyer près d'elle.\n"
            "Tu pourras la trouver à l'hôpital de Beauville, c'est le village juste au nord d'ici.\n"
            "Elle m'a également demandé de te donner ceci, c'est un journal de quêtes.\n"
            "Si tu ne sais plus ce que tu dois faire, appuie sur 'F' pour l'ouvrir.",
            "Ta tante se trouve à l'hôpital de Beauville, il est à droite quand tu rentres.",
            "Tu es là ! Tu vas pouvoir m’aider !\nComme tu le sais, ton oncle et moi avons été envoyés ici pour contrer l'épidémie "
            "qui frappe les habitants de Démuin. Le virus qui circule actuellement est le nacoro mais tu as déjà reçu le vaccin "
            "contre ce virus donc, si tu le souhaites, tu peux nous aider sans problème."
        ],
        "npc1_name": "m0npc1",
        "npc2_name": "mBnpc0",
        "npc2_type": "npc29"
    },
    {
        "quest_type": 1,
        "goal_nbr": 3,
        "name": "chap1q1",
        "statement": "Apporter les vaccins au village de Démuin",
        "dialogue": [
            "Tu veux nous aider ? Super ! Tu vas pouvoir m'assister. Il faut que je reste ici mais ton oncle, lui, est "
            "sur le terrain et j'ai besoin de lui apporter d'autres vaccins. Pourrais-tu les lui apporter ? "
            "Le village se trouve au sud-est d'ici.\n"
            "Je vais aussi te donner ceci, c'est un livret expliquant les 17 ODD des Nations Unies, c'est-à-dire les "
            "Objectifs de Développement Durables, des objectifs à suivre si l'on veut laisser un monde meilleur aux générations futures, "
            "à commencer par la tienne.\nSi tu ne sais pas pourquoi on te demande de faire telle ou telle chose, n'hésite pas "
            "à regarder dans ce livret à quoi correspond chaque objectif, appuie sur 'G' pour l'ouvrir.\n"
            "Je te laisse aller livrer ces vaccins maintenant. Reviens me voir quand c'est fait.",
            "Démuin se trouve au sud-est, tu peux y aller par en bas ou par le champ à droite d'ici.",
            "Ah super, les vaccins ! C'est gentil de nous aider."
        ],
        "npc1_name": "mBnpc0",
        "npc2_name": "mDnpc0",
        "npc2_type": "npc13"
    },
    {
        "quest_type": 1,
        "goal_nbr": 3,
        "name": "chap1q2",
        "statement": "Apporter le matériel pour la tente médicale à Démuin",
        "dialogue": [
            "Te revoilà. Avec notre aide, le village va pouvoir s'en sortir, mais une fois tous les habitants guéris, "
            "notre travail ne sera pas fini pour autant. Le principe du développement durable est de penser à long terme. "
            "C'est pourquoi nous avons décidé de construire une tente médicale qui permettra de faciliter le travail des "
            "professionnels de la santé dans ce village.\nPour cela, veux-tu bien apporter ce matériel là-bas? "
            "Après ça je ne t'embêterai plus.",
            "Apporte le matériel à ton oncle qui doit toujours être dans le village.",
            "Super, merci beaucoup. Je n'ai rien d'autre à te faire faire mais si tu t'ennuies, tu peux apporter ton aide à Démuin "
            "en allant demander au chef du village s'il y a quelque chose que tu pourrais faire. C'est le vieil homme derrière moi. "
        ],
        "npc1_name": "mBnpc0",
        "npc2_name": "mDnpc0",
        "npc2_type": "npc13"
    },

    # Chap 2: goal 6 & 15
    {
        "quest_type": 2,
        "goal_nbr": 15,
        "name": "chap2q0",
        "statement": "Récolter 10 bois dans la forêt",
        "dialogue": [
            "Bonjour mon enfant, tu veux nous aider ? Eh bien comme tu peux le voir, les toits de certaines maisons du village se sont écroulés. "
            "Il faut les reconstruire au plus vite mais pour ça il nous faut du bois. Pourrais-tu aller récolter 10 bois pour nous ?\n"
            "Dans la forêt à l'est d'ici se trouvent des petits arbres que tu pourras couper avec cette hache, tiens !\n"
            "Appuie sur 'C' pour l'équiper.",
            "Il nous faut 10 arbres, normalement il y en a assez dans la forêt à l'est.",
            "C'est très bien ! On va pouvoir se mettre à la rénovation mais ça va mettre un peu de temps. "
            "Si tu veux encore nous aider, va parler au cultivateur qui se trouve dans le champ au nord d'ici, il a besoin d'aide.",
            "Tu as coupé 1 arbre !"
        ],
        "npc1_name": "mDnpc1",
        "npc2_name": "mDnpc1",
        "npc2_type": "npc8",
        "obj_type": "tree",
        "obj_nbr": 10
    },
    {
        "quest_type": 2,
        "goal_nbr": 6,
        "name": "chap2q1",
        "statement": "Creuser une tranchée pour l'eau",
        "dialogue": [
            "Oui en effet je ne dirais pas non à un peu d'aide. Peux-tu achever la tranchée que j'ai commencée ici jusqu'à la rivière pour amener l'eau aux plantations.\n"
            "Creuse la terre avec cette pelle. Appuie sur 'V' pour l'équiper.",
            "Creuse bien tous les carrés de terre de là où je suis jusqu'à la rivière.",
            "Merci beaucoup pour ton aide, mais la pression de la rivière n'est pas assez forte pour que l'eau arrive ici. "
            "Pourrais-tu aller voir à la source au nord d'ici s’il y a moyen d'y remédier ?\nTu y trouveras mon ami, il te dira ce que tu dois faire.",
            "1 carré de terre en moins !"
        ],
        "npc1_name": "m2npc1",
        "npc2_name": "m2npc1",
        "npc2_type": "npc12",
        "obj_type": "dirt",
        "obj_nbr": 10
    },
    {
        "quest_type": 2,
        "goal_nbr": 6,
        "name": "chap2q2",
        "statement": "Casser les gros rochers dans l'eau",
        "dialogue": [
            "Tu veux augmenter la pression du cours d’eau ? Oui, il y a ces 4 gros rochers qui sont tombés dans l'eau et qui font barrage. "
            "Tu peux les casser avec cette pioche.\nAppuie sur 'B' pour l'équiper.",
            "Une fois que tu as fini, retourne aux plantations pour voir si l'eau arrive bien.",
            "Bien joué, retourne aux plantations pour voir si tout va bien maintenant.",
            "1 rocher en moins !"
        ],
        "npc1_name": "m3npc1",
        "npc2_name": "m3npc1",
        "npc2_type": "npc4",
        "obj_type": "rock",
        "obj_nbr": 4
    },

    # Chap 3: goal 14
    {
        "quest_type": 1,
        "goal_nbr": 0,
        "name": "chap3q0",
        "statement": "Retourner auprès de sa tante",
        "dialogue": [
            "Tu as fait du bon boulot ici, nous allons reconstruire les toits des maisons du village avec les bois que tu nous as apportés. "
            "Pendant ce temps-là, tu peux aller rejoindre ta tante, elle a apparemment encore des choses à te faire faire.",
            "Reviens faire un tour ici dans quelques temps pour voir le changement.",
            "J'ai entendu que tu avais bien aidé le village de Démuin, c'est super. Nous n'avons pas encore fini de traiter l'épidémie mais nous avançons bien.\n"
            "En attendant qu'on ait fini, tu peux te rendre à Cénet et aider les villageois qui en ont besoin comme tu l'as fait pour Démuin.\n"
            "C'est le village qui se trouve au sud-ouest d'ici."
        ],
        "npc1_name": "mDnpc1",
        "npc2_name": "mBnpc0",
        "npc2_type": "npc29"
    },
    {
        "quest_type": 2,
        "goal_nbr": 14,
        "name": "chap3q1",
        "statement": "Ramasser les déchets dans l'eau",
        "dialogue": [
            "Bonjour et bienvenue à Cénet, le village de pêche. Enfin, nous sommes un village de pêche mais peut-être plus pour longtemps... "
            "Comme tu peux le voir dans la rivière, il y a des déchets qui polluent l'eau, dérangent le milieu naturel des poissons et nous "
            "empêchent de travailler car maintenant, tout ce que nous relevons de nos filets, ce sont ces déchets. "
            "Tu pourrais ramasser les déchets comme celui qu'il y a juste à côté de toi ? Comme ça, moi, pendant ce temps, je pourrai essayer "
            "de prendre les poissons qui arrivent à passer grâce à toi. "
            "Ramasse-les avec ce filet.\nAppuie sur 'N' pour l'équiper.",
            "Il reste encore des déchets dans l'eau.",
            "Merci beaucoup, je n'ai pas encore réussi à en avoir un mais je sens que ça va mordre !",
            "1 déchet en moins !"
        ],
        "npc1_name": "mCnpc1",
        "npc2_name": "mCnpc1",
        "npc2_type": "npc3",
        "obj_type": "trash",
        "obj_nbr": 5
    },
    {
        "quest_type": 1,
        "goal_nbr": 0,
        "name": "chap3q2",
        "statement": "Livrer le poisson à Beauville",
        "dialogue": [
            "Notre village gagne de l'argent en livrant du poisson aux autres villages. C'est pourquoi il est vital pour nous que l'eau reste de bonne qualité.\n"
            "Si tu retournes à Beauville, peux-tu livrer ce colis s'il-te-plait ?\nL'homme à qui tu dois le livrer se trouve au centre du village.",
            "L'homme est souvent près de la maison au centre de Beauville.",
            "C'est le colis provenant de Cénet ? Cool, merci bien. Tu peux aller leur dire que je l'ai bien reçu."
        ],
        "npc1_name": "mCnpc3",
        "npc2_name": "mBnpc1",
        "npc2_type": "npc1"
    },
    {
        "quest_type": 1,
        "goal_nbr": 14,
        "name": "chap3q3",
        "statement": "Aller voir la source de cette pollution",
        "dialogue": [
            "La pollution est déjà revenue ! Il faut remédier à ce problème à la source, sinon cela reviendra tout le temps. "
            "Cette pollution vient de l'usine au nord.\nPourrais-tu aller voir ce qui s'y passe ? "
            "Tu peux y aller en passant par Beauville. L'entrée se trouve sur la gauche.",
            "Pour aller à l'usine, passe par Beauville et l'entrée se trouve à gauche.",
            "Le chef de l’usine ? C'est l'homme là-bas près des tonneaux."
        ],
        "npc1_name": "mCnpc1",
        "npc2_name": "m4npc1",
        "npc2_type": "npc1"
    },
    {
        "quest_type": 1,
        "goal_nbr": 14,
        "name": "chap3q4",
        "statement": "Donner la réponse du patron de l'usine au pêcheur",
        "dialogue": [
            "Oui, c'est moi le chef de l'usine. "
            "Arrêter de polluer ? La pollution arrive jusqu'au village de Cénet et empêche les villageois de pêcher ? Mince !\n"
            "Ecoute, je sais que mon usine pollue et j'aimerais bien régler ce problème mais je ne peux rien y faire pour le moment. "
            "Je n'ai pas assez de travailleurs et personne ne veut travailler dans cette pollution.",
            "Je t'ai dit que je ne pouvais rien y faire pour le moment.",
            "Comment ça, ils ne peuvent rien faire pour l’instant ? C'est pourtant simple, s'ils ne règlent pas le problème, on ne pourra plus "
            "distribuer du poisson aux autres villages, à commencer par eux !"
        ],
        "npc1_name": "m4npc2",
        "npc2_name": "mCnpc1",
        "npc2_type": "npc3"
    },

    # Chap 4: goal 15
    {
        "quest_type": 1,
        "goal_nbr": 3,
        "name": "chap4q0",
        "statement": "Retourner voir la situation à Démuin",
        "dialogue": [
            "Nous en avons fini avec cette épidémie, tout va bien maintenant. Merci encore pour ton aide. "
            "N'hésite pas à repasser au village de Démuin. ",
            "Retourne au village voir comme il a changé.",
            "Tous les malades du village sont guéris et tous les habitants ont eu le vaccin donc on en a fini avec ce virus !"
        ],
        "npc1_name": "mBnpc0",
        "npc2_name": "mDnpc0",
        "npc2_type": "npc13"
    },
    {
        "quest_type": 1,
        "goal_nbr": 15,
        "name": "chap4q1",
        "statement": "Parler au chef du village",
        "dialogue": [
            "Après cette bonne nouvelle j'en ai aussi une mauvaise. Des animaux ont saccagé les plantations au nord. "
            "Va voir le chef du village, il va t'expliquer.",
            "Va parler au chef du village.",
            "Ah, te voilà ! C'est terrible, avec les arbres que tu as coupés dans la forêt, tu as détruit le milieu de vie de certains animaux "
            "qui n'ont eu d'autre choix que d'aller manger nos plantations. "
            "On va mettre de la nourriture à leur disposition dans la forêt afin qu'ils ne recommencent pas, mais il faut vraiment "
            "replanter des arbres là où tu les as coupés. Va voir mon fils. Il a déraciné les souches d'arbres. Il ne te reste plus qu'à planter."
        ],
        "npc1_name": "mDnpc0",
        "npc2_name": "mDnpc1",
        "npc2_type": "npc8"
    },
    {
        "quest_type": 2,
        "goal_nbr": 15,
        "name": "chap4q2",
        "statement": "Replanter des arbres dans la forêt",
        "dialogue": [
            "Salut, j'ai déjà fait les trous dans la terre. Il ne te reste plus qu'à planter ces petits arbres dedans.",
            "Plante bien des arbres dans tous les trous que j'ai faits.",
            "Super, beau boulot ! Nous n'avons plus qu'à attendre qu'ils poussent.",
            "1 arbre de planté !"
        ],
        "npc1_name": "m1npc1",
        "npc2_name": "m1npc1",
        "npc2_type": "npc16",
        "obj_type": "dirt",
        "obj_nbr": 13
    },
    {
        "quest_type": 1,
        "goal_nbr": 1,
        "name": "chap4q3",
        "statement": "Proposer son aide au cultivateur",
        "dialogue": [
            "Maintenant va voir le cultivateur pour l'aider. Les champs ont été tout saccagés.",
            "Vois avec le cultivateur si tu peux lui apporter ton aide.",
            "Je n'ai pas besoin d'aide pour les champs maintenant. Nous allons devoir recommencer tout. "
            "Par contre, tu peux peut-être m'aider pour autre chose.\n"
            "Il n'y aura plus assez de boulot ici pour tous les villageois qui y travaillaient avant "
            "donc, si tu as une idée d'un boulot qu'ils pourraient faire, va leur proposer.\n"
            "C'est important pour maintenir l'équilibre économique du village."
        ],
        "npc1_name": "mDnpc1",
        "npc2_name": "m2npc1",
        "npc2_type": "npc12"
    },
    {
        "quest_type": 1,
        "goal_nbr": 1,
        "name": "chap4q4",
        "statement": "Proposer de nouveaux employés au patron de l'usine",
        "dialogue": [
            "Travailler à l’usine ? Oui, pourquoi pas.",
            "Dès que c'est bon pour le patron, on peut aller y travailler.",
            "De nouveaux travailleurs ? Vois ça avec mon employé à l'entrée. C'est lui qui devra gérer cette équipe."
        ],
        "npc1_name": "m2npc2",
        "npc2_name": "m4npc2",
        "npc2_type": "npc2"
    },
    {
        "quest_type": 1,
        "goal_nbr": 1,
        "name": "chap4q5",
        "statement": "Dire aux habitants de Démuin qu'ils peuvent aller à l'usine",
        "dialogue": [
            "Une équipe pour gérer la pollution, moi ça me va. Tu peux leur dire de venir.",
            "Ils peuvent commencer dès qu'ils arrivent.",
            "Il nous attend ? D'accord, on y va. Merci pour le coup de main."
        ],
        "npc1_name": "m4npc1",
        "npc2_name": "m2npc2",
        "npc2_type": "npc24"
    },
    {
        "quest_type": 1,
        "goal_nbr": 14,
        "name": "chap4q6",
        "statement": "Annoncer au pêcheur la bonne nouvelle",
        "dialogue": [
            "C'est parfait ici, merci pour ton aide. Une dernière chose, maintenant que le problème de pollution est réglé de notre côté, "
            "tu voudrais bien dire aux pêcheurs de Cénet de recommencer à nous envoyer leurs marchandises ?",
            "Vas dire aux pêcheurs de Cénet que nous ne pollurons plus la rivière !",
            "C'est super, la rivière n'a jamais été aussi propre ! Merci pour tout."
        ],
        "npc1_name": "m4npc2",
        "npc2_name": "mCnpc1",
        "npc2_type": "npc3"
    }
]


interaction_texts = {
    "tree": "Utilise une hache si tu veux couper cet arbre.",
    "dirt": "Utilise une pelle si tu veux enlever cette terre",
    "rock": "Utilise une pioche si tu veux casser ce rocher.",
    "trash": "Utilise un filet si tu veux ramasser ce déchet.",

    "m0npc1": "Comment se passe ton aventure jusqu'ici ?",
    "m1npc1": "Oui je fais une petite pause. Je vais m'y remettre bientôt.",
    "m2npc1": "Mes plantations sont de plus en plus belles chaque jour. N'est-ce pas ?",
    "m2npc2": "C'est agréable de travailler ici. Tu ne trouves pas ?",
    "m3npc1": "Des rochers se sont décrochés de la montagne. Il faut faire attention par ici.",
    "m4npc1": "Si tu cherches le patron, c'est l'homme là-bas près des tonneaux.",
    "m4npc2": "Si tu trouves des gens qui cherchent un boulot envoie-les moi, je cherche des travailleurs pour mon usine.",
    "mAnpc1": "Salut",
    "mBnpc0": "Je suis contente que tu sois venu nous aider. Si tu n'as rien à faire, n'hésite pas à te balader dans la région.",
    "mBnpc1": "Les poissons que nous livre le village de Cénet sont de moins en moins bons à cause de la pollution. J'espère que cela va s'arranger.",
    "mBnpc2": "mBnpc2",
    "mBnpc3": "mBnpc3",
    "mBnpc4": "mBnpc4",
    "mCnpc1": "J'espère que la pêche sera bonne aujourd'hui.",
    "mCnpc2": "J'aime bien regarder les poissons passer ici.",
    "mCnpc3": "Désolé mais j'ai du travail.",
    "mDnpc0": "Si tu ne sais pas quoi faire, retourne auprès de ta tante. Elle a toujours des choses à faire faire aux autres.",
    "mDnpc1": "Comment vas-tu mon enfant?",
    "mDnpc2": "Si tu cherches le chef du village c'est le vieil homme là bas au centre.",
    "mDnpc3": "On a vraiment pas de chance dans ce village!",
    "mDnpc4": "Attention à ne pas marcher dans nos plantations!"
    }


goals = [
    # Goal 0:
    {
        "title": "17 objectifs pour transformer notre monde",
        "expl": "Les objectifs de développement durable sont un appel à l’action de tous les pays – "
                "pauvres, riches et à revenu intermédiaire – afin de promouvoir la prospérité tout en protégeant la planète. "
                "Ils reconnaissent que mettre fin à la pauvreté doit aller de pair avec des stratégies qui développent la "
                "croissance économique et répondent à une série de besoins sociaux, notamment l’éducation, la santé, "
                "la protection sociale et les possibilités d’emploi, tout en luttant contre le changement climatique "
                "et la protection de l’environnement.\n"
                "Site internet : https://www.un.org/sustainabledevelopment",
        "advice": "",
        "facts": [],
        "color": (255, 255, 255)
    },

    # Goal 1:
    {
        "title": "Pas de pauvreté",
        "expl": "La pauvreté ne se résume pas à l’insuffisance de revenus et de ressources pour assurer des moyens de subsistance durables."
                "Ses manifestations comprennent la faim et la malnutrition, l’accès limité à l’éducation et aux autres services de base, "
                "la discrimination et l’exclusion sociales ainsi que le manque de participation à la prise de décisions.",
        "advice": "Donne ce que tu n'utilises pas.",
        "facts": [
            "783 millions de personnes vivent en-dessous du seuil de pauvreté international fixé à 1,90 dollar par jour",
            "La majorité de ces personnes appartient à deux régions : l’Asie du Sud et l’Afrique subsaharienne",
            "Les taux de pauvreté élevés se trouvent souvent dans les petits pays fragiles et touchés par un conflit",
            "Un enfant sur quatre âgé de moins de 5 ans à travers le monde a une taille insuffisante par rapport à son âge."
        ],
        "color": (224, 43, 64)
    },

    # Goal 2:
    {
        "title": "Faim Zéro",
        "expl": "Il est temps de repenser la façon dont nous cultivons, partageons et consommons notre alimentation. "
                "Quand elles sont pratiquées correctement, l’agriculture, la sylviculture et la pêche peuvent produire "
                "des aliments pour tous et générer des revenus décents, tout en soutenant un développement centré sur "
                "les habitants des régions rurales et la protection de l’environnement.",
        "advice": "Gaspille moins la nourriture et soutiens l'agriculture locale.",
        "facts": [
            "Une personne sur neuf dans le monde est sous-alimentée (soit 815 millions)",
            "La majorité des personnes souffrant de la faim dans le monde vivent dans un pays en développement, où 12,9 % de la population est sous-alimentée",
            "L’Asie est le continent qui compte le plus de personnes souffrant de la faim – les deux tiers de la population totale",
            "La malnutrition est la cause de près de la moitié (45%) des décès d’enfants de moins de 5 ans – 3,1 millions d’enfants chaque année."
        ],
        "color": (209, 159, 42)
    },

    # Goal 3:
    {
        "title": "Bonne santé et bien-être",
        "expl": "De nombreux efforts supplémentaires sont nécessaires pour éliminer complètement un large éventail de "
                "maladies et résoudre de nombreux problèmes de santé persistants et émergents. En mettant l’accent sur un "
                "financement plus efficace des systèmes de santé, l’amélioration de l’assainissement et de l’hygiène, un "
                "meilleur accès aux professionnels de santé et davantage de conseils sur les moyens de réduire la pollution "
                "ambiante, des progrès significatifs peuvent être réalisés pour sauver des vies.",
        "advice": "Pense à faire tes vaccins.",
        "facts": [
            "Depuis 2000, les vaccins contre la rougeole ont permis d’éviter plus de 15,6 millions de décès",
            "Le risque de décès est également plus élevé en zone rurale et dans les ménages les plus pauvres",
            "Le VIH est la principale cause de décès chez les femmes en âge de procréer dans le monde",
            "La moitié seulement des femmes dans les régions en développement ont bénéficié du minimum recommandé de soins de santé."
        ],
        "color": (76, 159, 56)
    },

    # Goal 4:
    {
        "title": "Education de qualité",
        "expl": "Obtenir une éducation de qualité est le fondement pour améliorer la vie des gens et le développement durable. "
                "Outre l’amélioration de leur qualité de vie, l’accès à une éducation inclusive et équitable peut aider à "
                "doter les populations locales des outils nécessaires pour développer des solutions innovantes aux plus grands "
                "problèmes du monde.",
        "advice": "Aide à l'éducation des enfants dans ta communauté.",
        "facts": [
            "Plus de la moitié des enfants qui ne sont pas inscrits à l’école vivent en Afrique sub-saharienne",
            "On estime que 50 % des enfants en âge de fréquenter l’école primaire qui ne sont pas scolarisés vivent dans des zones touchées par un conflit",
            "617 millions de jeunes dans le monde manquent de compétences de base en mathématiques et en alphabétisation."
        ],
        "color": (197, 25, 45)
    },

    # Goal 5:
    {
        "title": "Egalité entre les sexes",
        "expl": "Des progrès ont été accomplis dans le monde entier en matière d’égalité des sexes dans le cadre de la réalisation "
                "des objectifs du Millénaire pour le développement (notamment l’égalité d’accès à l’enseignement primaire pour "
                "les filles et les garçons), mais les femmes et les filles continuent de pâtir de discrimination et de violences "
                "dans toutes les régions du monde.",
        "advice": "Défends l'égalité des droits entre les hommes et les femmes.",
        "facts": [
            "Environ les deux tiers des pays des régions en développement ont atteint l’égalité des sexes dans l’enseignement primaire",
            "49 pays ne disposent toujours pas de lois protégeant les femmes contre la violence domestique",
            "750 millions de femmes et de filles dans le monde ont été mariées avant l’âge de 18 ans",
            "Une femme sur cinq, dont 19% des femmes âgées de 15 à 49 ans, ont subi des violences physiques et/ou sexuelles de la "
            "part d’un partenaire intime ou des violences sexuelles de la part d’une autre personne."
        ],
        "color": (255, 58, 33)
    },

    # Goal 6:
    {
        "title": "Eau propre et assainissement",
        "expl": "Une eau propre et accessible pour tous est un élément essentiel du monde dans lequel nous voulons vivre. "
                "Il y a assez d’eau sur la planète pour réaliser ce rêve. Pour améliorer l’assainissement et l’accès à l’eau potable, "
                "il faut investir davantage dans la gestion des écosystèmes d’eau douce et des installations sanitaires au "
                "niveau local dans plusieurs pays en développement d’Afrique subsaharienne, d’Asie centrale, d’Asie du Sud, "
                "d’Asie orientale et d’Asie du Sud-Est.",
        "advice": "Evite de gaspiller l'eau.",
        "facts": [
            "Entre 1990 et 2015, la proportion de la population mondiale utilisant une source d’eau potable améliorée a augmenté de 76% à 90%",
            "3 personnes sur 10 n’ont pas accès à des services d’eau potable gérés de manière sûre",
            "Chaque jour, 1 000 enfants meurent de maladies faciles à prévenir dues aux conditions d’assainissement et d’hygiène",
            "2,4 milliards de personnes manquent d’installations sanitaires de base, telles que des toilettes ou de latrines",
            "Plus de 80% des eaux usées résultant des activités humaines sont déversées dans les rivières ou la mer sans aucune dépollution."
        ],
        "color": (39, 189, 226)
    },

    # Goal 7:
    {
        "title": "Energie propre et d'un coût abordable",
        "expl": "L’énergie est au centre de presque tous les défis majeurs, mais aussi des perspectives prometteuses, qui se "
                "présentent au monde aujourd’hui. Qu’il s’agisse d’emplois, de sécurité, de changement climatique, de production "
                "de nourriture ou d’accroissement des revenus, l’accès de tous à l’énergie est essentiel. Il faut améliorer l’accès "
                "à des technologies et à des carburants propres, et il faut progresser vers l’intégration des énergies renouvelables "
                "dans les bâtiments, les transports et l’industrie.",
        "advice": "Utilise des appareils et des ampoules à basse consommation.",
        "facts": [
            "13% de la population mondiale n’a pas accès à l’électricité moderne",
            "3 milliards de personnes dépendent du bois, du charbon ou des déchets animaux pour la cuisson et le chauffage",
            "L’énergie est le principal facteur contribuant au changement climatique, soit 60 % des émissions mondiales de gaz à effet de serre",
            "La part des énergies renouvelables dans la consommation finale d’énergie a atteint 17,5% en 2015."
        ],
        "color": (252, 195, 18)
    },

    # Goal 8:
    {
        "title": "Travail décent et croissance économique",
        "expl": "Le taux de chômage dans le monde atteint les 5,7%. Dans trop d’endroits, avoir un emploi ne garantit pas la capacité "
                "d’échapper à la pauvreté. La lenteur et le caractère inégal de ces progrès font que nous devons revoir et "
                "réorganiser nos politiques économiques et sociales visant à éliminer complètement la pauvreté.",
        "advice": "Profite de l'éducation qu'on t'offre, certains n'ont pas cette chance.",
        "facts": [
            "Les hommes gagnent 12,5% de plus que les femmes dans 40 pays sur 45 disposant de données",
            "L’écart de rémunération entre hommes et femmes dans le monde est de 23% et, sans action décisive, "
            "il faudra encore 68 ans pour parvenir à un salaire égal. Le taux d’activité des femmes sur le marché "
            "du travail est de 63% et celui des hommes de 94%."
        ],
        "color": (162, 25, 66)
    },

    # Goal 9:
    {
        "title": "Industrie, innovation et infrastructures",
        "expl": "Les investissements dans l’infrastructure – le transport, l’irrigation, l’énergie, les technologies de "
                "l'information et de la communication – sont essentiels pour parvenir au développement durable et à "
                "l'autonomisation des communautés dans de nombreux pays. On sait depuis longtemps que la croissance de la "
                "productivité, des revenus ainsi que les améliorations en matière de santé et d’éducation nécessitent des "
                "investissements dans les infrastructures.",
        "advice": "Soutien des projets innovants.",
        "facts": [
            "16% de la population mondiale n’a pas accès aux réseaux haut débit mobiles",
            "L’industrialisation a un effet multiplicateur sur l’emploi et donc un impact positif sur la société. "
            "Chaque emploi dans le secteur manufacturier crée 2,2 emplois dans d’autres secteurs."
        ],
        "color": (253, 105, 37)
    },

    # Goal 10:
    {
        "title": "Inégalités réduites",
        "expl": "La communauté internationale a considérablement progressé pour ce qui est de sortir les populations de la pauvreté. "
                "Les nations les plus vulnérables continuent à marquer des points dans la réduction de la pauvreté. "
                "Cependant, les inégalités persistent et il y a encore de vastes disparités vis-à-vis de l’accès aux services "
                "de santé et à l’éducation et à d’autres moyens de production.",
        "advice": "Soutien les personnes marginalisées et désavantagées.",
        "facts": [
            "La protection sociale a été considérablement étendue dans le monde, mais les personnes handicapées ont jusqu’à "
            "cinq fois plus de chances que la moyenne d’engager des dépenses de santé importantes",
            "Jusqu’à 30% de l’inégalité des revenus est due à l’inégalité au sein des ménages, y compris entre les femmes et les hommes. "
            "Les femmes sont également plus susceptibles que les hommes de vivre avec moins de 50% du revenu médian."
        ],
        "color": (221, 19, 103)
    },

    # Goal 11:
    {
        "title": "Villes et communautés durables",
        "expl": "De nombreux problèmes se posent pour faire en sorte que les villes continuent de générer des emplois et de "
                "la prospérité, sans grever les sols et les ressources naturelles. Les problèmes des villes les plus courants "
                "incluent le surpeuplement, le manque de fonds pour faire fonctionner les services de base, l’insuffisance de "
                "logements adéquats, des infrastructures dégradées et l’augmentation de la pollution de l’air.",
        "advice": "Privilégie le vélo, la marche ou les transports en commun.",
        "facts": [
            "La moitié de l’humanité – 3,5 milliards de personnes – vit aujourd’hui dans des villes. Ce chiffre devrait atteindre 5 milliards d’ici 2030",
            "883 millions de personnes vivent dans des bidonvilles aujourd’hui et la plupart se trouvent en Asie de l’Est et du Sud-Est",
            "Les villes n’occupent que 3 % de la masse continentale mondiale, ",
            "mais produisent plus de 70 % de ses émissions de dioxyde de carbone et consomment entre 60 et 80% de l’énergie mondiale."
        ],
        "color": (253, 157, 36)
    },

    # Goal 12:
    {
        "title": "Consommation et production durables",
        "expl": "La consommation et la production durables encouragent à utiliser les ressources et l’énergie de manière efficace, "
                "à mettre en place des infrastructures durables et à assurer à tous l’accès aux services de base, "
                "des emplois verts et décents et une meilleure qualité de la vie. Elles contribuent à mettre en œuvre des "
                "plans de développement général, à réduire les coûts économiques, environnementaux et sociaux futurs, "
                "à renforcer la compétitivité économique et à réduire la pauvreté.",
        "advice": "Recycle le papier, le plastique, le verre et l'aluminium.",
        "facts": [
            "Si la population mondiale atteint 9,6 milliards de personnes d’ici à 2050, l’équivalent de près de trois planètes "
            "pourrait être nécessaire pour fournir les ressources nécessaires pour maintenir les modes de vie actuels",
            "L’être humain pollue l’eau plus vite que le temps nécessaire à la nature pour recycler et purifier l’eau dans les lacs et les rivières",
            "Si les consommateurs du monde entier optaient pour des ampoules à haut rendement énergétique, le monde économiserait 120 milliards de dollars par an."
        ],
        "color": (191, 139, 46)
    },

    # Goal 13:
    {
        "title": "Lutte contre les changements climatiques",
        "expl": "Les conditions météorologiques changent, le niveau de la mer monte, les phénomènes météorologiques deviennent "
                "plus extrêmes et les émissions de gaz à effet de serre sont maintenant à leur plus haut niveau de l’histoire. "
                "Sans action, la température moyenne à la surface du monde devrait dépasser les 3 degrés centigrades ce siècle. "
                "Les personnes les plus pauvres et les plus vulnérables sont les plus touchées.",
        "advice": "Agis maintenant pour arrêter le réchauffement climatique.",
        "facts": [
            "Lorsque la température augmente d’un degré, la production de céréales diminue d’environ 5 %",
            "Les émissions globales de dioxyde de carbone (CO2) ont augmenté de près de 50 % depuis 1990",
            "Les émissions ont augmenté plus rapidement entre 2000 et 2010 que durant chacune des trois décennies précédentes."
        ],
        "color": (72, 119, 60)
    },

    # Goal 14:
    {
        "title": "Vie aquatique",
        "expl": "La gestion prudente de cette ressource vitale mondiale est un élément clé pour un avenir durable. Cependant, "
                "à l’heure actuelle, les eaux côtières se détériorent continuellement à cause de la pollution et l’acidification "
                "des océans a un effet de confrontation sur le fonctionnement des écosystèmes et de la biodiversité. "
                "Cela a également un impact négatif sur la pêche artisanale. Les aires marines protégées doivent être gérées "
                "efficacement et dotées de ressources suffisantes, et des réglementations doivent être mises en place pour "
                "réduire la surpêche, la pollution marine et l’acidification des océans.",
        "advice": "Evite les sacs plastiques pour garder les océans propres.",
        "facts": [
            "Les océans couvrent les trois quarts de la surface de la Terre, contiennent 97% de l’eau de la Terre, "
            "et représentent 99% des espaces de vie disponibles sur terre en volume",
            "Plus de trois milliards de personnes dépendent de la biodiversité marine et côtière pour subvenir à leurs besoins",
            "Les océans absorbent environ 30% du CO2 produit par les humains et atténuent les impacts du réchauffement climatique."
        ],
        "color": (0, 125, 187)
    },

    # Goal 15:
    {
        "title": "Vie terrestre",
        "expl": "Les forêts recouvrent 30.7% de la surface de la planète, assurent la sécurité alimentaire et fournissent "
                "des abris, et sont essentielles pour lutter contre le changement climatique, protéger la biodiversité et "
                "les foyers des populations autochtones. En protégeant les forêts, nous pourrons également renforcer la "
                "gestion des ressources naturelles et accroître la productivité des terres.",
        "advice": "Plante un arbre et respecte l'environnement.",
        "facts": [
            "Environ 1,6 milliard de personnes – dont environ 70 millions de cultures autochtones – dépendent des forêts pour assurer leur subsistance",
            "Les forêts abritent plus de 80 % des espèces d’animaux, de plantes et d’insectes que compte la planète",
            "Sur les 8 300 races animales connues dans le monde, 8% ont disparu et 22% sont menacées d’extinction."
        ],
        "color": (64, 174, 73)
    },

    # Goal 16:
    {
        "title": "Paix, justice et institutions efficaces",
        "expl": "La lutte contre les menaces d’homicide, la violence contre les enfants, la traite des êtres humains et la "
                "violence sexuelle est importante pour promouvoir des sociétés pacifiques et inclusives au service du "
                "développement durable. Cette lutte ouvre la voie de l’accès à la justice pour tous et à la mise en place "
                "d’institutions efficaces et responsables à tous les niveaux.",
        "advice": "Défends les droits de l'homme.",
        "facts": [
            "La justice et la police font partie des institutions les plus touchées par la corruption",
            "La corruption, la fraude, le vol et l’évasion fiscale coûtent quelque $1,26 billion de dollars par an aux pays en développement",
            "Environ 28,5 millions d’élèves du primaire qui ne sont pas scolarisés vivent dans des zones touchées par le conflit."
        ],
        "color": (0, 85, 138)
    },

    # Goal 17:
    {
        "title": "Partenariats pour la réalisation des objectifs",
        "expl": "Des partenariats efficaces entre les gouvernements, le secteur privé et la société civile sont nécessaires "
                "pour un programme de développement durable réussi. Ces partenariats inclusifs construits sur des principes "
                "et des valeurs, une vision commune et des objectifs communs qui placent les peuples et la planète au centre, "
                "sont nécessaires au niveau mondial, régional, national et local.",
        "advice": "Participe à des projets de développement.",
        "facts": [
            "79% des importations originaires de pays en développement vers les pays développés sont exemptées de droits de douane",
            "Plus de quatre milliards de personnes n’utilisent pas Internet et 90% d’entre elles vivent dans des pays en développement",
            "Dans le monde, 30% des jeunes sont des natifs numériques, qui utilisent Internet depuis au moins cinq ans."
        ],
        "color": (26, 54, 104)
    }
]
