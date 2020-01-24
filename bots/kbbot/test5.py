import sys
from kb import KB, Boolean, Integer, Constant

# Define our propositional symbols
# J1 is true if the card with index 1 is a jack, etc
# You need to initialise all variables that you need for you strategies and game knowledge.
# Add those variables here.. The following list is complete for the Play Jack strategy.

"""
  	            Aces  10s 	Kings 	Queens 	Jacks
        Clubs 	  0    1 	  2 	  3 	  4
        Diamonds  5    6 	  7 	  8 	  9
        Hearts 	 10   11 	 12 	 13 	 14
        Spades 	 15   16 	 17 	 18 	 19
"""

C0 = Boolean('c0')
C1 = Boolean('c1')
C2 = Boolean('c2')
C3 = Boolean('c3')
C4 = Boolean('c4')
C5 = Boolean('c5')
C6 = Boolean('c6')
C7 = Boolean('c7')
C8 = Boolean('c8')
C9 = Boolean('c9')
C10 = Boolean('c10')
C11 = Boolean('c11')
C12 = Boolean('c12')
C13 = Boolean('c13')
C14 = Boolean('c14')
C15 = Boolean('c15')
C16 = Boolean('c16')
C17 = Boolean('c17')
C18 = Boolean('c18')
C19 = Boolean('c19')
PC0 = Boolean('pc0')
PC1 = Boolean('pc1')
PC2 = Boolean('pc2')
PC3 = Boolean('pc3')
PC4 = Boolean('pc4')
PC5 = Boolean('pc5')
PC6 = Boolean('pc6')
PC7 = Boolean('pc7')
PC8 = Boolean('pc8')
PC9 = Boolean('pc9')
PC10 = Boolean('pc10')
PC11 = Boolean('pc11')
PC12 = Boolean('pc12')
PC13 = Boolean('pc13')
PC14 = Boolean('pc14')
PC15 = Boolean('pc15')
PC16 = Boolean('pc16')
PC17 = Boolean('pc17')
PC18 = Boolean('pc18')
PC19 = Boolean('pc19')




# Create a new knowledge base
kb = KB()

# strategy: plays cheap card first (J, Q, K)
# This adds information which cards are Cheap
kb.add_clause(C2)
kb.add_clause(C3)
kb.add_clause(C4)
kb.add_clause(C7)
kb.add_clause(C8)
kb.add_clause(C9)
kb.add_clause(C12)
kb.add_clause(C13)
kb.add_clause(C14)
kb.add_clause(C17)
kb.add_clause(C18)
kb.add_clause(C19)

# all x PC(x) <-> C(x) => ~C | PC, ~PC | C
kb.add_clause(~C2, PC2)
kb.add_clause(~C3, PC3)
kb.add_clause(~C4, PC4)
kb.add_clause(~C7, PC7)
kb.add_clause(~C8, PC8)
kb.add_clause(~C9, PC9)
kb.add_clause(~C12, PC12)
kb.add_clause(~C13, PC13)
kb.add_clause(~C14, PC14)
kb.add_clause(~C17, PC17)
kb.add_clause(~C18, PC18)
kb.add_clause(~C19, PC19)
kb.add_clause(~PC2, C2)
kb.add_clause(~PC3, C3)
kb.add_clause(~PC4, C4)
kb.add_clause(~PC7, C7)
kb.add_clause(~PC8, C8)
kb.add_clause(~PC9, C9)
kb.add_clause(~PC12, C12)
kb.add_clause(~PC13, C13)
kb.add_clause(~PC14, C14)
kb.add_clause(~PC17, C17)
kb.add_clause(~PC18, C18)
kb.add_clause(~PC19, C19)

# print all models of the knowledge base
for model in kb.models():
    print(model)

# print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
