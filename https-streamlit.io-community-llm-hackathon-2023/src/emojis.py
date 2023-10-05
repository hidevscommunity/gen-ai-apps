# emojis
class Common:
    pass

class Emojis(Common):
    def __init__(self):
        pass
    ideas = {
        "📥🔗📜" : "A new way to express The input that you process With emojis that impress And convey more with less",
        "🖼️📷" : "A challenge to achieve The image that you perceive With cameras that retrieve And frames that interweave",
        "👏👏👏"  : "A praise for your creation The emoji translation With innovation and imagination And a poetic celebration" ,
        "📥" :{ "type": "input"},
        
        "🔗" : { "url": "<URL>" },
        "📜" : { "value" : "<VALUE>" }

    }
    reversed = {
        "A": "🅰️",
        "new": "🆕",
        "way": "🛤️",
        "to": "🔄",
        "express": "🗣️",
  "The": "🌟",
  "input": "📥",
  "that": "🤔",
  "you": "👉",
  "process": "🔄",
  "With": "👁️‍🗨️",
  "emojis": "😀🌈",
  "impress": "🤩",
  "And": "➕",
  "convey": "📢",
  "more": "🔝",
  "with": "➖",
  "less": "👌",
  "challenge": "🏆",
  "achieve": "🏅",
  "image": "🖼️",
  "perceive": "👁️",
  "cameras": "📷📸",
  "retrieve": "🔍",
  "frames": "🖼️",
  "interweave": "🔄🔀",
  "praise": "👏👏",
  "for": "👉",
  "your": "👨‍🎨👩‍🎨",
  "creation": "🎨",
  "emoji": "😃🎉",
  "translation": "🔠➡️",
  "innovation": "🚀💡",
  "and": "🔗",
  "imagination": "🧠💭",
  "a": "🅰️",
  "poetic": "✍️📜",
  "celebration": "🥳🎉",
  "type": "🖋️",
  "url": "🌐🔗",
  "<URL>": "🌐🔗",
  "value": "💎",
  "<VALUE>": "💎"
}

    # emit new source code with new constants
    # save in session save buffer
    def prompt_model(self, text):
        for x in ["Create prompt model that will ",
                  "Construct a prompt that will have the effect of ",
                  "Imagine instructions will have the effect of ",
                  "Instructions for",
                  "Instructions about",
                  "Structure of",
                  "Math behind",
                  "Symbols behind",
                  "Terms behind",
                  "Key Terms behind",
                  "Find Key Concepts behind",
                  "Find Bugs contained",
                  "Find Syntax contained",
                  "Find Tokens contained",
                  "Write missing documentation",
                  "Write missing todos",
                  "Flag missing issues",
                  "Warn user about issues found in",
                  "Find security issues in",
                  "Flag security issues in",
                  "Escalate security issues in",
                  "Patch security issues in",
                  "Contain security issues in",
                  "Communicate responsibly security issues in",
                  "Redact private data found in",
                  "Find High entropy contained",
                  "Rewrite in python",
                  "Rewrite in typescript",
                  "Rewrite in as formal proof",
                  "Rewrite in as formal math",
                  "Rewrite in as formal restatement",
                  "Rewrite in as formal conjecture",
                  "Rewrite in Haskel",
                  "Rewrite in bash",
                  "Rewrite in json",
                  "Rewrite in yaml",
                  "Rewrite in emojis",
                  "Rewrite in coq",
                  "Find Key Concepts behind",
                  "Find Bugs contained",
                  "Find Syntax contained",
                  "Find Tokens contained",
                  "Find Keys contained",
                  "Find High entropy contained",
                  "Deep embedded knowledge inside",
                  "Key Concepts hidden inside of",
                  "Occult Knowledge hidden inside of",
                  "Obscured  Knowledge hidden inside of",
                  "Expression in emojis of",
                  "Rewriting using emojis of",
                  "Creative Rewriting using emojis for",
                  "Creative Rewriting using emojis instead of words for",
                  "Using emojis instead of words of",
                  "Using emojis instead of words for",
                  "Construction of",
                  "Deconstruction of",
                  "Reconstruction of",
                  "Refactoring of",
                  "Rewriting of",
                  "Formal reepression of",
                  "Summary of",
                  "Snarks found in",
                  "Universal concepts found in",
                  "Deep knowledge found in",
                  "Emoji Deconstruction of",
                  "Emoji Reconstruction of",
                  "Hackathonization of",
                  "Epic poem about",
                  "Epic poem using the muses as inspiration about",
                  "an Ode to",
                  "a quine about",
                  "a self referential statement about",
                  "a self referential buffer containing",
                  "a self referential tensor containing",
                  "a self referential matrix containing",
                  "a self referential array containing",
                  "a self referential goedel number containing",
                  "an autopoetic self referential goedel number quine relay containing",
                  "an autopoetic self referential goedel number heidegarian quine relay containing",
                  "Metaphorical Deconstruction of",
                  "Metaphorical Emoji Reconstruction of",
                  "Metaphorical Reconstruction of",
                  "Critical Reconstruction of"]:
            yield { "combine" : [ x,text] }
            
    def lookup_ai(self,term, **args):
        yield from self.prompt_model(f"define the {term} with args {args} using example :'''{{data.text.raw}}'''")
    
    def lookup_emoji(self,x):
        if not isinstance(x,str):
            return
        if x in self.ideas:
            return #have it
        
        if x not in self.reversed:
            yield from self.lookup_ai("We need an Emoji")
            yield from self.lookup_ai(f"Rewrite using emojis the term '{x}'")
            yield from self.lookup_ai(f"Rewrite as emojis the idea '{x}'")
            yield from self.lookup_ai(f"Rewrite as python the idea '{x}'")
            yield from self.lookup_ai(f"Rewrite as math the idea '{x}'")        
            yield from self.lookup_ai(f"Consider the meaning of the term '{x}'")        
            yield from self.lookup_ai(f"Generate a Prompt to help find out the answer to the question of what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"help find out the answer to the question of what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"what are some possible new Emojis for {x}?")
            yield from self.lookup_ai(f"What are some Emojis for {x}?")        
            self.reversed[x] = "TODO"
    
    def process(self):
        # \'{data.text.raw}\'
        prmt= self.prompt_model(f"Answer the following question: What is the meaning of following Emoji: '''{{data.text.raw}}'''")
        
        for e in self.ideas:
            #st.write(e)
            yield from  self.lookup_ai(prmt,**{"emoji":e})            
            v = self.ideas[e]
            if isinstance(v,str):
                for x in v.split():
                    #st.write(e, x)
                    self.lookup_emoji(e)
                    self.lookup_emoji(x)
            elif isinstance(v,dict): #could be a word
                for k in v: #key name
                    v2 = v[k] #can be dic
                    if isinstance(v2, dict):
                        for k2 in v2:
                            v3 = v2[k2] # thied level
                            for a in [e, v, k, v2, k2, v3]:
                                self.lookup_emoji(a)

                            #st.write(e, v, k, v2, k2, v3)
                    else:
                        #st.write(e, v, k, v2)
                        pass
            #for a in [e, v, k, v2]:
            #    lookup_emoji(a)
        else:        
            for x in self.ideas[e]:
                #st.write(e, x)
                for a in [e, x]:
                    self.lookup_emoji(a)

    def load_data(self):
        dataset = []
        text_data = resources_pb2.Text(raw=fstr)
        data = resources_pb2.Data(text=text_data)
        input_proto = resources_pb2.Input(
            data=data,
        )
        dataset.append(input_proto)
        return dataset
    
def main():
    m  = Emojis()
    for x in m.process():
        print(x)
#models = {

#    "App": Apps(),
#    "DataSet": DataSets(),
#    "PythonGlobals": Globals(),
#    "PythonTypes": Types(),
#    "PythonAsts": Asts(),
#}
if __name__ == "__main__" :
    main()
