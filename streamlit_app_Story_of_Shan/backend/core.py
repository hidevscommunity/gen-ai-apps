import os
from typing import Any, List, Dict

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from langchain.chains import ConversationalRetrievalChain
#from langchain.vectorstores import Pinecone
#import pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

from langchain.llms import OpenAI

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

import numpy as np
from consts import INDEX_NAME

from backend.helper import Relation_dict, Person_dict, locations,  relation_extraction, relation_score_modification, respond_analyizer


story_0 = """Working at a coffee shop during my sophomore summer break, I observed Jake, a college sophomore. He's an adrenaline-loving skateboarder, a vinyl record aficionado, and a stand-up comedy enthusiast. Amid the coffee shop's cozy ambiance, Jake, with a charming grin, mistook me for a fellow economics classmate, sparking an unexpected reunion.
                        He said, "Give me an Americano, please." Then, with a surprised grin, he exclaimed, "Isn't this Shan? We took an economics class together!"
                        """

respond_list_0 = [
"I don't know you." ,
"Who are you?" ,
"It's me." ,
"Surprised, but intrigued." ] 
respond_list_score_0 = [
1 ,
2 ,
3 ,
4] 
character_0 = "Jake"

class Shan_Story_LLM_Core:

    def __init__(self):
        pass


    def iniciate_llm(self):

        llm = OpenAI(temperature=.7)

        # This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
        summary_template = """
        Imagine you are a AI novel writer and summize past stories

        history: {history}

        Write Story: Write a summary about the history from first person view: 
        """
        summary_prompt_template = PromptTemplate(input_variables=["history"], template=summary_template)
        summary_chain = LLMChain(llm=llm, prompt=summary_prompt_template, output_key="history_summary")

        # This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
        story_template = """

        Imagine you are a AI novel writer and writing about Shan's story. 

        history: {history_summary}

        Shan: {human_input}
        Write Story: Continue the story from first person view and end before Shan need to respond. Make sure story ended with period: 
        """
        story_prompt_template = PromptTemplate(input_variables=["history_summary", "human_input"], template=story_template)
        story_chain = LLMChain(llm=llm, prompt=story_prompt_template, output_key="new_story")

        choice_template = """You are a AI novel writer and write about multiple choice questions. 

        history: {history_summary}

        new_story: {new_story}

        Example:
        Multiple Choice Selections:
        1. [Ignore him] (Attraction level: 1)
        2. "Who are you?" (Attraction level: 2)
        3. "It's me." (Attraction level: 3) 
        4. "Surprised, but intrigued." (Attraction level: 4)

        Create a multiple choice Selections from first person view based on this history and new story:
        Multiple Choice Selections:
        """
        choice_prompt_template = PromptTemplate(input_variables=["history_summary", "new_story"], template=choice_template)
        choice_chain = LLMChain(llm=llm, prompt=choice_prompt_template, output_key="questions")

        # This is the overall chain where we run these two chains in sequence.
        self.overall_chain = SequentialChain(
            chains=[summary_chain, story_chain, choice_chain],
            input_variables=["history", "human_input"],
            # Here we return multiple variables
            output_variables=["history_summary", "new_story", "questions"],
            verbose=True)

            

        # This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
        story_template = """

        Imagine you are a AI novel writer and writing about Shan's story at college. 

        history: {history_summary}

        Shan: {human_input}
        Write Story: End the story from first person view for today.
                    Provide a sense of closure and reflection.
                    Make sure story ended with period: 
        """
        endday_story_prompt_template = PromptTemplate(input_variables=["history_summary", "human_input"],
                                                    template=story_template)
        endday_story_chain = LLMChain(llm=llm, prompt=endday_story_prompt_template, output_key="new_story")

        # This is the overall chain where we run these two chains in sequence.
        self.endday_overall_chain = SequentialChain(
                                chains=[summary_chain, endday_story_chain],
                                input_variables=["history", "human_input"],
                                # Here we return multiple variables
                                output_variables=["history_summary", "new_story"],
                                verbose=True)


        # This is an LLMChain to write a synopsis given a title of a play and the era it is set in.
        story_template = """

        Imagine you are a AI novel writer and writing about Shan's story at college. 

        history: {history_summary}

        Shan: {human_input}
        Write Story: End the story from first person view for today.
                    Provide a sense of closure and reflection.
                    Make sure story ended with period: 
        """
        nextday_story_prompt_template = PromptTemplate(input_variables=["history_summary", "human_input"],
                                                    template=story_template)
        nextday_story_chain = LLMChain(llm=llm, prompt=nextday_story_prompt_template, output_key="new_story")

        # This is the overall chain where we run these two chains in sequence.
        self.nextday_overall_chain = SequentialChain(
                                chains=[summary_chain, nextday_story_chain],
                                input_variables=["history", "human_input"],
                                # Here we return multiple variables
                                output_variables=["history_summary", "new_story"],
                            verbose=True)





    def run_llm_selection_chain(self, chat_history,
                                selection , character, Person_dict
                                ) -> Any:


        score = Person_dict[character]['Relation_with_Shan']

        if len(chat_history) == 0:
            character= character_0
            respond, respond_score = respond_list_0[selection], respond_list_score_0[selection]
            score = relation_score_modification(score,respond_score)
            Person_dict[character]['Relation_with_Shan'] = score
            relation = relation_extraction(score)
            designed_respond = "Current Shan's relation with {} is {} and Shan have decided to responded: {}".format(character,
                                                                                                    relation,
                                                                                                    respond
                                                                                                    )
            output = self.overall_chain({"history": story_0, 
                                    "human_input": designed_respond})

        else:
            output = chat_history[-1]
            history = output["history_summary"] + output["new_story"]

            respond, respond_score =  respond_analyizer(output, selection)
            score = relation_score_modification(score,respond_score)
            Person_dict[character]['Relation_with_Shan'] = score
            relation = relation_extraction(score)
            designed_respond = "Current Shan's relation with {} is {} and Shan have decided to responded: {}".format(character,
                                                                                                    relation,
                                                                                                    respond
                                                                                                    )
            output = self.overall_chain({"history": history, 
                                    "human_input": designed_respond})

        return output #({"question": query, "chat_history": chat_history})




    def run_llm_end_story_chain( self, chat_history,
                                selection, character, Person_dict
                                ) -> Any:


        score = Person_dict[character]['Relation_with_Shan']

        output = chat_history[-1]
        history =  output["history_summary"] + output["new_story"]
        respond, respond_score =  respond_analyizer(output, selection)
        score = relation_score_modification(score,respond_score)
        Person_dict[character]['Relation_with_Shan'] = score
        relation = relation_extraction(score)
        designed_respond = "Current Shan's relation with {} is {} and Shan have decided to responded: {}".format(character,
                                                                                                relation,
                                                                                                respond
                                                                                                )
        output = self.nextday_overall_chain({"history":history, 
                                        "human_input":designed_respond})

        return output #({"question": query, "chat_history": chat_history})



    def run_llm_nextday_story_chain( self, chat_history,
                                selection, character, Person_dict
                                ) -> Any:

        location = np.random.choice(locations)

        score = Person_dict[character]['Relation_with_Shan']

        output = chat_history[-1]
        history =  output["history_summary"] + output["new_story"]
        #respond, respond_score =  respond_analyizer(output, selection)
        #score = relation_score_modification(score,respond_score)
        #Person_dict[character]['Relation_with_Shan'] = score
        
        Apearance = Person_dict[character]['Apearance']
        Description = Person_dict[character]['Description']
        relation = relation_extraction(score)
        if Apearance == 0:
            designed_respond = "{} [Shan begin a new day at  {} with a suprising encountering with {} and her current relation with him is {}.]. Begin the story describing how Shan met {}:".format(Description, location,
                        character, relation, character)
        else:
            designed_respond = "[Shan begin a new day at  {} with a suprising encountering with {} and her current relation with him is {}]. Begin the story describing how Shan met {}:".format(location,
                        character, relation, character)


        #designed_respond = "Current Shan's relation with {} is {} and Shan have decided to responded: {}".format(character,
        #                                                                                        relation,
        #                                                                                        respond
        #                                                                                        )
        output = self.nextday_overall_chain({"history":history, 
                                        "human_input":designed_respond})

        return output #({"question": query, "chat_history": chat_history})

