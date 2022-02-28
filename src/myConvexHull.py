# File      : myConvexHull.py
# Oleh      : Damianus Clairvoyance Diva Putra (13520035)
# Tanggal   : 28 Februari 2022

import pandas as pd
from sklearn import datasets
import math

def findLeftMost(bucket):
    # masukan: bucket berisi array of points, dengan point berupa tuple (x, y)
    # keluaran: point paling kiri berdasarkan absis dan ordinat
    leftmost = bucket[0]
    for point in bucket:
        if (point[0] < leftmost[0]):
            leftmost = point
        elif (point[0] == leftmost[0] and point[1] < leftmost[1]):
            leftmost = point
    return leftmost

def findRightMost(bucket):
    # masukan: bucket berisi array of points, dengan point berupa tuple (x, y)
    # keluaran: point paling kanan berdasarkan absis dan ordinat
    rightmost = bucket[0]
    for point in bucket:
        if (point[0] > rightmost[0]):
            rightmost = point
        elif (point[0] == rightmost[0] and point[1] > rightmost[1]):
            rightmost = point
    return rightmost

def findEquation(x1, y1, x2, y2):
    # masukan: dua titik (x1, y1) dan (x2, y2) pada suatu garis l
    # luaran: a, b, dan c dalam persamaan garis 1
    # persamaan garis 1: ax + by + c = 0
    # persamaan garis 2: y - y1 = m(x - x1) = mx - mx1
    #                   mx - y + (y1 - mx1) = 0
    #             maka, a = m, b = -1, c = y1 - mx1
    m = (y2-y1)/(x2-x1)
    return m, -1, y1 - m*x1

def findY(x1, y1, x2, y2, x):
    # masukan: dua titik (x1, y1) dan (x2, y2) pada suatu garis l, serta nilai x
    # luaran: nilai y dari nilai x pada garis l
    # rumus gradien: m = (y2-y1)/(x2-x1)
    # rumus cari y: y = m(x - x1) + y1
    if (x1 != x2):
        m = (y2-y1)/(x2-x1)
        return m*(x - x1) + y1
    else:
        return 0

def findDistance(x1, y1, x2, y2, x3, y3):
    # masukan: dua titik P1(x1, y1) dan P2(x2, y2) pada suatu garis l, 
    #          serta titik P3(x3, y3)
    # luaran: jarak titik P3 terhadap garis P1P2
    # rumus jarak: |ax + by + c|/akar(a^2 + b^2)
    a, b, c = findEquation(x1, y1, x2, y2)
    return abs(a*x3 + b*y3 + c)/math.sqrt(a*a + b*b)

'''
def findDistance(x1, y1, x2, y2, x3, y3):
    # versi 2
    return (1/2) * abs((x1 - x3) * (y2-y1) - (x1 - x2) * (y3 - y1))
'''

def findAngle(x1, y1, x2, y2, x3, y3):
    # masukan: tiga titik P1(x1, y1), P2(x2, y2), dan P3(x3, y3),
    #          yang membentuk segitiga P1P3P2, dengan
    #          sisi a = sisi P3P1, sisi b = sisi P3P2, dan sisi c = sisi P1P2
    # luaran: sudut C, yang mengapit sisi a dan b
    # rumus dasar: c^2 = a^2 + b^2 - 2*a*b*cos(theta)
    a2 = (x3-x1)*(x3-x1) + (y3-y1)*(y3-y1)
    b2 = (x3-x2)*(x3-x2) + (y3-y2)*(y3-y2)
    c2 = (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1)
    a = math.sqrt(a2)
    b = math.sqrt(b2)
    c = math.sqrt(c2)
    if (((a2 + b2 - c2)/(2*a*b)) <= 1 and ((a2 + b2 - c2)/(2*a*b)) >= -1):
        return math.acos((a2 + b2 - c2)/(2*a*b))
    else:
        return 0

def findFurthest(bucket, left, right):
    # masukan: dua titik left(x1, y1) dan right(x2, y2) pada suatu garis l,
    #          serta bucket (array titik pada suatu section)
    # luaran: titik dengan jarak terjauh terhadap garis l
    furthest = bucket[0]
    for point in bucket:
        distCurrent = findDistance(left[0], left[1], right[0], right[1], point[0], point[1])
        distFurthest = findDistance(left[0], left[1], right[0], right[1], furthest[0], furthest[1])
        if (distCurrent > distFurthest):
            furthest = point
        elif (distCurrent == distFurthest):
            angleCurrent = findAngle(left[0], left[1], right[0], right[1], point[0], point[1])
            angleFurthest = findAngle(left[0], left[1], right[0], right[1], furthest[0], furthest[1])
            if (angleCurrent > angleFurthest):
                furthest = point
    return furthest

def ConvexHullDnCUpper(bucket, left, right, bucketDnC):
    # algoritma rekursif Divide and Conquer, algoritma dijelaskan pada laporan
    # pengolahan section lebih atas dari garis leftmost-rightmost
    # masukan: bucket (array titik pada suatu section), 
    #          left (titik kiri), right (titik kanan)
    # masukan/keluaran: bucketDnC (array titik pembentuk ConvexHull)
    leftBucket = []
    rightBucket = []

    if (len(bucket) != 0):
        # pencarian titik terjauh dari garis left-right
        furthest = findFurthest(bucket, left, right)
        for point in bucket:
            # pembagian titik dalam bucket utuk pemrosesan lebih lanjut
            if (point != furthest):
                y = findY(left[0], left[1], furthest[0], furthest[1], point[0])
                # bila titik di atas garis left-furthest, masukkan dalam leftBucket
                if (y > point[1]):
                    leftBucket.append(point)
                y = findY(right[0], right[1], furthest[0], furthest[1], point[0])
                # bila titik di atas garis furthest-right, masukkan dalam rightBucket
                if (y > point[1]):
                    rightBucket.append(point)
        # untuk tiap bucket baru, kembali lakukan divide and conquer
        ConvexHullDnCUpper(leftBucket, left, furthest, bucketDnC)
        ConvexHullDnCUpper(rightBucket, furthest, right, bucketDnC)
    else:
        # bila bucket kosong (tidak ada titik di atas garis), left pembentuk Convex Hull
        if (left not in bucketDnC):
            bucketDnC.append(left)
    return

def ConvexHullDnCLower(bucket, left, right, bucketDnC):
    # algoritma rekursif Divide and Conquer, algoritma dijelaskan pada laporan
    # pengolahan section lebih atas dari garis leftmost-rightmost
    # masukan: bucket (array titik pada suatu section), 
    #          left (titik kiri), right (titik kanan)
    # masukan/keluaran: bucketDnC (array titik pembentuk ConvexHull)
    leftBucket = []
    rightBucket = []

    if (len(bucket) != 0):
        # pencarian titik terjauh dari garis left-right
        furthest = findFurthest(bucket, left, right)
        for point in bucket:
            # pembagian titik dalam bucket utuk pemrosesan lebih lanjut
            if (point != furthest):
                y = findY(left[0], left[1], furthest[0], furthest[1], point[0])
                # bila titik di bawah garis left-furthest, masukkan dalam leftBucket
                if (y < point[1]):
                    leftBucket.append(point)
                y = findY(right[0], right[1], furthest[0], furthest[1], point[0])
                # bila titik di bawah garis furthest-right, masukkan dalam rightBucket
                if (y < point[1]):
                    rightBucket.append(point)
        # untuk tiap bucket baru, kembali lakukan divide and conquer
        ConvexHullDnCLower(rightBucket, furthest, right, bucketDnC)
        ConvexHullDnCLower(leftBucket, left, furthest, bucketDnC)
    else:
        # bila bucket kosong (tidak ada titik di atas garis), left pembentuk Convex Hull
        if (left not in bucketDnC):
            bucketDnC.append(left)
    return

def ConvexHull(bucket):
    cHullBucket = []
    upperBucket = []
    lowerBucket = []
    leftmost = findLeftMost(bucket)
    rightmost = findRightMost(bucket)

    # pembagian titik di atas dan bawah garis leftmost-rightmost
    for point in bucket:
        y = findY(leftmost[0], leftmost[1], rightmost[0], rightmost[1], point[0])
        if (y > point[1]):
            upperBucket.append(point)
        elif (y < point[1]):
            lowerBucket.append(point)
        # else
            # do nothing, karena artinya berada pada garis
    
    # lakukan divide and conquer section atas
    ConvexHullDnCUpper(upperBucket, leftmost, rightmost, cHullBucket)
    # rightmost pasti pembentuk ConvexHull
    cHullBucket.append(rightmost)
    # lakukan divide and conquer section bawah
    ConvexHullDnCLower(lowerBucket, leftmost, rightmost, cHullBucket)
    return cHullBucket