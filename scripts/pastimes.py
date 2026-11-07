import sys, random, json, itertools, chess
seed = int(sys.argv[1].replace("-","")); rnd = random.Random(seed)
# ---------- chess mate-in-two ----------
def mate_in_one(b):
    for m in b.legal_moves:
        b.push(m); ok = b.is_checkmate(); b.pop()
        if ok: return True
    return False
def forces_mate2(b, m):
    b.push(m)
    if b.is_checkmate() or b.is_stalemate() or not list(b.legal_moves): b.pop(); return False
    reps = 0
    for r in list(b.legal_moves):
        b.push(r)
        if not mate_in_one(b): b.pop(); b.pop(); return False
        b.pop(); reps += 1
    b.pop(); return reps >= 2
def chess_problem():
    while True:
        b = chess.Board(None); sq = list(chess.SQUARES); rnd.shuffle(sq); it = iter(sq)
        b.set_piece_at(next(it), chess.Piece(chess.KING, chess.WHITE)); b.set_piece_at(next(it), chess.Piece(chess.KING, chess.BLACK))
        for _ in range(rnd.randint(2,4)):
            b.set_piece_at(next(it), chess.Piece(rnd.choice([chess.QUEEN,chess.ROOK,chess.ROOK,chess.BISHOP,chess.KNIGHT,chess.PAWN]), chess.WHITE))
        for _ in range(rnd.randint(0,2)):
            b.set_piece_at(next(it), chess.Piece(rnd.choice([chess.PAWN,chess.KNIGHT,chess.BISHOP,chess.ROOK]), chess.BLACK))
        for s in chess.SQUARES:
            p = b.piece_at(s)
            if p and p.piece_type == chess.PAWN and chess.square_rank(s) in (0,7): b.remove_piece_at(s)
        b.turn = chess.WHITE
        if not b.is_valid() or b.is_check() or b.is_game_over(): continue
        if mate_in_one(b): continue
        keys = [m for m in b.legal_moves if forces_mate2(b, m)]
        if len(keys) != 1: continue
        k = keys[0]
        if b.is_capture(k) or b.gives_check(k) or b.piece_at(k.from_square).piece_type == chess.KING: continue
        return b, k
b, key = chess_problem()
san = b.san(key)
G = {'K':('♔','♚'),'Q':('♕','♛'),'R':('♖','♜'),'B':('♗','♝'),'N':('♘','♞'),'P':('♙','♟')}
cells = []
for r in range(7,-1,-1):
    for f in range(8):
        s = chess.square(f,r); dark = (f+r)%2==0
        x, y = f*40, (7-r)*40
        cells.append(f'<rect x="{x}" y="{y}" width="40" height="40" fill="{"#d9c59a" if dark else "#f7f0dd"}"/>')
        p = b.piece_at(s)
        if p:
            o, sol = G[p.symbol().upper()]
            if p.color == chess.WHITE:
                cells.append(f'<text x="{x+20}" y="{y+31}" font-size="32" text-anchor="middle" font-family="DejaVu Sans" fill="#fffdf4">{sol}</text><text x="{x+20}" y="{y+31}" font-size="32" text-anchor="middle" font-family="DejaVu Sans" fill="#2b2118">{o}</text>')
            else:
                cells.append(f'<text x="{x+20}" y="{y+31}" font-size="32" text-anchor="middle" font-family="DejaVu Sans" fill="#2b2118">{sol}</text>')
files = ''.join(f'<text x="{f*40+20}" y="344" font-size="10" text-anchor="middle" fill="#6b5a3c" font-family="serif">{"abcdefgh"[f]}</text>' for f in range(8))
ranks = ''.join(f'<text x="-8" y="{(7-r)*40+24}" font-size="10" text-anchor="middle" fill="#6b5a3c" font-family="serif">{r+1}</text>' for r in range(8))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -4 348 358" ><rect x="-1" y="-1" width="322" height="322" fill="none" stroke="#7a5c2e" stroke-width="2"/>{"".join(cells)}{files}{ranks}</svg>'
# reply-check: list defenses with mating second move
sol_lines = []
b.push(key)
for r in b.legal_moves:
    rs = b.san(r); b.push(r)
    for m in b.legal_moves:
        b.push(m)
        if b.is_checkmate(): b.pop(); sol_lines.append(f"{rs} {b.san(m)}"); break
        b.pop()
    b.pop()
b.pop()
# ---------- logic puzzle ----------
cats = {"Name":["Ada","Ben","Cora","Dale"],"Pet":["cat","dog","hen","pig"],"Drink":["tea","milk","cider","water"]}
catn = list(cats)
perms = list(itertools.permutations(range(4)))
sol = {c: rnd.choice(perms) for c in catn}  # sol[c][i] = item index at house i
def val(c,i): return cats[c][sol[c][i]]
def pos(c, item): return list(sol[c]).index(cats[c].index(item))
def clues_pool():
    P = []
    for c1 in catn:
        for c2 in catn:
            if c1 >= c2: continue
            for i in range(4):
                a, bb = val(c1,i), val(c2,i)
                P.append(("same",c1,a,c2,bb,f"The {c1.lower() if c1!='Name' else ''} {a} " if False else None))
    return P
def mk():
    out = []
    items = [(c,x) for c in catn for x in cats[c]]
    for (c1,a),(c2,bb) in itertools.permutations(items,2):
        if c1 == c2: continue
        p1, p2 = pos(c1,a), pos(c2,bb)
        if p1 == p2: out.append(("same",(c1,a),(c2,bb)))
        else: out.append(("not",(c1,a),(c2,bb)))
        if abs(p1-p2)==1: out.append(("next",(c1,a),(c2,bb)))
        if p1 < p2: out.append(("left",(c1,a),(c2,bb)))
    for c,x in items: out.append(("at",(c,x),pos(c,x)+1))
    return out
pool = mk()
def holds(cl, asg):  # asg: cat -> perm (house->item index)
    t = cl[0]
    def P(c,x): return list(asg[c]).index(cats[c].index(x))
    if t=="at": return P(*cl[1])==cl[2]-1
    p1,p2 = P(*cl[1]),P(*cl[2])
    return {"same":p1==p2,"not":p1!=p2,"next":abs(p1-p2)==1,"left":p1<p2}[t]
def count(cls, limit=2):
    n = 0
    for a in perms:
        for b2 in perms:
            for c3 in perms:
                asg = {catn[0]:a,catn[1]:b2,catn[2]:c3}
                if all(holds(c,asg) for c in cls):
                    n += 1
                    if n >= limit: return n
    return n
def desc(x): c,i = x; return {"Name":f"{i}","Pet":f"the {i}","Drink":f"the {i}"}[c]
def say(cl):
    t=cl[0]
    def who(x):
        c,i = x
        return {"Name":i,"Pet":f"whoever keeps the {i}","Drink":f"whoever drinks {i}"}[c]
    if t=="at": return f"{who(cl[1])[0].upper()+who(cl[1])[1:]} lives in house {cl[2]}."
    A,B = who(cl[1]), who(cl[2])
    A = A[0].upper()+A[1:]
    return {"same":f"{A} is {B}." if cl[1][0]=="Name" else f"{A} is {B}.",
            "not":f"{A} is not {B}.","next":f"{A} lives next door to {B}.","left":f"{A} lives somewhere to the left of {B}."}[t]
# keep only clues not trivially same-category; build greedily
rnd.shuffle(pool)
chosen = []
for cl in pool:
    chosen.append(cl)
    if count(chosen) == 1: break
# prune redundant
i = 0
while i < len(chosen):
    t = chosen[:i]+chosen[i+1:]
    if count(t) == 1: chosen = t
    else: i += 1
assert count(chosen) == 1
# question: pick target not answerable from a single clue
import copy
q_cat, q_item = "Pet", rnd.choice(cats["Pet"]); ask = "Drink"
ans = val(ask, pos("Pet", q_item))
grid = {c: [val(c,i) for i in range(4)] for c in catn}
print(json.dumps({"chess_svg": svg, "chess_title": "Mate in Two", "chess_prompt": "White to move and checkmate in two moves, against any defence.",
 "chess_solution": f"Key move: {san}. Then {', '.join(sol_lines)}.",
 "logic_title": "The Four Houses",
 "logic_intro": "Four houses stand in a row, numbered 1 to 4 from the left. Each has a different resident (Ada, Ben, Cora, Dale), a different pet (cat, dog, hen, pig), and a different favourite drink (tea, milk, cider, water).",
 "logic_clues": [say(c) for c in chosen],
 "logic_question": f"Who drinks what, and in which house? Specifically: what does whoever keeps the {q_item} drink?",
 "logic_answer": f"The keeper of the {q_item} drinks {ans}. Full solution: " + "; ".join(f"House {i+1}: {grid['Name'][i]}, {grid['Pet'][i]}, {grid['Drink'][i]}" for i in range(4)) + "."}))
