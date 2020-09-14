def frecuency(freqlist, cleanlist):
	
	listmax=list()
	i=int()
	while(len(listmax) <301):
		spl=freqlist[i].split('\t')
		freq=spl[0]
		term=spl[1]
		if(term in cleanlist):
			listmax.append(freqlist[i])
		i=i+1
		
	return(listmax)

def frequencyTerm(freqlist, termin):
	freqTerm=int()
	for i in freqlist:
		spl=i.split('\t')
		freq=spl[0]
		term=spl[1][:-1]
		if(termin in term):
			freqTerm=freq


	return(freqTerm)

