#
 
A
r
c
h
i
t
e
c
t
u
r
e
 
D
o
c
u
m
e
n
t
a
t
i
o
n




#
#
 
S
y
s
t
e
m
 
L
a
y
e
r
s




#
#
#
 
P
r
e
s
e
n
t
a
t
i
o
n
 
L
a
y
e
r




L
o
c
a
t
e
d
 
i
n
 
t
h
e
 
c
l
i
e
n
t
 
d
i
r
e
c
t
o
r
y
.




H
a
n
d
l
e
s
 
U
I
 
a
n
d
 
a
c
c
e
s
s
i
b
i
l
i
t
y
.




#
#
#
 
A
P
I
 
L
a
y
e
r




L
o
c
a
t
e
d
 
i
n
 
t
h
e
 
s
e
r
v
e
r
 
d
i
r
e
c
t
o
r
y
.




P
r
o
v
i
d
e
s
 
R
E
S
T
 
e
n
d
p
o
i
n
t
s
.




#
#
#
 
B
u
s
i
n
e
s
s
 
L
a
y
e
r




L
o
c
a
t
e
d
 
i
n
 
t
h
e
 
s
e
r
v
e
r
 
d
i
r
e
c
t
o
r
y
.




C
o
n
t
a
i
n
s
 
a
p
p
l
i
c
a
t
i
o
n
 
r
u
l
e
s
 
a
n
d
 
v
a
l
i
d
a
t
i
o
n
.




#
#
#
 
D
a
t
a
 
L
a
y
e
r




R
e
s
e
r
v
e
d
 
f
o
r
 
f
u
t
u
r
e
 
d
a
t
a
b
a
s
e
 
i
n
t
e
g
r
a
t
i
o
n
.




#
#
#
 
T
e
s
t
 
L
a
y
e
r




L
o
c
a
t
e
d
 
i
n
 
t
h
e
 
t
e
s
t
 
d
i
r
e
c
t
o
r
y
.




V
a
l
i
d
a
t
e
s
 
a
p
p
l
i
c
a
t
i
o
n
 
b
e
h
a
v
i
o
u
r
.




#
#
 
D
e
p
e
n
d
e
n
c
y
 
D
i
r
e
c
t
i
o
n




C
l
i
e
n
t


 
 
-
>
 
R
E
S
T
 
A
P
I


 
 
-
>
 
B
u
s
i
n
e
s
s
 
L
o
g
i
c


 
 
-
>
 
D
a
t
a
 
A
c
c
e
s
s


 
 
-
>
 
D
a
t
a
b
a
s
e




T
h
e
 
c
l
i
e
n
t
 
m
u
s
t
 
n
o
t
 
d
i
r
e
c
t
l
y
 
a
c
c
e
s
s
 
t
h
e
 
d
a
t
a
b
a
s
e
.