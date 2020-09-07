#! /bin/bash
#python FODPSim.py -D 121 -kb 9 -addT False -fb 2 -percent $1
#python FODPSim.py -T 0 -D 169 -M 48 -S 2 -kb 11 -mb 2 -addT False -fb $1 -percent 0.01 -type 2
#python FODPSim.py -T $2 -D 168 -M 48 -S 8 -kb 17 -mb 3 -addT False -percent $1 -type 0
#python FODPSim.py -T $2 -D 177 -M 48 -S 8 -kb 11 -mb 2 -addT False -percent $1 -type 0
#python FODPSim.py -T 12 -D 168 -M 48 -S 2 -kb 17 -mb 3 -addT False -percent $1 -type 1

#python FODPSim.py -T $2 -D 169 -M 48 -S 8 -kb 11 -mb 2 -addT False -percent $1 -type 1

#python FODPSim.py -T 12 -M 48 -D 171 -S 2 -kb 11 -mb 2 -kt 10 -mt 2 -fb 1 -ft 1 -percent $1 -type 0
#python FODPSim.py -T 24 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 10 -mt 2 -percent $1 -type 0


#python FODPSim.py -T 24 -D 169 -M 48 -S 2 -kb 11 -mb 2 -addT False -fb $2 -percent $1 -type 2










#python FODPSim.py -T $2 -M 48 -D 168 -S 8 -kb 17 -mb 3 -kt 10 -mt 2 -fb 1 -ft 1 -percent $1 -type 0
#python FODPSim.py -T $2 -M 48 -D 169 -S 8 -kb 11 -mb 2 -kt 5 -mt 1 -fb 12 -ft 3 -percent $1 -type 2

#python FODPSim.py -T 72 -M 48 -D 169 -S 8 -kb 17 -mb 3 -fb 1 -ft 1 -percent 0.005 -typeb $1 -typet $1 -networkBW 10

#python FODPSim.py -T 48 -M 48 -D 169 -S 8 -kb 11 -mb 2 -fb 1 -ft 1 -percent 0.01 -typeb $1 -typet $1 -networkBW 4
#python FODPSim.py -T 48 -M 48 -D 169 -S 8 -kb 17 -mb 3 -fb 1 -ft 1 -percent 0.01 -typeb $1 -typet $1 -networkBW 4

#for f in 0.001 0.002 0.003 0.004 0.005 0.006 0.007 0.008 0.009 0.01
#for f in 8 12 16 20 24 28 32 36 40 44 48 52 56 60
#for f in 2 4 6 8 10 12
#do
	#python FODPSim.py -T 94 -M 96 -D 84 -S 4 -kb 8 -mb 2 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 1
	#python FODPSim.py -T 94 -M 96 -D 84 -S 4 -kb 8 -mb 2 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 1
	#python FODPSim.py -T 94 -M 48 -D 168 -S 8 -kb 8 -mb 2 -fb 13 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 1
	#python FODPSim.py -addT True -T 94 -M 48 -D 168 -S 12 -kb 12 -mb 1 -kt 11 -mt 1 -fb 13 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 1
	#iiiiipython FODPSim.py -addT True -M 48 -D 169 -S 8 -kb 11 -mb 2 -kt 11 -mt 1 -fb $f -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
	#python FODPSim.py -T 0 -M 48 -D 169 -S 0 -kb 9 -mb 4 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 4
	#python FODPSim.py -T 0 -addT True -M 48 -D 168 -S 8 -kb 17 -mb 3 -kt 10 -mt 2 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 4
	#python FODPSim.py -T 96 -M 96 -D 84 -S 6 -kb 17 -mb 3 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 4
	#python FODPSim.py -T 96 -addT True -M 96 -D 84 -S 6 -kb 12 -mb 1 -kt 11 -mt 1 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 4
	#python FODPSim.py -T 34  -M 1 -D 126 -S 6 -kb 8 -mb 2 -fb 1 -ft 1 -percent $f -typeb $1 -typet $1 -networkBW 4
#done



#for x in 0.001 0.002 0.003 0.004 0.005 0.006 0.007 0.008 0.009 0.01
#for t in 0.01 0.02 0.03 0.04 0.05
#for t in 24 48 72 96 120
#do
#	python FODPSim.py -addT True -T $t -M 48 -D 169 -S 13 -kb 12 -mb 1 -kt 11 -mt 1 -fb 13 -ft 1 -percent 0.01 -typeb 0 -typet 0 -networkBW 1
#	python FODPSim.py -T $t -M 48 -D 169 -S 13 -kb 11 -mb 2 -fb 13 -ft 1 -percent 0.01 -typeb 0 -typet 0 -networkBW 1
#	python FODPSim.py -T $t -M 48 -D 169 -S 8 -kb 11 -mb 2 -fb 13 -ft 1 -percent 0.01 -typeb 4 -typet 4 -networkBW 1
#	python FODPSim.py -T $t -M 48 -D 169 -S 8 -kb 11 -mb 2 -fb 13 -ft 1 -percent 0.01 -typeb 2 -typet 2 -networkBW 1
#done


#for f in 1 3 5 7 9 11 13
#do
#	python FODPSim.py -addT True -T 120 -M 48 -D 169 -S 8 -kb 11 -mb 2 -kt 5 -mt 1 -fb $f -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#done

#for x in 1 2 3 4 5 6 7 8
#do
#	python FODPSim.py -addT True -T 120 -M 48 -D 169 -S 8 -kb 11 -mb 2 -kt 5 -mt 1 -fb 1 -ft $x -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#done



#for t in 0 1 2
#do
#	   python FODPSim.py -addT True -T 120 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 47 -mt 1 -fb 13 -ft 1 -percent 0.05 -typeb $t -typet $t -networkBW 1
#done

#for fb in 1 3 5 7 9 11 13
#do
#	python FODPSim.py -T 120 -addT True -T 120 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb $fb -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#done

#for ft in 1 2 3 4 5 6 7 8
#do
#	python FODPSim.py -T 120 -addT True -T 120 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 1 -ft $ft -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#done
#for fb in 4 5 6 7 8 9 10 11 12 13 
#do 
#	python FODPSim.py -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb $fb -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#done

#for f in 0.002 0.004 0.006 0.008 0.01 0.012 0.014 0.016 0.018 0.2
#do
#	python FODPSim.py -T 0 -M 48 -D 169 -S 8 -kb 11 -mb 2 -fb 13 -percent $f -typeb 0 -typet 0 -networkBW 1
	#python FODPSim.py -T 0 -addT True -M 48 -D 169 -S 13 -kb 12 -mb 1 -kt 11 -mt 1 -fb 1 -ft 1 -percent $f -typeb 0 -typet 0 -networkBW 1
	#python FODPSim.py -T 0 -M 48 -D 169 -S 8 -kb 11 -mb 2 -fb 13 -percent $f -typeb 4 -typet 4 -networkBW 1
#done

#for t in 0.05
#do
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 11 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 9 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 7 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 5 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 3 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 1 -ft 1 -percent 0.05 -typeb 2 -typet 2 -networkBW 1
#	python FODPSim.py -T $t -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent 0.05 -typeb 0 -typet 0 -networkBW 1
#	#python FODPSim.py -T 120 -addT True -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent 0.05 -typeb 1 -typet 1 -networkBW $n
#done
#for fb in 1 3 5 7 9 11 13
#for f in 0.004 0.006 0.008 0.01

#for t in 0 1 2
#do
#	python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent 0.01 -typeb $t -typet $t -networkBW 1
#done
#        python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 14 -ft 1 -percent 0.01 -typeb 2 -typet 2 -networkBW 1



#for f in 0.002 0.004 0.006 0.008 0.01
#do
	#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 173 -S 4 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent $f -typeb 0 -typet 0 -networkBW 1
	#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent $f -typeb 1 -typet 1 -networkBW 1
	#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent $f -typeb 2 -typet 2 -networkBW 1
	#python FODPSim.py -T 120 -plus1 True -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent $f -typeb 2 -typet 2 -networkBW 1
	#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 14 -ft 1 -percent $f -typeb 2 -typet 2 -networkBW 1
#done


#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 173 -S 4 -kb 11 -mb 2 -kt 5 -mt 1 -fb 14 -ft 1 -percent 0.01 -typeb 0 -typet 0 -networkBW 1
#for fb in 2 3 4 5 6 7 8 9 10 11 12 13
for fb in 14
do
       python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb $fb -ft 1 -percent 0.01 -typeb 2 -typet 2 -networkBW 1
done
#python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 14 -ft 1 -percent 0.01 -typeb 1 -typet 1 -networkBW 1


#for f in 0.002 0.004 0.006 0.008 0.01
#do
#	python FODPSim.py -T 120 -diskCap 16 -plus1 False -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 14 -ft 1 -percent $f -typeb 2 -typet 2 -networkBW 1
#done

       #python FODPSim.py -T 120 -diskCap 16 -M 48 -D 169 -S 13 -kb 11 -mb 2 -kt 5 -mt 1 -fb 13 -ft 1 -percent $1 -typeb $2 -typet $2 -networkBW 1
