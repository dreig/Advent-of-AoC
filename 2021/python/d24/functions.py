def block0(w, z):
    x = (z % 26 + 12) != w
    return (z // 1) * (25*x + 1) + (w+15)*x

def block1(w, z):
    x = (z % 26 + 14) != w
    return (z // 1) * (25*x + 1) + (w+12)*x

def block2(w, z):
    x = (z % 26 + 11) != w
    return (z // 1) * (25*x + 1) + (w+15)*x

def block3(w, z):
    x = (z % 26 - 9) != w
    return (z // 26) * (25*x + 1) + (w+12)*x

def block4(w, z):
    x = (z % 26 - 7) != w
    return (z // 26) * (25*x + 1) + (w+15)*x

def block5(w, z):
    x = (z % 26 + 11) != w
    return (z // 1) * (25*x + 1) + (w+2)*x

def block6(w, z):
    x = (z % 26 - 1) != w
    return (z // 26) * (25*x + 1) + (w+11)*x

def block7(w, z):
    x = (z % 26 - 16) != w
    return (z //  26) * (25*x + 1) + (w+15)*x

def block8(w, z):
    x = (z % 26 + 11) != w
    return (z // 1) * (25*x + 1) + (w+10)*x

def block9(w, z):
    x = (z % 26 - 15) != w
    return (z // 26) * (25*x + 1) + (w+2)*x

def block10(w, z):
    x = (z % 26 + 10) != w
    return (z // 1) * (25*x + 1) + w*x

def block11(w, z):
    x = (z % 26 + 12) != w
    return (z // 1) * (25*x + 1) + w*x

def block12(w, z):
    x = (z % 26 - 4) != w
    return (z // 26) * (25*x + 1) + (w+15)*x

def block13(w, z):
    x = (z % 26) != w
    return (z // 26) * (25*x + 1) + (w+15)*x
