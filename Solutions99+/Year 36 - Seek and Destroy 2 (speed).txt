-- 7 Billion Humans (2053) --
-- 36: Seek and Destroy 2 --

-- Author: ansvonwa
-- Size: 195
-- Speed: 50
-- Speed Tests: 50, 50, 50

a:
step n
mem1 = set n
if mem1 == nothing:
	jump a
endif
b:
step n
mem2 = set n
if mem2 == nothing:
	jump b
endif
if mem2 < mem1:
	mem3 = set mem1
	mem1 = set mem2
	mem2 = set mem3
endif
c:
step n
mem3 = set n
if mem3 == nothing:
	jump c
endif
if mem3 < mem2:
	if mem3 < mem1:
		mem4 = set mem3
		mem3 = set mem2
		mem2 = set mem1
		mem1 = set mem4
	else:
		mem4 = set mem3
		mem3 = set mem2
		mem2 = set mem4
	endif
endif
step n
mem4 = set n
if mem4 < mem2:
	if mem4 < mem1:
		mem3 = set mem2
		mem2 = set mem1
		mem1 = set mem4
	else:
		mem3 = set mem2
		mem2 = set mem4
	endif
else:
	if mem4 < mem3:
		mem3 = set mem4
	endif
endif
step n
mem4 = set n
if mem4 <= mem3:
	if mem4 < mem2:
		if mem4 < mem1:
			mem3 = set mem2
			mem2 = set mem1
			mem1 = set mem4
		else:
			mem3 = set mem2
			mem2 = set mem4
		endif
	else:
		if mem4 < mem3:
			mem3 = set mem4
		endif
	endif
endif
step n
mem4 = set n
if mem4 <= mem3:
	if mem4 < mem2:
		if mem4 < mem1:
			mem3 = set mem2
			mem2 = set mem1
			mem1 = set mem4
		else:
			mem3 = set mem2
			mem2 = set mem4
		endif
	else:
		if mem4 < mem3:
			mem3 = set mem4
		endif
	endif
else:
	if n == nothing:
		step n
		if n == datacube:
			jump d
		endif
		step n
	endif
endif
step n
d:
mem4 = set n
if mem4 <= mem3:
	if mem4 < mem2:
		if mem4 < mem1:
			mem3 = set mem2
			mem2 = set mem1
			mem1 = set mem4
		else:
			mem3 = set mem2
			mem2 = set mem4
		endif
	else:
		if mem4 < mem3:
			mem3 = set mem4
		endif
	endif
endif
pickup mem1
mem1 = nearest shredder
giveto mem1
pickup mem2
giveto mem1
pickup mem3
giveto mem1
if mem4 == datacube and
 mem4 != mem3:
	step mem4
	mem1 = set mem4
	e:
	mem2 = set s
	if mem2 == nothing:
		step s
		jump e
	endif
	if mem1 > mem2:
		mem4 = set mem1
		mem1 = set mem2
		mem2 = set mem4
	else:
		if mem2 == shredder:
			jump f
		endif
	endif
	g:
	step s
	mem3 = set s
	if mem3 == nothing:
		jump g
	endif
	if mem3 < mem2:
		mem4 = set mem3
		mem3 = set mem2
		if mem4 < mem1:
			mem2 = set mem1
			mem1 = set mem4
		else:
			mem2 = set mem4
		endif
	else:
		if mem3 == shredder:
			jump h
		endif
	endif
	i:
	step s
	mem4 = set s
	if mem4 == nothing:
		jump i
	endif
	if mem4 < mem2:
		if mem4 < mem1:
			mem4 = set mem3
			mem3 = set mem2
			mem2 = set mem1
			mem1 = set s
		else:
			mem4 = set mem3
			mem3 = set mem2
			mem2 = set s
		endif
	else:
		if mem4 < mem3:
			mem4 = set mem3
			mem3 = set s
		endif
	endif
else:
	j:
	step n
	mem1 = set n
	if mem1 == nothing:
		jump j
	endif
	k:
	step n
	mem2 = set n
	if mem2 == nothing:
		jump k
	endif
	if mem2 < mem1:
		mem3 = set mem1
		mem1 = set mem2
		mem2 = set mem3
	endif
	l:
	step n
	mem3 = set n
	if mem3 == nothing:
		jump l
	endif
	if mem3 < mem2:
		if mem3 < mem1:
			mem4 = set mem3
			mem3 = set mem2
			mem2 = set mem1
			mem1 = set mem4
		else:
			mem4 = set mem3
			mem3 = set mem2
			mem2 = set mem4
		endif
	endif
	m:
	step n
	mem4 = set n
	if mem4 == nothing:
		jump m
	endif
	if mem4 < mem3:
		if mem4 < mem2:
			if mem4 < mem1:
				mem4 = set mem3
				mem3 = set mem2
				mem2 = set mem1
				mem1 = set n
			else:
				mem4 = set mem3
				mem3 = set mem2
				mem2 = set n
			endif
		else:
			mem4 = set mem3
			mem3 = set n
		endif
	endif
	f:
	h:
endif
pickup mem1
mem1 = nearest shredder
giveto mem1
pickup mem2
giveto mem1
pickup mem3
giveto mem1
pickup mem4
giveto mem1



