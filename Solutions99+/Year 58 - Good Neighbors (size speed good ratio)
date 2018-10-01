-- 7 Billion Humans (2053) --
-- 58: Good Neighbors --
 mem1 = nearest wall
step mem1
if n == wall and
 w != worker and
 e != worker:
	step e
	mem1 = nearest datacube
	a:
	pickup mem1
	mem1 = set s
	step n
	step n
	step n
	drop
	jump a
endif
if s == wall and
 e != worker:
	mem1 = nearest datacube
	b:
	pickup mem1
	if w == worker:
		drop
		end
	endif
	mem1 = set n
	step s
	step s
	step s
	drop
	jump b
endif
