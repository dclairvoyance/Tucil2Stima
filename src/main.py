# File      : main.py
# Oleh      : Damianus Clairvoyance Diva Putra (13520035)
# Tanggal   : 28 Februari 2022

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from myConvexHull import ConvexHull

def start():
    print("Selamat datang di implementasi Convex Hull dengan algoritma Divide and Conquer.")
    print()
    return

def choose():
    # cetak daftar dataset
    print("Pilihan dataset:")
    print("1. Iris")
    print("2. Wine")
    print("3. Breast Cancer")

    # pilih dataset
    pilihan = int(input("Pilihan Anda: "))
    while (pilihan > 3 or pilihan < 1):
        print("Pilihan tidak tersedia.")
        print()
        pilihan = int(input("Pilihan Anda: "))
    
    # load dataset
    if (pilihan == 1):
        data = datasets.load_iris()
    elif (pilihan == 2):
        data = datasets.load_wine()
    else: # pilihan == 3dataa
        data = datasets.load_breast_cancer()
    print()

    # buat dataFrame tabel yang telah dipilih
    df = pd.DataFrame(data.data, columns=data.feature_names) 
    df['Target'] = pd.DataFrame(data.target)

    # cetak data atribut dari tabel yang telah dipilih
    nCol = len(data.feature_names)
    print("Pilihan atribut:")
    for i in range(nCol):
        print(i+1, data.feature_names[i])
    
    # pilih atribut dari tabel yang telah dipilih
    x = int(input("Pilihan atribut pertama Anda (contoh: 1): "))
    y = int(input("Pilihan atribut kedua Anda (contoh: 2): "))
    while (x == y or (x > nCol or x <= 0) or (y > nCol or y <= 0) ):
        print("Pilihan Anda tidak tersedia atau pilihan 1 dan 2 Anda sama.")
        print()
        x = int(input("Pilihan atribut pertama (contoh: 1): "))
        y = int(input("Pilihan atribut kedua (contoh: 2): "))
    return data, df, x, y

def visualize(data, df, x, y):
    # atur kelengkapan visualisasi berupa ukuran, warna, dan legenda
    plt.figure(figsize = (10, 6))
    colors = ['b','r','g', 'c', 'm', 'y', 'k']
    xName = data.feature_names[x-1]
    yName = data.feature_names[y-1]
    plt.title(f"{xName} vs {yName}") 
    plt.xlabel(xName) 
    plt.ylabel(yName)

    # tampilkan titik dan garis antartitik sesuai Convex Hull
    for i in range(len(data.target_names)):
        bucket = df[df['Target'] == i]
        bucket = bucket.iloc[:,[x-1,y-1]].values
        bucket = bucket.tolist()
        hull = ConvexHull(bucket)
        bucket = np.asarray(bucket)
        hull.append(hull[0])
        xs, ys = zip(*hull)
        plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
        plt.plot(xs, ys, colors[i])
        plt.legend()
    plt.show()

# main program
start()
data, df, x, y = choose()
visualize(data, df, x, y)