/*
 * samplelib.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// DP-matching０寄り //DP - matching0 쪽
float funcDP(
			 float fPe, // ペナルティ　0.20くらいか？ //벌금 0.2 정도인가?
			 const float *  f1AccX1, // 系列1のx軸加速度の一次配列 //계열 1의 x축 가속도의 기본 배열
			 const float *  f1AccY1, // 系列1のy軸加速度の一次配列 //계열 1의 y축 가속도의 기본 배열
			 const float *  f1AccZ1, // 系列1のz軸加速度の一次配列 //계열 1의 z축 가속도의 기본 배열
			 int iLen1, // 系列1の系列長 //계열1의 길이
			 const float *  f1AccX2, // 系列2のx軸加速度の一次配列 //계열 2의 x축 가속도의 기본 배열
			 const float *  f1AccY2, // 系列2のy軸加速度の一次配列 //계열 2의 y축 가속도의 기본 배열
			 const float *  f1AccZ2, // 系列2のz軸加速度の一次配列 //계열 2의 z축 가속도의 기본 배열
			 int iLen2 // 系列2の系列長//계열2의 길이
)
{
	
	// 変数宣言 //변수 선언
	int iR, iC; //가로 세로 길이
	float **f2DpTbl; //DP-Matchingの表
	float *f1Mag1;
	float *f1Mag2;
	float fL, fT, fLT;
	float fCosTheta;
	float fTheta;
	float fPiHalf;
	float fDiff;
	int **i2LenTbl;
	
	float PI = 3.1415926535;
	
	// 円周率の半分 //원주율의 절반
	fPiHalf=(float)PI/2.0f;
	
	// DP-Matchingの表、メモリ確保 //DP-Matching 표, 메모리 확보
	f2DpTbl=(float **)malloc(sizeof(float *)*iLen1);
	for(iR=0;iR<iLen1;iR++){
		f2DpTbl[iR]=(float *)malloc(sizeof(float)*iLen2);
	}
	// 長さテーブルの表、メモリ確保 //길이 테이블 테이블,메모리 확보
	i2LenTbl=(int **)malloc(sizeof(int *)*iLen1);
	for(iR=0;iR<iLen1;iR++){
		i2LenTbl[iR]=(int *)malloc(sizeof(int)*iLen2);
	}
	// Magの表、メモリ確保 //Mag표, 메모리 확보
	// Magの表、メモリ確保 //Mag표, 메모리 확보
	f1Mag1=(float *)malloc(sizeof(float)*iLen1);
	f1Mag2=(float *)malloc(sizeof(float)*iLen2);
	// Magの表 //Mag 테이블
	for(iR=0;iR<iLen1;iR++){
		f1Mag1[iR] = sqrtf((float)f1AccX1[iR]*f1AccX1[iR] + f1AccY1[iR]*f1AccY1[iR] + f1AccZ1[iR]*f1AccZ1[iR]);
	}
	for(iC=0;iC<iLen2;iC++){
		f1Mag2[iC] = sqrtf((float)f1AccX2[iC]*f1AccX2[iC] + f1AccY2[iC]*f1AccY2[iC] + f1AccZ2[iC]*f1AccZ2[iC]);
	}
	
	// 表の(0, 0)の計算 // 테이블 (0, 0)을 계산
	iR=0;
	iC=0;
	if((f1Mag1[iR]==0.0f)||(f1Mag2[iC]==0.0f)){
		fCosTheta=0.0f;
	}
	else{
		fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC]);
	}
	if(fCosTheta>1.0f){
		fCosTheta=1.0f;
	}
	else if(fCosTheta<-1.0f){
		fCosTheta=-1.0f;
	}
	fTheta=acosf((float)fCosTheta);
	if(fTheta>PI){
		fTheta=PI;
	}
	else if(fTheta<0.0f){
		fTheta=0.0f;
	}
	f2DpTbl[iR][iC]=fTheta;
	i2LenTbl[iR][iC]=1;
	
	// 表の第0行目の計算 //테이블의 0번째 계산
	iR=0;
	for(iC=1;iC<iLen2;iC++){
		if((f1Mag1[iR]==0.0f)||(f1Mag2[iC]==0.0f)){
			fCosTheta=0.0f;
		}
		else{
			fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC]);
		}
		if(fCosTheta>1.0f){
			fCosTheta=1.0f;
		}
		else if(fCosTheta<-1.0f){
			fCosTheta=-1.0f;
		}
		fTheta=acosf((float)fCosTheta);
		if(fTheta>PI){
			fTheta=PI;
		}
		else if(fTheta<0.0f){
			fTheta=0.0f;
		}
		f2DpTbl[iR][iC]=fTheta+f2DpTbl[iR][iC-1]+fPe;
		i2LenTbl[iR][iC]=i2LenTbl[iR][iC-1]+1;
	}
	
	// 表の第0列目の計算//테이블의 0번째 계산
	iC=0;
	for(iR=1;iR<iLen1;iR++){
		if((f1Mag1[iR]==0.0f)||(f1Mag2[iC]==0.0f)){
			fCosTheta=0.0f;
		}
		else{
			fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC]);
		}
		if(fCosTheta>1.0f){
			fCosTheta=1.0f;
		}
		else if(fCosTheta<-1.0f){
			fCosTheta=-1.0f;
		}
		fTheta=acosf((float)fCosTheta);
		if(fTheta>PI){
			fTheta=PI;
		}
		else if(fTheta<0.0f){
			fTheta=0.0f;
		}
		f2DpTbl[iR][iC]=fTheta+f2DpTbl[iR-1][iC]+fPe;
		i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC]+1;
	}
	
	// 表の第1行第1列以降の計算 //테이블 1행 1열 이상의 계산
	for(iR=1;iR<iLen1;iR++){
		for(iC=1;iC<iLen2;iC++){
			if((f1Mag1[iR]==0.0f)||(f1Mag2[iC]==0.0f)){
				fCosTheta=0.0f;
			}
			else{
				fCosTheta=(f1AccX1[iR]*f1AccX2[iC] + f1AccY1[iR]*f1AccY2[iC] + f1AccZ1[iR]*f1AccZ2[iC]) / (f1Mag1[iR]*f1Mag2[iC]);
			}
			if(fCosTheta>1.0f){
				fCosTheta=1.0f;
			}
			else if(fCosTheta<-1.0f){
				fCosTheta=-1.0f;
			}
			fTheta=acosf((float)fCosTheta);
			if(fTheta>PI){
				fTheta=PI;
			}
			else if(fTheta<0.0f){
				fTheta=0.0f;
			}
			fT=fTheta+f2DpTbl[iR-1][iC]+fPe;
			fLT=fTheta+f2DpTbl[iR-1][iC-1];
			fL=fTheta+f2DpTbl[iR][iC-1]+fPe;
			if(fT<=fL){
				if(fLT<=fT){
					f2DpTbl[iR][iC]=fLT;
					i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC-1]+1;
				}
				else{
					f2DpTbl[iR][iC]=fT;
					i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC]+1;
				}
			}
			else{
				if(fLT<=fL){
					f2DpTbl[iR][iC]=fLT;
					i2LenTbl[iR][iC]=i2LenTbl[iR-1][iC-1]+1;
				}
				else{
					f2DpTbl[iR][iC]=fL;
					i2LenTbl[iR][iC]=i2LenTbl[iR][iC-1]+1;
				}
			}
		}
	}
	
	// 結果 //결과
	fDiff=f2DpTbl[iLen1-1][iLen2-1];
	
	float dpResult = fDiff / (iLen1 + iLen2);
	
	for(iR=0;iR<iLen1;iR++){
		free(f2DpTbl[iR]);
		free(i2LenTbl[iR]);
	}
	free(f2DpTbl);
	free(i2LenTbl);
	
	free(f1Mag1);
	free(f1Mag2);
	
	// 相違度を返す //상위 순위를 반환
	return(dpResult);
	
}

#include <iostream>

using namespace std;

int main(){	
	cout << "pppp\n";
	return 0;
}