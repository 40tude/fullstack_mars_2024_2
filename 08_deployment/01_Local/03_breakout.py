import random 

lst = [
"Mario",
"Donkey Kong",
"Link",
"Samus",
"Yoshi",
"Kirby",
"Fox McCloud",
"Pikachu",
"Jigglypuff",
"Captain Falcon",
"Ness",
"Luigi",
]

len_lst = len(lst)
group_size = 5
nb_group = len_lst//group_size
nb_remaining_pers = len_lst%group_size

# random.shuffle(lst)

for g in range(nb_group):
  for p in range(group_size):
    print(lst[p+g*group_size])
  print()


i = 1 + g*group_size + p
while i<len_lst:
  print(lst[i])
  i +=1





  