from midiutil.MidiFile import MIDIFile 
import pickle
import torch
import numpy as np

with open("pitch_data.pkl", "rb") as f:
    dic = pickle.load(f)
    train_X = dic["X"]
    train_Y = dic["Y"]

with open("model_prediction_CNN.pkl", "rb") as f:
	prediction = pickle.load(f)

with open("sample_prediction.pkl", "rb") as f:
	cnn_predict = pickle.load(f)

with open("prediction.pkl", "rb") as f:
	lstm_prediction = pickle.load(f)

print(len(prediction))

def midi_generator(X, Y, Z, n):
	track = 0
	channel = 0
	volume = 100
	MyMIDI = MIDIFile(3)
	label_track = 1
	prediction_track = 2
	time = 0
	tempo = 60
	MyMIDI.addTempo(track,time, tempo)
	for i, item in enumerate(X[n]):
		time = float(item[0])
		duration = float(item[1]) - float(item[0]) 
		#time = i
		#duration = 1
		pitch = int(item[2])
		flag = int(Y[n][i])
		MyMIDI.addNote(track,channel,pitch,time,duration,volume)
		if(flag == 4):
			MyMIDI.addNote(label_track,channel,90,time,duration,volume)
		flag = int(Z[n][i])
		if(flag == 1):
			MyMIDI.addNote(prediction_track,channel,30,time,duration,volume)

	midifile = open("/Users/Fischer/NYU/MusicStructuralAnalysis_Project/sample_prediction/sample{}.mid".format(int(n)), "wb")
	MyMIDI.writeFile(midifile)
	midifile.close()

for i in range(1300, 1373):
	midi_generator(train_X, train_Y, prediction, i)


def crf_midi_generator(X, Y, Z, n):
	track = 0
	channel = 0
	volume = 100
	MyMIDI = MIDIFile(3)
	label_track = 1
	prediction_track = 2
	time = 0
	tempo = 60
	MyMIDI.addTempo(track,time, tempo)
	print(Z["out"][2].shape)
	print(X[n].shape)
	for i, item in enumerate(X[n]):
		time = float(item[0])
		duration = float(item[1]) - float(item[0])
		#time = i
		#duration = 1
		pitch = int(item[2])
		flag = int(Y[n][i])
		MyMIDI.addNote(track,channel,pitch,time,duration,volume)
		if(flag == 2):
			MyMIDI.addNote(label_track,channel,90,time,duration,volume)
		flag = int(Z["out"][0][i])
		if(flag == 1):
			MyMIDI.addNote(prediction_track,channel,30,time,duration,volume)

	midifile = open("sample.mid", "wb")
	MyMIDI.writeFile(midifile)
	midifile.close()

#crf_midi_generator(train_X, train_Y, lstm_prediction, 1285)


def cnn_midi_generator(X, Y, Z, n):
	track = 0
	channel = 0
	volume = 100
	MyMIDI = MIDIFile(3)
	label_track = 1
	prediction_track = 2
	time = 0
	tempo = 60
	MyMIDI.addTempo(track,time, tempo)
	for i, item in enumerate(X[n]):
		time = float(item[0])
		duration = float(item[1]) - float(item[0])
		#time = i
		#duration = 1
		pitch = int(item[2])
		flag = int(Y[n][i])
		MyMIDI.addNote(track,channel,pitch,time,duration,volume)
		if(flag == 4):
			MyMIDI.addNote(label_track,channel,90,time,duration,volume)
		flag = int(Z[n - 1300][i])
		if(flag == 1):
			MyMIDI.addNote(prediction_track,channel,30,time,duration,volume)

	midifile = open("/Users/Fischer/NYU/MusicStructuralAnalysis_Project/sample_prediction/CNN_sample{}.mid".format(int(n)), "wb")
	MyMIDI.writeFile(midifile)
	midifile.close()

for i in range(1300, 1373):
	cnn_midi_generator(train_X, train_Y, cnn_predict, i)



"""new_train_y = []
for i, target in enumerate(train_Y):
	two_list = []
	four_list = []
	new_label = np.zeros_like(target)
	# in case of bad data
	target[-1] = 4
	loc = 0
	two_list.append(0)
	for label in target:
		if int(label[0]) == 4:
			two_list.append(loc + 1)
			four_list.append(loc)
		loc = loc + 1
	two_list.pop()
	if (len(two_list) != len(four_list)):
		print(i, len(two_list), len(four_list))
		print(target)
	for i in range(len(two_list)):
		start = two_list[i]
		end = four_list[i]
		mid = (start + end) // 2
		new_label[mid + 1:end + 1] = 1
	new_train_y.append(new_label)
print(new_train_y[100].reshape(-1))
f = open("balanced_target.pkl", "wb")
pickle.dump(new_train_y, f)
f.close()"""

