# -*- coding: UTF-8 -*-

import math

# DP-matching０寄り //DP - matching0 쪽
def funcDP(
            fPe, # ペナルティ　0.20くらいか？ //벌금 0.2 정도인가?
            f1AccX1,# 系列1のx軸加速度の一次配列 //계열 1의 x축 가속도의 기본 배열
            f1AccY1, # 系列1のy軸加速度の一次配列 //계열 1의 y축 가속도의 기본 배열
            f1AccZ1, # 系列1のz軸加速度の一次配列 //계열 1의 z축 가속도의 기본 배열
            iLen1, # 系列1の系列長 //계열1의 길이
            f1AccX2, # 系列2のx軸加速度の一次配列 //계열 2의 x축 가속도의 기본 배열
            f1AccY2, # 系列2のy軸加速度の一次配列 //계열 2의 y축 가속도의 기본 배열
            f1AccZ2, # 系列2のz軸加速度の一次配列 //계열 2의 z축 가속도의 기본 배열
            iLen2 # 系列2の系列長//계열2의 길이
):

    # 変数宣言 //변수 선언
    iR=iC=0 # //가로 세로 길이
    f2DpTbl=[[]] #DP-Matchingの表
    f1Mag1 = []
    f1Mag2 = []
    fL=fT=fLT=.0
    fCosTheta=.0
    fTheta=.0
    fPiHalf=.0
    fDiff=.0
    i2LenTbl=[[]]

    PI = 3.1415926535;

    # 円周率の半分 //원주율의 절반
    fPiHalf=PI/2.0

    f2DpTbl = [[0 for i in range(iLen2)] for i in range(iLen1)]
    i2LenTbl = [[0 for i in range(iLen2)] for i in range(iLen1)]
    
    for iR in range(0, iLen1):
        f1Mag1.append(math.sqrt(f1AccX1[iR]*f1AccX1[iR] + f1AccY1[iR]*f1AccY1[iR] + f1AccZ1[iR]*f1AccZ1[iR]))

    #for(iC=0;iC<iLen2;iC++){
    for iC in range(0, iLen2):
        f1Mag2.append(math.sqrt(f1AccX2[iC]*f1AccX2[iC] + f1AccY2[iC]*f1AccY2[iC] + f1AccZ2[iC]*f1AccZ2[iC]))


    # 表の(0, 0)の計算 // 테이블 (0, 0)을 계산
    iR=0
    iC=0
    if f1Mag1[iR]==0.0 or f1Mag2[iC]==0.0:
        fCosTheta=0.0
    else:
        fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC])

    if fCosTheta>1.0:
        fCosTheta=1.0
    elif fCosTheta<-1.0:
        fCosTheta=-1.0

    fTheta=math.acos(fCosTheta)
    if fTheta>PI:
        fTheta=PI
    elif fTheta<0.0:
        fTheta=0.0

    f2DpTbl[iR][iC]=fTheta
    i2LenTbl[iR][iC]=1

    # 表の第0行目の計算 //테이블의 0번째 계산
    iR=0;
    for iC in range(1,iLen2):
        if f1Mag1[iR]==0.0 or f1Mag2[iC]==0.0:
            fCosTheta=0.0
        else:
            fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC]);

        if fCosTheta>1.0:
            fCosTheta=1.0
        elif fCosTheta<-1.0:
            fCosTheta=-1.0

        fTheta=math.acos(fCosTheta)
        if fTheta>PI:
            fTheta=PI
        elif fTheta<0.0:
            fTheta=0.0

        f2DpTbl[iR][iC]=fTheta+f2DpTbl[iR][iC-1]+fPe
        i2LenTbl[iR][iC]=i2LenTbl[iR][iC-1]+1

    # 表の第0列目の計算//테이블의 0번째 계산
    iC=0;
    for iR in range(1,iLen1):
        if f1Mag1[iR]==0.0 or f1Mag2[iC]==0.0:
            fCosTheta=0.0
        else:
            fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC])
        if fCosTheta>1.0:
            fCosTheta=1.0
        elif fCosTheta<-1.0:
            fCosTheta=-1.0

        fTheta=math.acos(fCosTheta)
        if fTheta>PI:
            fTheta=PI
        elif fTheta<0.0:
            fTheta=0.0

        f2DpTbl[iR][iC]=fTheta+f2DpTbl[iR-1][iC]+fPe
        i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC]+1


    # 表の第1行第1列以降の計算 //테이블 1행 1열 이상의 계산
    for iR in range(1,iLen1):
        for iC in range(1,iLen2):
            if f1Mag1[iR]==0.0 or f1Mag2[iC]==0.0:
                fCosTheta=0.0
            else:
                fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC])

            if fCosTheta>1.0:
                fCosTheta=1.0
            elif fCosTheta<-1.0:
                fCosTheta=-1.0

            fTheta=math.acos(fCosTheta)
            if fTheta>PI:
                fTheta=PI

            elif fTheta<0.0:
                fTheta=0.0

            fT=fTheta+f2DpTbl[iR-1][iC]+fPe
            fLT=fTheta+f2DpTbl[iR-1][iC-1]
            fL=fTheta+f2DpTbl[iR][iC-1]+fPe
            if fT<=fL:
                if (fLT<=fT):
                    f2DpTbl[iR][iC]=fLT
                    i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC-1]+1
                else:
                    f2DpTbl[iR][iC]=fT
                    i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC]+1
            else:
                if fLT<=fL:
                    f2DpTbl[iR][iC]=fLT
                    i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC-1]+1
                else:
                    f2DpTbl[iR][iC]=fL;
                    i2LenTbl[iR][iC]=i2LenTbl[iR][iC-1]+1


    # 結果 //결과
    fDiff=f2DpTbl[iLen1-1][iLen2-1]

    dpResult = fDiff / (iLen1 + iLen2)

    # 相違度を返す
    return(dpResult)


