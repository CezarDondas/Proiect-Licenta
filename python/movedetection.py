#Aici am incercat sa detecteze miscare doar atunci cand acceleratia in modul depaseste acel prag setat mai sus cu 10
#dar acea acceleratie de pe fiecare coordonata sa fie diferita in urmatoare iteratie ptr ca daca acceleratia ar fi aceeasi
#fara sa se miste senzorul, aceasta ar detecta miscare desi nu s-a miscat.
def move_detection(xAccel,yAccel,zAccel,thresholder_accel):
    
    absxAcc=abs(xAccel) - prevabsxAcc
    print(absxAcc)

    absyAcc=abs(yAccel) - prevabsyAcc
    print(absyAcc)

    abszAcc=abs(zAccel) - prevabszAcc
    print(abszAcc)

    print("\n")
    prevabsxAcc=abs(xAccel)
    print(prevabsxAcc)

    prevabsyAcc=abs(yAccel)
    print(prevabsyAcc)

    prevabszAcc=abs(zAccel)
    print(prevabszAcc)

    if (abs(xAccel)>thresholder_accel and absxAcc!=0) or (abs(yAccel)>thresholder_accel and absyAcc!=0) or (abs(zAccel)>thresholder_accel and abszAcc!=0):
        print('\nMiscare detectata!!!!!!\n')
    else:
        print('\nNu s-a detectat nimic.\n')