#final code
#library importsz
import sys
import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
warnings.filterwarnings("ignore")
try:
	import librosa
	import scipy
	import wave
	import urllib
	import numpy as np
	import matplotlib.pyplot as plt
	from pydub import AudioSegment
	from pydub.utils import db_to_float
	from pydub.silence import split_on_silence
	from pydub.silence import detect_silence
	import math
	from scipy import stats
	from scipy.stats import norm, skew
	import pandas as pd
	import seaborn as sns
	import glob
	import librosa.display
	import matplotlib.pyplot as plt

except ImportError as error2:
    print(sys.exc_info()[0])
    print('This error is aPlease use pillow version 4.0.0')
try:
#load data
	data,sampling_rate = librosa.load('C:\\Users\\YASHSHAVI KASHYAP\\Downloads\\human.wav')
	m= data.size

#duration
	duration=int(m/sampling_rate)#duration of audio

#furrier transform of data
	data_fft = np.fft.rfft(data)

#frequencies
	frequencies = np.abs(data_fft)

#maximum pitch
	maxp=np.argmax(frequencies)

	arr=[117]*len(frequencies)
	sumf=0
	for i in range(0,len(frequencies)):
		if int(frequencies[i])>0 and int(frequencies[i])<int(maxp):
			arr[i]=int(frequencies[i])
			sumf=sumf+i

	minp=arr.index(min(arr))#min pitch

	meanp=sumf/len(frequencies)#mean pitch

	noofsamples=data.size
#data_fft is fourier transform of data

#total energy
	Et=np.sum(data**2)
	ef=np.sum(frequencies**2)/noofsamples

#power
	power=Et/duration


	plt.figure(2, figsize=(8,6))
	plt.subplot(211)
	Pxx, freqs, bins, im = plt.specgram(data, Fs=sampling_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
	cbar=plt.colorbar(im)
	plt.xlabel('Time (s)')
	plt.ylabel('Frequency (Hz)')
	cbar.set_label('Intensity dB')
	plt.close()

	#minimum intensity
	mini=cbar.vmin
	#maximum intensity
	maxi=cbar.vmax

	meani=(mini+maxi)/2
	sound = AudioSegment.from_wav("C:\\Users\\YASHSHAVI KASHYAP\\Downloads\\human.wav")
	chunks = split_on_silence(sound, 
			# must be silent for at least half a second
				min_silence_len=20,

			# consider it silent if quieter than -16 dBFS
				silence_thresh=-(round(abs(sound.dBFS))+100)
			)
#1000 means 1 sec then 60 second means
	sixty_seconds = 60 * 1000

	second_1_minute = sound[sixty_seconds:120000]
	hunks = split_on_silence(second_1_minute, 
    # must be silent for at least half a second
				min_silence_len=20,

    # consider it silent if quieter than -16 dBFS
				silence_thresh=-(round(abs(sound.dBFS))+100)
				)
#1000 means 1 sec then 60 second means

#SPEAKING RATE
	speaking_rate=len(hunks)/len(chunks)

	#SILENCES
	pauses=detect_silence(sound, min_silence_len=20, silence_thresh=-(round(abs(sound.dBFS))+100), seek_step=1)

#FINDING DURATIONS
	sumd=0
	ls=[]
	for start_i, end_i in pauses:
         dur=int(end_i)-int(start_i)
         ls.append(dur)
	breaks=[]

#VOICE BREAKS
	for i in ls:
		if i >900:
			breaks.append(i)
#SEPRATING BREAKES AND PAUSES
	ls=list(set(ls)-set(breaks))

#PUASES DURATION
	for i in ls:
		sumd=sumd+i

#TOTAL DURATION OF PAUSES
	durp=sumd

#NO OF PAUSES
	nop=len(ls)

#NO OF VOICE BREAKES
	noofVoiceBreaks=len(breaks)

#MAXIMUM DURATION OF PAUSES
	maximum_pause=max(ls)

#AVG DURATION OF PAUSES
	avgp=durp/nop

#FINDING PEAK
	peak=scipy.signal.find_peaks(data,rel_height=0.5)

#MAXIMUM FALLING AND MAXIMUM RISING

	MaxFalling=np.amin(data)
	MaxRising=np.amax(peak[0])
	sums=0



#JITTER, SHIMMER, JITTERRAP 
	for i in range(1,len(peak[0])-1):
		sums=sums+abs(20*math.log10(peak[0][i+1]/peak[0][i]))

#SHIMMER
	shimmer=sums/(len(peak[0])-1)
	peakf=abs(np.fft.fft(peak[0]))
	sumps=0
	for i in range(1,len(peakf)-1):
		sumps=sumps+(peakf[i+1]**-1)-(peakf[i]**-1)

#JITTER
	jitter=sumps/(len(peakf)-1)
	sortedp=np.sort(peak[0])
	sortedf=abs(np.fft.fft(sortedp))
	dif=abs(sortedp[11]-sortedp[15])
	suh=0
	avgabsdiff=(dif)/4
	avgneigh1=(abs(sortedp[6]-sortedp[10]))
	avgneigh2=abs(sortedp[17]-sortedp[22])
	avg=(dif+avgneigh1+avgneigh2)/3

	for i in range(11,16):
		suh=suh+abs(sortedf[i]**-1)
	period=suh/5

#JITTERRAP
	jitterrap=(avgabsdiff+avg)/period


#NUMBER OF RISING, NUMBER OF FALLING, AVERAGE RISE, AVERAGE FALL

	noofrise=len(peak[0])

	avgtorise=noofrise/len(data)
	nooffall=0
	for i in data:   
		if i == np.amin(data):
			nooffall=nooffall+1

		avgtofall=nooffall/len(data)



	print("duration: "+str(duration)+"seconds\n")
	print("energy: "+str(Et)+"joule\n")
	print("power: "+str(power)+"joule/sec\n")
	print("min_pitch: "+str(minp)+"Hz\n")
	print("max_pitch: "+str(maxp)+"Hz\n")
	print("mean_pitch: "+str(meanp)+"Hz\n")
	print("intensityMin: "+str(mini)+"dB\n")
	print("intensityMax: "+str(maxi)+"dB\n")
	print("intensityMean: "+str(meani)+"dB\n")
	print("jitter: "+str(jitter)+"\n")
	print("shimmer: "+str(shimmer)+"dB\n")
	print("jitterRap: "+str(jitterrap)+"\n")
	print("numVoiceBrreaks: "+str(noofVoiceBreaks)+"\n")
	print("PercentBreaks: "+str(((noofVoiceBreaks/duration)*100))+"\n")
	print("speakRate: "+str(speaking_rate)+"wpm\n")
	print("numPauses: "+str(nop)+"\n")
	print("maxDurPauses: "+str(maximum_pause/1000)+"sec\n")
	print("avgDurPauses: "+str(avgp/1000)+"sec\n")
	print("TotDurPauses: "+str(durp/1000)+"sec\n")
	print("MaxRising: "+str(MaxRising)+"dB\n")
	print("MaxFalling: "+str(MaxFalling)+"dB\n")
	print("AvgToRise: "+str(avgtorise)+"dB\n")
	print("AvgToFall: "+str(avgtofall)+"dB\n")
	print("numRising: "+str(noofrise)+"\n")
	print("numFall: "+str(nooffall)+"\n")
except:
    pass
print('Data analysis (EDA)\n')
d=pd.DataFrame(data,columns=["Amplitudes"],index=None)

print('Data frame head\n')
print(d.head())
print('\nDataframe description\n')
print(d.describe())
print('\nAdding Fourier transform of signal i.e FREQUENCIES (corresponding to each amplitude) in dataframe\n')
freq=pd.DataFrame(data_fft)
d["frequencies"]=freq
print(d.head())
d.drop(["frequencies"],axis=1,inplace=True)
freq=pd.DataFrame(frequencies)
d["frequencies"]=freq
print('\nConsidering only real part of frequencies\n')
print(d.head())
print('\nMaximum frequency\n')
maxFr=d.sort_values(by="frequencies",ascending=False).head()
print(maxFr)
print('\n Info\n')
print(d.info())
print('Missing ratio')
missing_ratio=(d.isnull().sum()/len(d))*100
print(missing_ratio.sort_values(ascending=False))
print('\nfor analysing in time domain ,taking only those values which have there defined real part i.e droping those values which have null real part\n')

d.dropna(axis=0,inplace=True)
print('After droping')
print(d.info())
print('\n')
print(d.describe())
print('\n Total values: '+str(d['Amplitudes'].size))
print('\n Unique values: '+str(d['Amplitudes'].nunique()))

print('Visulisation')
print('\n JUPITER NOOTBOOK\n')

