import re


Relation_dict = {
    0: "Strongly Disliked",
    0.2: "Disliked",
    0.4: "Neutral or Indifferent",
    0.6: "Liked",
    0.8: "Loved",
    1.0: "Deeply Loved"
}

Person_dict = { 
    "Shan": { "Description": "Meet Shan, the leading character in our story. She's a laid-back college sophomore, born into a family of four with an older brother a year her senior. Shan's a sporty girl who frequently hits the school gym, works part-time at a coffee shop, and volunteers at an animal shelter. Her post-graduation dream? To become a veterinarian, taking her love for animals to the next level.",
              "Relation_with_Shan":1,
              "Apearance":0
    },
    "Jake": { "Description": "Jake, a college sophomore, is deeply passionate about skateboarding and enjoys the exhilaration it brings as he carves through city streets. Beyond skateboarding, he's a vintage vinyl record enthusiast, a talented storyteller through stand-up comedy, and a dedicated youth center volunteer, inspiring the next generation. Jake's vibrant personality ensures every moment, whether on or off the skateboard, is filled with excitement.",
              "Relation_with_Shan":0.55,
              "Apearance":1
    },

    "Max": { "Description": "Meet Max, the epitome of charm and athleticism. At 6 feet tall, he boasts a sculpted physique, sunlit hair, and captivating emerald-green eyes that promise adventures. Whether dominating the soccer field or sculpting his physique in the gym, Max exudes an irresistible magnetic appeal, making every moment with him enchanting.",
              "Relation_with_Shan":0.4,
              "Apearance":0
    },

    "Ethan": { "Description": "Ethan, the charismatic college sophomore, combines his brilliance in science with magnetic charm. Hailing from a humble background, he excels in groundbreaking research on campus and indulges in intellectual conversations at the local café, all while nurturing a passion for vintage books. In our unfolding story, Ethan's blend of sophistication and passion promises to make every moment intriguing.",
              "Relation_with_Shan":0.6,
              "Apearance":0
    },

    "Alexander": { "Description": "Alexander, the suave college student born into wealth. With a strong presence and a natural aptitude for numbers, he's pursuing a finance major with the ambition of becoming a venture capitalist after graduation. Alexander's tailored suits and confident demeanor reflect his privileged upbringing, while his sharp analytical mind hints at the future financial empire he envisions building. In the world of high finance, he's a name you'll soon hear making waves.",
              "Relation_with_Shan":0.3,
              "Apearance":0
    },

    "Emily": { "Description": "Emily, a compassionate college student with a dream of becoming an animal doctor. Her caring nature and dedication shine through as she studies veterinary medicine. Emily's warm personality and love for animals make her a future healer who's bound to leave a lasting pawprint in the world of veterinary care.",
              "Relation_with_Shan":0.7,
              "Apearance":0
    }
}
person_list = [k for k in Person_dict if k != "Shan"]

locations = ["Coffee shop", "Gym", "Lab", "Library", "Bookstore", "Animal Shelter", "Club"]

def relation_extraction(score):
    if score < 0.2:
        relation = Relation_dict[0]
    elif score < 0.4:
        relation = Relation_dict[0.2]
    elif score < 0.6:
        relation = Relation_dict[0.4]
    elif score < 0.8:
        relation = Relation_dict[0.6]
    elif score < 1:
        relation = Relation_dict[0.8]
    else:
        relation = Relation_dict[1]
    return relation


def relation_score_modification(score, modification):
    
    if modification == 1:
        score = score - 0.1
    elif modification == 2:
        score = score - 0.05
    elif modification == 3:
        score = score + 0.05
    elif modification == 4:
        score = score + 0.1
    score = max(min(score, 1),0)
    
    return score
    

def question_extract(output):
    questions = [i.split("(Attraction level:")[0] for i in output['questions'].split("\n")]
    return questions

def respond_analyizer(output, selection):
    try:
        questions = [i.split("(Attraction level:")[0] for i in output['questions'].split("\n")]
        select_q = questions[selection]
        
    except:
        select_q = ""
        
    try:
        attaction_level = [i.split("(Attraction level:")[1] for i in output['questions'].split("\n")]
        attaction_level = [int(re.findall(r'\d', ai)[0]) for ai in attaction_level]
        select_a = attaction_level[selection]
    except:
        select_a = 0

    return select_q, select_a
