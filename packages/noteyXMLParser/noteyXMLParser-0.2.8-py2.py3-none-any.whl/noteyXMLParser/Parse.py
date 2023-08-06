

import xml.etree.ElementTree as ET
from .Objects import *
import json
from collections import deque
from .CreateDict import *
'''
    class to parse the xml file and then create the json file

'''
class XMLParser:
    def __init__(self, score_path, fileData = False) -> None:
        if fileData:
            self.root = ET.fromstring(score_path)
        else:
            self.tree = ET.parse(score_path)
            self.root = self.tree.getroot()
        self.final_string = ""
        self.fingerDict = createfingerDict()
        self.chroma_to_chord = createChromaToChord()
        self.sharpMap = {"sharp": "#", "flat": "b", "natural": ""}
        self.bMap = {"Cb": "B", "Db": "C#", "Eb": "D#", "Fb": "E", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
        self.noteMemo = {}

    def parse(self):
        playString = self.getNotes()
        beatBase, beat_type = self.getTimeSignature()
        beat_unit, bpm = self.getBPMCounter()
        return playString, beatBase, bpm

    def getTimeSignature(self):
        beats = None
        beat_type = None
        for value in self.root.iter("time"):
            beats = value.find('beats').text
            beat_type = value.find('beat-type').text

        if beats is None:
            beats = "no beats found"
        if beat_type is None:
            beat_type = "no beat type found"
        return [beats, beat_type]

    def getBPMCounter(self):
        beat_unit = None
        bpm = None
        for value in self.root.iter("metronome"):
            beat_unit = value.find('beat-unit').text
            bpm = value.find('per-minute').text
        if beat_unit is None:
            beat_unit = "no beat unit found"
        if bpm is None:
            bpm = "no bpm found"
        return beat_unit, bpm

    def getFignerNotation(self, pitch):
        if pitch in self.fingerDict:
            return self.fingerDict[pitch]
        else:
            return " , , "
    
    # function to handle accidentals(sharps etc)
    def accidentalHandler(self, pitch, accidental):
        if accidental in self.sharpMap:
            inputPitch = pitch + self.sharpMap[accidental]
            if inputPitch in self.bMap:
                return self.bMap[inputPitch]
            else:
                return inputPitch
        else:
            return pitch + accidental

    def parseNoteIter(self, parentIter, noteIter) -> PlayedNote:
        if (parentIter.find('accidental') != None):  
            # check if key is in sharpMap
            prevNote = str(noteIter.find('step').text) + "_" + str(int(noteIter.find('octave').text) - 1)
            note = self.accidentalHandler(str(noteIter.find('step').text), str(parentIter.find('accidental').text)) + "_" + str(int(noteIter.find('octave').text) - 1)
            if prevNote in self.noteMemo:
                self.noteMemo[prevNote] = note
        else:
            note = str(noteIter.find('step').text) + "_" + str(int(noteIter.find('octave').text) - 1)
            if note in self.noteMemo:
                note = self.noteMemo[note]

        duration = int(parentIter.find('duration').text)
        type = str(parentIter.find('type').text)
        return PlayedNote(note,  duration, NoteDuration[type], self.getFignerNotation(note))
    
    def getNotes(self):
        note_list = []
        chord_end = False
        chord_start = False
        chord_note_queue = deque()
        
        for measure in self.root.iter('measure'):
            for neighbor in measure.iter('note'):
                if (neighbor.find('chord') != None):
                    if note_list[-1].noteType == 0 and not chord_start:
                        chord_start = True
                        print("First not of the chord", note_list[-1].pitch)
                        chord_note_queue.append(note_list.pop())
                        for pitch in neighbor.iter('pitch'):
                            print("Rest of the notes in the string", str(pitch.find('step').text) + "_" + str(int(pitch.find('octave').text) - 1))
                            chord_note_queue.append(self.parseNoteIter(neighbor, pitch))
                    else:
                        for pitch in neighbor.iter('pitch'):
                            print("Rest of the notes in the string", str(pitch.find('step').text) + "_" + str(int(pitch.find('octave').text) - 1))
                            chord_note_queue.append(self.parseNoteIter(neighbor, pitch))
                        chord_end = True

                elif(neighbor.find('chord') == None and chord_end == True):
                    note_list.append(PlayedChord(chord_note_queue, self.chroma_to_chord))
                    print("Chord end")
                    for pitch in neighbor.iter('pitch'):
                            print("First not after a cord", str(pitch.find('step').text) + "_" + str(int(pitch.find('octave').text) - 1))
                            note_list.append(self.parseNoteIter(neighbor, pitch))
                    chord_end = False
                    chord_start = False
                    chord_note_queue = deque()

                else:
                    for pitch in neighbor.iter('pitch'):
                        note_list.append(self.parseNoteIter(neighbor, pitch))   
                    if (neighbor.find('dot') != None):
                        note_list[-1].addDot()

                    if(neighbor.find('tie') != None):
                        if (neighbor.find('tie').get('type') == "start"):
                            print("tie started @  with note ",  note_list[-1].pitch, "duration", note_list[-1].type)
                            note_list[-1].addTie(True)
                        else:
                            note_list[-1].addTie(False)
                            dur = 0
                            print("tie ended @  with note ",  note_list[-1].pitch, "duration", note_list[-1].type)
                            for i, node in reversed(list(enumerate(note_list))):
                                if node.tie == True:
                                    node.addTie(False)
                                    node.type += dur
                                    del note_list[i+1:]
                                    break
                                else:
                                    dur += node.type
                            print("note type summed @  with note ",  note_list[-1].pitch, "duration", note_list[-1].type)
            self.noteMemo = {}
        final_string = ""
        for i in note_list:
            final_string += i.createString()  + " "
        return final_string
