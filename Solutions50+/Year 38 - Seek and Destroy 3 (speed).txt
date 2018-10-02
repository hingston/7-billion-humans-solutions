-- 7 Billion Humans (2053) --
-- 38: Seek and Destroy 3 --

-- Author: ansvonwa
-- Size: 43
-- Speed: 12
-- Speed Tests: 12, 11, 12, 12, 12
-- Success Rate: 81/125

step n
mem1 = set n
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
step n
mem2 = set n
if mem2 < mem1:
	mem1 = set mem2
endif
pickup mem1
a:
mem2 = nearest worker
if myitem == nothing or
 myitem > mem2:
	b:
	mem1 = nearest hole
	step mem1
endif
mem1 = nearest shredder
step mem1
mem2 = nearest worker
if mem2 < myitem:
	jump b
endif
if mem2 == nothing or
 myitem == [blank]:
	giveto mem1
endif
jump a


