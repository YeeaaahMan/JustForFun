from lxml import etree

def whatKey(string):
    """Function takes number of 'keys combination' and returns combination's string format."""
    n = int(string)
    letter = n & 0b11111111
    if n & 0b1111111100000000 == 16384:
        if letter < 96:
            return 'Ctrl+' + chr(letter)
        else:
            return 'Ctrl+' + numKey(letter)
    elif n & 0b1111111100000000 == 32768:
        if letter < 96:
            return 'Alt+' + chr(letter)
        else:
            return 'Alt+' + numKey(letter)
    elif n & 0b1111111100000000 == 8192:
        if letter < 96:
            return 'Shift+' + chr(letter)
        else:
            return 'Shift+' + numKey(letter)
    else:
        return 'None' #'UnknownKey+' + chr(letter)
    
def numKey(keycode):
    """for i in range(0, 10):
    NumKeys.setdefault(i+96, 'NumPad' + str(i))"""
    NumKeys = {
        96: 'NumPad0',
        97: 'NumPad1',
        98: 'NumPad2',
        99: 'NumPad3',
        100: 'NumPad4',
        101: 'NumPad5',
        102: 'NumPad6',
        103: 'NumPad7',
        104: 'NumPad8',
        105: 'NumPad9',
        106: 'Multiply',
        107: 'Add',
        108: 'UnknownKey',
        109: 'Subtract',
        110: 'Decimal',
        111: 'Divide',
        186: 'Oem1',
        188: 'Oemcomma',
        190: 'OemPeriod',
        191: 'OemQuestion',
        192: '~',
        219: 'OemOpenBrackets',
        220: 'Oem5',
        221: 'Oem6',
        222: 'Oem7',
        226: 'OemBackslash'
        }
    return NumKeys[keycode]

print "Reading Settings.wot..."
inputFile = open('Settings.wot', 'r')

root = etree.Element("root")
print "Creating XML tree..."

# .decode("cp1251") changes coding cp1251 to Unicode (need for LXML module)
Line = inputFile.readline().strip().decode("cp1251")
while Line:
    prevLine = Line
    Line = inputFile.readline().strip().decode("cp1251")
    if not Line.isdigit():
        #print 'Line not digit'
        continue
    else:
        #print 'Line is digit'
        Description = prevLine
        Hotkey = whatKey(Line).decode("cp1251") # need, because sometimes combination exist non ASCII symbol
        Value = ['', '', '', '']
        #print 'reading macros'
        for m in range(4):
            lM = int(inputFile.readline().strip())
            for i in range(lM):
                Value[m] += inputFile.readline().decode("cp1251")
        #print Description, Hotkey
        
        record = etree.SubElement(root, "record", hotkey = Hotkey, type = "Autotext") #combination 'Hotkey'
        etree.SubElement(record, "description").text = Description #description's text 'Description'
        etree.SubElement(record, "text").text = "%COMMAND%"
        etree.SubElement(record, "logging").text = "No"

        variable = etree.SubElement(record, "variable", key = "%COMMAND%")
        etree.SubElement(variable, "value").text = Value[0] # macro1 'value[0]'
        etree.SubElement(variable, "value").text = Value[1] # macro2
        etree.SubElement(variable, "value").text = Value[2] # macro3
        etree.SubElement(variable, "value").text = Value[3] # macro4 'value[3]'

inputFile.close()

print 'Creating new.xml ...'
toXML = etree.tostring(root, pretty_print=True)       
applic = open("new.xml", "w") # file name
applic.writelines("""<?xml version="1.0" encoding="utf-8"?>\n""")
applic.writelines(toXML)
applic.close()

print ("\nDone! Press Enter to continue...")
raw_input()
