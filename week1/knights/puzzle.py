from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

players = ["A", "B", "C"]

knowledge = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave)
)
for player in players:
    knowledge.add(Not(And(Symbol(f"{player}Knight"),Symbol(f"{player}Knave"))))
    
    
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledge, 
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledge,
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledge,
    Implication(AKnight, Or(And(AKnight,BKnave), And(AKnave,BKnave))),
    Implication(AKnave, Not(Or(And(AKnight,BKnave), And(AKnave,BKnave)))),
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# A Knight, B Knave, C Knight
knowledge3 = And(
    knowledge,

    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # B says "A said 'I am a knave'."
    Implication(BKnight, Implication(AKnight, AKnave)),
    Implication(BKnave, Implication(AKnave, Not(AKnave))),
    
    # B says "C is a knave."
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    
    # C says "A is a knight."
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
