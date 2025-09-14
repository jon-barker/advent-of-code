input = 'hepxcrrq' # Part I
# input = 'hepxxyzz' # Part II

valid_alphabet = 'abcdefghjkmnpqrstuvwxyz'
valid_alphabet_ind = {c:i for (i, c) in enumerate(valid_alphabet)}

def check_pairs(s_in):
  # O(n) method for checking there are two
  # non-overlapping pairs of repeated chars
  # it's unclear whether the pairs two non-overlapping
  # pairs can be the same letter. here we assume no.
  prev = s_in[0]
  found = 0
  used = []
  for c in s_in[1:]:
    if c == prev:
      found += 1
      prev = None
      used.append(c)
    elif c in used:
      pass
    else:
      prev = c
  if found == 2:
    return True
  return False

def check_straight(s_in):
  # O(n) method for checking if there's a three letter
  # straight
  for i, c in enumerate(s_in):
    if c in 'ghijklmnoyz':
      pass
    elif i > len(s_in) - 3: 
      return False
    elif (s_in[i+1] == valid_alphabet[valid_alphabet_ind[s_in[i]] + 1]) and (s_in[i+2] == valid_alphabet[valid_alphabet_ind[s_in[i]] + 2]): 
      return True
  

def increment_password(s_in):
  s_in = list(s_in)
  done = False
  c_idx = len(s_in) - 1
  while not done:
    c_inc = valid_alphabet_ind[s_in[c_idx]] + 1
    if c_inc < len(valid_alphabet):
      done = True
      s_in[c_idx] = valid_alphabet[c_inc]
    else:
      s_in[c_idx] = valid_alphabet[0]
      c_idx -= 1 
  return ''.join(s_in)

found_new = False
while not found_new:
  input = increment_password(input)
  if check_straight(input) and check_pairs(input):
    found_new = True
print(input)
