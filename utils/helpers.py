def range2(we, he, ws=0, hs=0):
	return [(x, y) for x in range(ws, we) for y in range(hs, he)]

def in_bounds(x, y):
	return (x > -1 and x < 8 and y > -1 and y < 8)

OPPOSITE = {1:2, 2:1}
nexts = [[-1,0],[-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1]]