# This test requires CPython3.5
print(b"%%" % ())
print(b"=%d=" % 1)
print(b"=%d=%d=" % (1, 2))

print(b"=%s=" % b"str")
print(b"=%r=" % b"str")
