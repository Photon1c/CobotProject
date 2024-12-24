#All in one script

#Import modules
import json
import sys
import tinytroupe
from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld, TinySocialNetwork
from tinytroupe.examples import *
from tinytroupe.factory import TinyPersonFactory
from dotenv import load_dotenv
#sys.path.append('..') #adjust as necessary

load_dotenv()

#Create TinyPeople
boardroom = TinyPersonFactory("A global bank headquarters.")
CEO = boardroom.generate_person("Create a person that is a CEO of a major world bank.")
CFO = boardroom.generate_person("Create a person that is a CFO of a major world bank.")
CIO = boardroom.generate_person("Create a person that is a CIO of a major world bank.")
COO = boardroom.generate_person("Create a person that is a COO of a major world bank.")
MD = boardroom.generate_person("Create a person that is the marketing director of a major world bank.")

world = TinyWorld("An executive boardroom", [CEO, CFO, CIO, COO, MD])
world.make_everyone_accessible()

CEO.think_and_act("Discuss the top 4 major geopolitical events for January 2025.")
world.run(8)
