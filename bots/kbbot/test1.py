import sys
from kb import KB, Boolean, Integer, Constant

# Define our symbols
P = Boolean('P')
Q = Boolean('Q')
R = Boolean('R')
#D = Boolean('D')

# Create a new knowledge base
kb = KB()

# Add clauses

# KB:
# {(P v Q)
# (Q -> R) => -Q | R
# (R -> -P)} => -R | -P


kb.add_clause(~P, Q)
kb.add_clause(~Q, R)
kb.add_clause(~R, ~P)

# alpha: (P <-> - Q) => P -> -Q & -Q -> P =>
# -P | -Q
# Q | P

# -alpha: -((-P | -Q) & (Q | P)) => -(-P|-Q) | -(Q|P) => (P & Q) | (-Q & -P) => (P|-Q),(P|-P),(Q|-Q),(Q|-P)
kb.add_clause(P, ~Q)
kb.add_clause(Q, ~P)


# Print all models that satisfy the knowledge base
for model in kb.models():
    print(model)

# Print out whether the KB is satisfiable (if there are no models, it is not satisfiable)
print(kb.satisfiable())
