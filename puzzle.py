from curses import keyname
from imp import IMP_HOOK
from logic import *

AKnight = Symbol("A is a Knight") #A is a knight
AKnave = Symbol("A is a Knave") #A is a knave

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # if a is a knight then a is both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    # a is a knight or a knave
    Or(AKnight, AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Implication(AKnave, Or(AKnave, BKnave)),
    Or(AKnave, BKnave),
    Implication(BKnave, AKnave),
    Or(BKnight, AKnave),
    Or(AKnight, BKnave),

    Implication(AKnave, BKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

sent2A = Or(And(AKnight,BKnight),And(AKnave,BKnave)) # saying they are the same
sent2B = Or(And(AKnight,BKnave),And(AKnave,BKnight)) # saying they are diff

knowledge2 = And(
    # TODO

    # general knowledge:
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight, CKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # puzzle knowledge
    Biconditional(AKnight, sent2A),
    Biconditional(BKnight, sent2B)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

sent3A = Or(AKnight, BKnave)
sent3B1 = And(AKnight, BKnave)
sent3B2 = And(BKnight, CKnave)
sent3C = And(CKnight, AKnight)

knowledge3 = And(
    # TODO

    # AKnight,
    # BKnave,
    # CKnight


    # general knowledge:
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Or(CKnight, CKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # puzzle knowledge:
    Biconditional(BKnight, And(sent3B1, sent3B2)),
    Implication(BKnave, CKnight),
    Biconditional(CKnight, AKnight)
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
