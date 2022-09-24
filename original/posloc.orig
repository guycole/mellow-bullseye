

C			** POSLOC FIX ALGORITHM **

C=======================================================================
C
C		DESCRIPTION OF STANDARD FIX ALGORITHM INTERFACE  4/5/85
C
C   	Example of CALL statement:
C	
C	CALL fix ( NST, STATIONID, STALAT, STALON, ANT_TYPE,
C                  FREQ, LOB, FIXED, CRASHED, BPELAT, BPELON,
C                  MAJ_AXIS, MIN_AXIS, AREA, ORIEN, USED )
C
C       Argument description:
C
C       INPUT:
C	   	NST ............ INTEGER ....... Number of bearings.
C		STATIONID(50) .. CHARACTER*2  .. Reporting station ID.
C		STALAT(50) ..... REAL .......... Station latitude.
C               STALON(50) ..... REAL .......... Station longitude (+east).
C               ANT_TYPE(50) ... INTEGER ....... Antenna type ( 0 or other)
C                                                see subroutine PDDG.
C						 For this version of POSLOC
C						 the antenna types are:
C						  0 : 'GRD-6'
C						  1 : 'FRD-10'
C						  2 : 'FLR-9'
C						  3 : 'PUSHER'/'OUTBOARD'
C               FREQ ........... REAL .......... Frequency in MHZ.
C               LOB(50) ........ REAL .......... Reported bearing in degrees.
C       OUTPUT:
C               FIXED .......... LOGICAL ....... True if successful fix.
C               CRASHED ........ LOGICAL ....... True if run time error.
C               BPELAT ......... REAL .......... Latitude of BPE.
C               BPELON ......... REAL .......... Longitude of BPE (+east).
C               MAJ_AXIS ....... REAL .......... Length in NM.
C               MIN_AXIS ....... REAL .......... Length in NM.
C               AREA     ....... REAL .......... Ellipse area in Sq. NM.
C               ORIEN .......... REAL .......... Orientation of major axis
C                                                in degrees from north.
C               BRNGS_USED ..... INTEGER ....... Number of bearings used in
C                                                fix.
C		PDDG_USED(50) .. INTEGER ....... 1 if PDDG was used in fix,
C						 0 if not.
C=======================================================================
C
C   Note the code could be streamlined somewhat, but I left it this way
C   to match the original BASIC version as received from SKAGGS.
C=======================================================================
C
C   Input Parameters not used in POSLOC:
C	STAVAR
C=======================================================================
C
C   INCLUDE FILES:		COMBLK.INC
C=======================================================================
C
C			START OF ROUTINE
								

	SUBROUTINE POSLOC ( NB, NAME, STALAT, STALON, TYPE, FREQ,
     &                      BRNG, FIXED, CRASHED, BPELAT, BPELON, 
     &                      MAJ_AXIS, MIN_AXIS, AREA, ORIEN,
     &                      BRNGS_USED, PDDG_USED )
									

C***********************************************************************
C			PARAMETER DECLARATION

	INTEGER		NB, BRNGS_USED, PDDG_USED(50), TYPE(50)
	REAL		AREA, BPELAT, BPELON, BRNG(50), FREQ
	REAL		MAJ_AXIS, MIN_AXIS, ORIEN, STALAT(50)
	REAL		STALON(50) 
	CHARACTER*2	NAME(50)
	LOGICAL		FIXED, CRASHED

C***********************************************************************

C			** (POSLOC)**			6/7/84
C  			TRANSLATED FROM TEKTRONIX BASIC	
C			BY W.S. BRATT, NOSC CODE 754,
C			WHICH IN TURN WAS TRANSLATED
C			FROM ONLINE NELIAC BY R. LOMAX,
C			SKAGGS ISLAND.


C***********************************************************************
C
C		VARIABLES (not a complete list)
C   A : Area of confidence ellipse.
C   B1(nst) : Reported line of bearing.
C   B2(nst) : Bearing error
C   BPOS : "position vector" of valid lines of bearing
C   F : Frequency
C   ID(nst) : Bearing ID
C   I1 : Number of bearings
C   I2 : Position of rejected bearing
C   IFLAG : Control flag
C   M : Semi-major axis of confidence ellipse
C   M1 : Semi-minor axis of confidence ellipse
C   M3 : Largest bearing error
C   N : Number of valid bearings
C   NAME(nst) : Station ID
C   NST : Number of stations
C   N1,O1 : Simple flags
C   P : "PHI", target latitude
C   P2 : Indicates algorithm pass
C   PI : Constant 
C   POSITION : 	Position vector of IDs used 
C   R : Orientation of confidence ellipse
C   RONE : Conversion factor, degrees to radians 
C   RTWO : Conversion factor, radians to degrees
C   S1(nst) : Station latitude in radians
C   S2(nst) : Station longitude in radians
C   SPOS : "position vector" of current stations
C   STALAT(nst) : Station latitude in degrees
C   STALON(nst) : Station longitude in degrees
C   T : Target longitude
C   TYPE(nst) : Antenna type
C   W(nst) : Bearing weight
C
C***********************************************************************



	INCLUDE '(COMBLK)'

	INTEGER 	P2,X7,O1
	INTEGER 	SPOS(20),BPOS(20)
	REAL 		B2(50), M3

C   Establish error handler.
	EXTERNAL	LIB$SIG_TO_RET
	CALL LIB$ESTABLISH ( LIB$SIG_TO_RET )

C***********************************************************************
C   Initialize variables used in fix.
	F = FREQ
	N = NB
	DO I = 1,N
	  ID(I) = NAME(I)
	  S1(I) = STALAT(I)
	  STALON(I) = STALON(I)
	  S2(I) = STALON(I)
	  N2(I) = TYPE(I)
	  B1(I) = BRNG(I)
	END DO
C***********************************************************************
									
C   Set output device.
	LW = 5

	I1 = N

C   Initialize constants and set variables to 0.
	CALL POS_INITIAL(B2,P2,N1,O1)

C   Copy lat, lon and antenna type and initialize weights(W(i)).
	CALL PDDG(N,NAME,STALAT,STALON,TYPE)

C   Convert degree information to radians.
	CALL CONVERT

C   Transform spherical coordinates to vector equivalents.
	DO 300 I=1,N
300	 CALL XFORM(I)


C   **	Begin computing DF fix. **

C   Calculate initial BPE (best point estimate).   
	CALL XPRODBPE ( O1, FIXED )
	IF ( .NOT. FIXED ) GOTO 1000

C   Correct reciprocal bearings.
	CALL RECIP(P2)

C   Compute bearing error.
	CALL COMPBURTZ(I2,M3,N1,B2)

C   Reject wild bearings.
	CALL OUTLIER(N1,B2,I2,M3)

C   Compute weight for each bearing.
	CALL WEIGHT

C   Check bearings until all are determined usable (N1TMP = 0).
	N1TMP = 1
	DO WHILE (N1TMP .EQ. 1)
C   Nofix condition is handled in XPRODBPE.
	 CALL XPRODBPE ( O1, FIXED )
	 IF ( .NOT. FIXED ) GOTO 1000
	 CALL WEIGHT
	 CALL COMPBURTZ(I2,M3,N1,B2)
	 CALL OUTLIER(N1,B2,I2,M3)
	 N1TMP = N1
	END DO

C   Compute confidence region around the BPE.
	CALL CONFAREA

C   If I1 (the number of bearings at the start), does not equal N (the
C   number of valid bearings), then continue processing, otherwise
C   output answers and stop.
	IF (I1 .NE. N) THEN

D	 WRITE (LW,*),' PASS TWO'
	 IFLAG = 0
	 X1 = P
	 X2 = T
	 X3 = A
	 X4 = M
	 X5 = M1
	 X6 = R
	 X7 = N
	 DO 310 I=1,I1
310	  W(I) = 1.
	 N = I1
	 P2 = 1

	 CALL RECIP(P2)
	 CALL WEIGHT
	 CALL COMPBURTZ(I2,M3,N1,B2)

	 N1TMP = 1
	 DO WHILE ( N1TMP .EQ. 1)
	  CALL OUTLIER(N1,B2,I2,M3)
	  N1TMP = N1
	 END DO

C   If the number of valid bearings (N) is not the same as the number
C   bearings validated the first time (X7) then continue processing.
	 IF (N .GT. X7) THEN 
	  CALL XPRODBPE ( O1, FIXED )
	  IF ( .NOT. FIXED ) GOTO 1000
	  IF (ABS(P-X1) .LE. 0.0349066) THEN
	   T1 = T-X2
	   IF (ABS(T1) .GT. PI) THEN
	    IF (T1 .LT. 0.) THEN
	     T1 = T1 + 2*PI
	    ELSE
	     T1 = T1 - 2*PI
	    END IF
	   END IF
	   IF (ABS(T1*COS(X1)) .LE. 0.0349066) THEN
	    IFLAG = 1
	    CALL WEIGHT
	    CALL CONFAREA
	    P3 = 20
	   END IF
	  END IF
	 END IF

C   If IFLAG is 0 then answers are in X1 through X7.
	 IF (IFLAG .EQ. 0) THEN
	  P = X1
	  T = X2
	  A = X3
	  M = X4
	  M1 = X5
	  R = X6
	  N = X7
	 END IF

	END IF

C   Output results.
	CALL ANSBACK ( BPELAT, BPELON, B2 )

C   Store results in parameters to be passed back.
	MAJ_AXIS = M1
	MIN_AXIS = M
	AREA = A
	ORIEN = R
	BRNGS_USED = N
	DO I = 1,I1
	  PDDG_USED(I) = 1
	  IF ( W(I) .EQ. 0 ) PDDG_USED(I) = 0
 	END DO

1000	CONTINUE

	CRASHED = .FALSE.
	RETURN
	END



C			** ANSBACK **
C
C   Output results.

	SUBROUTINE ANSBACK ( BPELAT, BPELON, B2 )
	
	INCLUDE '(COMBLK)'

	REAL		BPELAT, BPELON, B2(50)
	CHARACTER*3     MCHAR, NCHAR

C   Pass the answers back.
C   Try to express it in degrees/minutes.
C   First, convert BPE to decimal degrees.

	X1 = P
	X2 = T
	P = ATAN(TAN(P)*1.00336924)
	P = INT(ABS(P*RONE*64.))*SGN(P)/64.
	T = INT(ABS(T*RONE*64.))*SGN(T)/64.
	BPELAT = P
	BPELON = T
	MCHAR = 'N'
	NCHAR = 'E'
C   Assume north and east.
	IF (P .LT. 0.) THEN
	 MCHAR = 'S'
	 P = ABS(P)
	END IF
	IF (T .LT. 0.) THEN
	 NCHAR = 'W'
	 T = ABS(T)
	END IF
C   Now get fractional degrees and store as seconds.
	M8 = 3600*(P - INT(P))
	N8 = 3600*(T - INT(T))
	M9 = INT(M8/60)
	N9 = INT(N8/60)
	IF ((M8 - M9*60) .NE. 0) M9 = M9 + 1
	IF ((N8 - N9*60) .NE. 0) N9 = N9 + 1
D	WRITE (LW,2)
2	FORMAT ('1',///24X,'** POSLOC FIX RESULTS **'///)

D	WRITE (LW,*) ' '
D	WRITE (LW,10) X1
10	FORMAT (1X,'PHI   : ',F10.2)
D	WRITE (LW,20) X2
20	FORMAT (1X,'THETA : ',F10.2)
D	WRITE (LW,30) F
30	FORMAT (1X,'FIX RESULTS ON FREQUENCY',F8.2,' MHZ')
D	WRITE (LW,*) ' '
D	WRITE (LW,40) INT(P),M9,MCHAR,INT(T),N9,NCHAR
40	FORMAT (1X,'BPE   :   ',I4,'-',I2,A2,'   ',I4,'-',I3,A2)
	R = R*RONE
D	WRITE(LW,50) INT(M),INT(M1),INT(R)
50	FORMAT (1X,'AXES  :  ',I5,' * ',I5,'  (',I8,')')
D	WRITE(LW,60) A,I1,N
60	FORMAT (1X,'AREA  : ',F11.2,' SQNM.  BRNGS/USED:  ',I2,' /',I2)
	CALL LOBERROR(X1,X2,B2)

	RETURN
	END




C			** BRNG **
C
C   Computes bearing (T1) in radians between a station,S2(i), and the
C   target,T.

C   Input : T,S2,S3,S5,C2,PI,I
C   Output : T1

	SUBROUTINE BRNG(I,T1)
	
	INCLUDE '(COMBLK)'

	C = T - S2(I)
	T1 = COS(C)*C5*S3(I) - S5*C2(I)
	D = SIN(C)*C5
	T1 = ATAN(T1/D) + PI/2
	IF (D .LT. 0.) T1 = T1+PI

	RETURN
	END




C			** COMPBURTZ **
C
C   Compute bearing error.

C   Input : W,B1,SR,I1
C   Output : N1,M3,I2,B2

	SUBROUTINE COMPBURTZ(I2,M3,N1,B2)
	
	REAL M3,B2(50)

	INCLUDE '(COMBLK)'

	M3 = 0.
	N1 = 0
C	WRITE (5,*)' COMPBURTZ '
	DO 10 I=1,I1
	 IF (W(I) .NE. 0.) THEN
	  CALL BRNG(I,T1)
	  B6 = ABS(T1 - B1(I))
	  T1 = PI*2 - B6
	  IF (T1 .LT. B6) B6 = T1
	  T1 = B6/SQRT(S4(I))
C	  WRITE (5,*) 'B6:',B6
C	  WRITE (5,*) 'S4(I),I:',S4(I),I
	  B2(I) = T1
	  IF (T1 .GT. M3) THEN
	   M3 = T1
	   I2 = I
	  END IF
	 END IF
10	CONTINUE
C	WRITE (5,*)' '
	RETURN
	END




C			** CONFAREA **
C
C   Computes the confidence region surrounding the estimate of target
C   position P (Phi) and T (Theta).

C   Input : W,S2,S3,S4,S5,C2,C5,E1,E2,E3,PI
C   Output : M,M1,A,R

	SUBROUTINE CONFAREA

	REAL Y(3),L1,L2,L3

	INCLUDE '(COMBLK)'

	IF (I1 .LT. 2) THEN
	  M = 0.
	  M1 = 0.
	  A = 0.
	  R = ACOS(E1(1)*E1(2) + E2(1)*E2(2) + E3(1)*E3(2))
	ELSE

	  DO 10 I=1,3
10	    Y(I) = 0.

	  DO 20 I=1,I1
	    IF (W(I) .NE. 0.) THEN
D	      WRITE (5,*) ' S4(I) IN CONFAREA : ',S4(I)
	      L3 = T - S2(I)
	      S6 = SIN(L3)
	      C6 = COS(L3)
	      U = C6*C5*S3(I) - S5*C2(I)
	      V1 = S6*C5
	      F1 = U*U + V1*V1
	      H1 = -C2(I)*S6/F1
	      H2 = -(V1*S6*S3(I) + U*C6)/F1
	      Y(1) = Y(1) + H1*H1/S4(I)
	      Y(2) = Y(2) + H1*H2/S4(I)
	      Y(3) = Y(3) + H2*H2/S4(I)
C	  Y(1) = Y(1) + H1*H1/1.0
C	  Y(2) = Y(2) + H1*H2/1.0
C	  Y(3) = Y(3) + H2*H2/1.0
	    END IF
20	  CONTINUE

	  D4 = 1/(Y(1)*Y(3) - Y(2)*Y(2))
	  A1 = Y(3)*D4
	  B = -Y(2)*D4
	  C = Y(1)*D4
	  F1 = (A1-C)*(A1-C) + 4*B*B
	  L1 = 0.5*(A1 + C + SQRT(F1))
	  L2 = D4/L1
	  M1 = 7377.273*SQRT(L1)
	  M = 7377.273*SQRT(L2)
	  R = ATAN((L1-A1)/B)
	  A = PI*M*M1
	  IF (R .LT. 0.) R = R+PI
	END IF

	RETURN
	END




C			** CONVERT **
C
C  Converts degree information to radians and calculates some constants.

C  Input : S4,S1,D1,S2,I1
C  Output : S1,S2,S3,S4,C2,B1

	SUBROUTINE CONVERT

	INCLUDE '(COMBLK)'

	DO 10 I=1,I1
	 S1(I) = S1(I)*D1
	 S3(I) = SIN(S1(I))
	 C2(I) = COS(S1(I))
	 S2(I) = S2(I)*D1
	 B1(I) = B1(I)*D1
	 S4(I) = 0.03
10	CONTINUE

	RETURN
	END




C			** INITIAL **
C
C   Initialize constants and set unused variables to zero.

	SUBROUTINE POS_INITIAL(B2,P2,N1,O1)

	REAL B2(50)
	INTEGER P2,N1,O1

	INCLUDE '(COMBLK)'

	PI = 3.14159265
	D1 = 0.01745329252
	RONE = 57.2957795131
	RTWO = 1.3

	P2 = 0
	N1 = 0
	O1 = 0

	DATA C3/1.96,2.237,2.388,2.491,2.569,2.631,2.683,2.727,2.766,
	12.8,2.831,2.858,2.883,2.906,2.928,2.948,2.967,2.984/


	DO 10 I=1,3
10	 C1(I) = 0.

	DO 20 I=1,50
	 B2(I) = 0.
	 C2(I) = 0.
 	 E1(I) = 0.
	 E2(I) = 0.
	 E3(I) = 0.
	 E4(I) = 0.
	 E5(I) = 0.
	 E6(I) = 0.
	 S3(I) = 0.
20	CONTINUE

	RETURN
	END




C			** LOBERROR **
C
C   Output line of bearing error results.

	SUBROUTINE LOBERROR(X1,X2,B2)

	INCLUDE '(COMBLK)'

	REAL	    B2(50)
	CHARACTER*3 UCHAR

	P = X1
	T = X2
D	WRITE (LW,*)' '
D	WRITE (LW,10)
10	FORMAT (2X,'ID    LOB     TLOB     DIST     ERROR     ChiSq    
	1 USED')
D	WRITE (LW,*) ' --    ---     ----     ----     -----     -----
D	1    ----'

	DO 30 I=1,I1
	 CALL BRNG(I,T1)
	 CALL RDIST(I,D)
	 UCHAR = 'YES'
	 IF (W(I) .EQ. 0.) UCHAR = 'NO'
D	 WRITE (LW,20) ID(I),B1(I)*RONE,T1*RONE,D*RONE*60,
D	1(T1-B1(I))*RONE,B2(I),UCHAR
20	 FORMAT (2X,A2,3X,F5.1,3X,F5.1,3X,F8.2,4X,F6.1,4X,F6.3,4X,A3)
30	CONTINUE

	RETURN
	END




C			** NOFIX **
C
C   Terminate execution if unable to fix target.

	SUBROUTINE NOFIX(LW)

D	WRITE (LW,*) ' '
D	WRITE (LW,*) ' NO FIX '

	RETURN
	END




C			** OUTLIER **
C
C  Rejects wildest bearing. N is the number of valid bearings, a wild
C  bearing has its associated weight ,W(I2), set to 0.

C  Input : N1,W,B2,C3,N
C  Output : N,W(I2)

	SUBROUTINE OUTLIER(N1,B2,I2,M3)

	REAL M3,B2(50)

	INCLUDE '(COMBLK)'

	IF (N1 .NE. 0) THEN
	 M3 = 0.
	 DO 10 I=1,I1
	  IF (W(I) .NE. 0.) THEN
	   IF (B2(I) .GT. M3) THEN
	    M3 = B2(I)
	    I2 = I
	   END IF
	  END IF
10	 CONTINUE
	END IF

	N1 = 0
	IF (N .GE. 19) THEN
	 IF (M3 .LT. 3.) GO TO 30
	ELSE
	 IF (M3 .LE. C3(N)) GO TO 30	
	END IF
	W(I2) = 0.
C  Above discards wildest bearing.
	N = N-1
	N1 = 1

C	WRITE (LW,20) I2,M3,N
20	FORMAT(1X,'MAXI  ',I2,'  MAX BURTZ',F10.2,' NR VALID = ',I2)
30	CONTINUE

	RETURN
	END




C			** PDDG **
C
C   Match bearing ID with station list, save relevant station info
C   and initialize weight vector.

C   Input : ID,NST,STALAT,STALON,TYPE
C   Output : S1,S2,N2,W

	SUBROUTINE PDDG(NBRNG,NAME,STALAT,STALON,TYPE)

	INTEGER TYPE(50)
	REAL STALAT(50),STALON(50)
	CHARACTER*2 NAME(50)

	INCLUDE '(COMBLK)'

	DO 20 I=1,NBRNG
	 IF (N2(I) .EQ. 0) THEN
	  W(I) = 0.1
	 ELSE
	  W(I) = 1.
	  S1(I) = ATAN(TAN(S1(I)*D1)*0.996652009)*RONE
	 END IF
20	CONTINUE

	RETURN
	END




C			** RDIST **
C
C   Computes the spherical distance (D) in radians between a station 
C   S2(i) and the target T.

C   Input : T,S2,S3,S5,C2,C5,I
C   Output : D

	SUBROUTINE RDIST(I,D)

	INCLUDE '(COMBLK)'

	C = S2(I) - T
	D = ACOS(S3(I)*S5 + C2(I)*C5*COS(C))

	RETURN
	END




C			** RECIP **
C
C   Corrects reciprocal bearings.

C   Input : N2,P2,R2,B1,I1,PI
C   Output : B1 (changed if needed)

	SUBROUTINE RECIP(P2)
	
	INTEGER P2

	INCLUDE '(COMBLK)'

	DO 20 I=1,I1
	 IF (P2 .NE. 1.) THEN
	  IF (N2(I) .NE. 0.  .AND.  N2(I) .NE. 3.) THEN
	   CALL RDIST(I,D)
	   IF (D .LT. RTWO) GO TO 20
	  END IF
	 END IF
	 CALL BRNG(I,T1)
	 B6 = ABS(T1 - B1(I))
	 T1 = 2*PI - B6
	 IF (T1 .LT. B6) B6 = T1
	 IF (B6 .GE. PI/2) THEN
	  T1 = PI + B1(I)
	  IF (T1 .GT. 2*PI) T1 = T1 - 2*PI
	  B1(I) = T1
	  CALL XFORM(I)
C	  WRITE (LW,10) I,B1(I)*RONE
10	  FORMAT (1X,'STATION ',I2,' RECIP BRNG = ',F10.4)
	 END IF
20	CONTINUE

	RETURN
	END




C			** SGN **
C
C   Determines the sign (+1,0 or -1) of a real input P.

	FUNCTION SGN(P)

	IF (P .LT. 0.) SGN = -1.
	IF (P .EQ. 0.) SGN = 0.
	IF (P .GT. 0.) SGN = 1.

	RETURN
	END




C			** WEIGHT **
C
C   Computes weights for each bearing.

C   Input : W,N2,F,I1,PI
C   Output : W,S4

	SUBROUTINE WEIGHT

	INCLUDE '(COMBLK)'


	DO 10 I=1,I1
	 IF (W(I) .NE. 0.) THEN
	  CALL RDIST(I,D)
	  T1 = D
	  IF (F .GT. 9.) THEN
	   W2 = -0.0585*F
	   W3 = 2.013*EXP(W2)
	  ELSE
	   W2 = -0.364*F
	   W3 = 12.367*EXP(W2)
	  END IF
	  IF (N2(I) .EQ. 0.  .OR.  N2(I) .GE. 3.) W3 = W3*1.5

C  Above value should be 1.5 (2.0 used previously).

	  IF (T1 .GT. 0.088) THEN
	   W4 = 1.1 + 0.955*T1
	  ELSE
	   W4 = 3.
	  END IF
	  IF (T1 .GT. 1.) W4 = W4*2.
	  S4(I) = 3.046E-4*(W3*W3 +W4)
	  IF (T1 .LT. PI/2) THEN
	   W2 = SIN(T1)
	  ELSE
	   W2 = 1.
	  END IF
	  W2 = W2*W2*S4(I)
	  W(I) = 1/W2
	 END IF
10	CONTINUE

	RETURN
	END

	   	
 

C			** XFORM **
C
C   Transforms station and bearing data to an earth-centered coordinate
C   system.

C   Input : I,B1,S1,S2,PI
C   Output : E1,E2,E3,E4,E5,E6  

	SUBROUTINE XFORM(I)

	INCLUDE '(COMBLK)'

	REAL T3(5)

	T1 = B1(I)
	B3 = COS(T1)
	B4 = -SIN(T1)
	X8 = PI/2 - S1(I)
	C4 = -COS(X8)

	X9 = S2(I)
	T3(1) = COS(X9)
	T3(4) = -SIN(X9)
	T3(2) = -C4*T3(4)
	T3(5) = T3(1)*C4
	T3(3) = SIN(X8)

	E1(I) = T3(1)*B3 + T3(2)*B4
	E2(I) = T3(3)*B4
	E3(I) = T3(4)*B3 + T3(5)*B4
	E4(I) = -B4*T3(1) + T3(2)*B3
	E5(I) = T3(3)*B3
	E6(I) = -B4*T3(4) + T3(5)*B3

	RETURN
	END




C			** XPRODBPE **
C
C   Computes bearing plane intersections, weights the intersections, and
C   computes the latitude and longitude of the fix point by evaluating
C   the weighted intersections.

C   Input : W,S1,E1,E2,E3,E4,E5,E6,O1,C1
C   Output : P,T (fix point),FIXED

	SUBROUTINE XPRODBPE( O1, FIXED )

	INTEGER 	O1
	LOGICAL 	FIXED

	INCLUDE '(COMBLK)'

	REAL V(3),P1(3),U1(3)

	DO 10 I=1,3
	 U1(I) = 0.
10	 V(I) = 0.

	L = I1-1
	DO 50 I=1,L
	 IF (W(I) .NE. 0.) THEN

	  DO 40 J=I+1,I1
	   IFLAG = 0
	   W1 = W(I)*W(J)
	   IF (W1 .NE. 0.) THEN
	    IF (S1(I) .NE. S1(J)) THEN
	     P1(1) = (E2(I)*E3(J) - E3(I)*E2(J))*W1
	     P1(2) = (E3(I)*E1(J) - E1(I)*E3(J))*W1
	     P1(3) = (E1(I)*E2(J) - E2(I)*E1(J))*W1
	     D2 = P1(1)*E4(I) + P1(2)*E5(I) + P1(3)*E6(I)
	     D3 = P1(1)*E4(J) + P1(2)*E5(J) + P1(3)*E6(J)

	     IF (D2*D3 .GE. 0.) THEN
	      IF (D2 .LT. 0.) THEN
	       DO 20 K=1,3
20	        P1(K) = -P1(K)
	       IF (O1 .NE. 0) THEN
		T1 = SQRT(P1(1)*P1(1) + P1(2)*P1(2) + P1(3)*P1(3))
		DO 30 K=1,3
		 P1(K) = P1(K)/T1
		 T1 = P1(K) - C1(K)
		 U1(K) = T1*T1
30		CONTINUE
		D = SQRT(U1(1) + U1(2) + U1(3))
		IF (D .GE. 0.174533) IFLAG=1
	       END IF
	      END IF
	      IF (IFLAG .EQ. 0) THEN
	       DO 35 K=1,3
35	        V(K) = V(K)+P1(K)
	      END IF
	     END IF

	    END IF
	   END IF
40	  CONTINUE

	 END IF
50      CONTINUE	

	T1 = SQRT(V(1)*V(1) + V(2)*V(2) + V(3)*V(3))
	IF (T1 .EQ. 0.) THEN
D	  WRITE (LW,*) T1
D	  WRITE (LW,*) 'NO FIX'
C	  CALL NOFIX(LW)
	  FIXED = .FALSE.
	END IF

	IF ( FIXED ) THEN
	  DO 60 I=1,3
60	    C1(I) = V(I)/T1

	  P = ASIN(C1(2))
	  T = ATAN(V(1)/V(3))
	  IF (V(3) .LT. 0.) THEN
	    IF (V(1) .GE. 0.) THEN
	      T = T+PI
	    ELSE
	      T = T-PI
	    END IF
	  END IF

	  S5 = SIN(P)
	  C5 = COS(P)
C	  WRITE (LW,70) P*RONE,T*RONE
70	  FORMAT (1X,'PHI = ',F10.4,' THETA = ',F10.4)
	END IF

	RETURN
	END
