# What are you looking in here for?

from innate.weightedlist import WeightedList


# Oh, you found this?
toppings = {
  1: "reserved",
  2: "special rare",
  3: "too weird",
  4: "rarest wacky comments",
  5: "rarest, easter eggs",
  8: "slightly rarer wacky comments",
  10: "wacky comments",
  15: "internal or irrelevant",
  20: "thoughts, questions",
  25: "rarest trivia",
  50: "rarer trivia, helpful comments",
  75: "trivia",
  100: "actual advice",
}


# I don’t know why I categorised and ordered these, but for whoever’s looking, you’re welcome.
flavours = WeightedList(

  (10, "Feel."),
  (10, "Look."),
  (10, "Observe."),
  (10, "Analyze."),
  (10, "Find."),
  (10, "Actually, there is no algorithm. Only rhythm."),
  (10, "Pro tip – do NOT play with liquid containers nearby."),
  (10, "Music is love, music is life."),
  
  (100, "Note patterns can sometimes spell out words."),
  (100, "The colours of notes and lanes correspond to which row of the keyboard their key is in."),
  (100, "If a note’s colour is different to the lane’s, it’s probably a shock note."),
  (100, "Hold notes do not actually have to be held for their entire duration."),
  (100, "It may help to press the key with 2 fingers for roll notes."),
  (100, "Shock notes can be quite a shock."),
  (100, "Watch out for lane switcheroos."),
  (100, "Hitting a note way off results in a miss hit and breaks your chain."),
  
  (10, "The 4 difficulties are Standing, Advancing, Expecting and... Insecurity?"),
  (50, "Higher difficulties have stricter accuracy leniency and faster note speeds."),
  (50, "You don’t have to be an expert to play an Expert chart."),
  (50, "Insane difficulty isn’t always insane. It’s just more insane than the 3 before it. Which probably makes it quite insane."),
  (50, "Remember, no matter how difficult it is, it can always be more so."),
  (75, "The highest accuracy score is 100,000."),
  
  (50, "You can create multiple accounts to save progress and settings."),
  
  (50, "Algorhythm is highly inspired by Phigros."),
  (50, "Algorhythm features original music created by yours truly (in GarageBand)."),
  (50, "Development on Algorhythm began the day it was conceptualised."),
  (50, "This idle backing soundtrack is called ‘Dawn’."),
  (50, "The first chart added to Algorhythm was ‘End of Time’s instrumental version, as the tutorial chart."),
  (15, "No, Algorhythm is not coded in ALGOL. It’s Python."),
  (5, "Algorhythm’s source code can be found on – wait, why would you want to see that?"),
  
  (25, "Remember to go soft on the keyboard."),
  (25, "Algorhythm doesn’t actually need sound effects if the keyboard already makes clicky sounds. Genius."),
  (25, "If you want hit sound effects, just use a mechanical keyboard :5head:"),
  (25, "Rip to anyone not playing this on a QWERTY keyboard. But hey, that’s a cool challenge."),
  (25, "No matter how difficult we make this, it seems someone’s still going to Apex Perfect it."),
  (15, "Please don’t file a copyright complaint."),
  
  (20, "Oh, you want harder charts?"),
  (20, "So, what if there were another difficulty above Insane?"),
  (20, "Why are they called tap notes when it’s not a touchscreen game?"),
  (20, "Just how many lanes could we add?"),
  (20, "Anyone trying this one-handed?"),
  (20, "Which F# minor arpeggio is playing Algorhythm on mobile?"),
  (20, "Hand acrobatics is fun, isn’t it?"),
  (20, "Anyone play better under pressure?"),
  (10, "Does music breathe you back to life?"),
  (10, "Did you know there are secret achievements?"),
  (10, "I wonder just how many easter eggs are in this game..."),
  (10, "Anyone opening and closing this game repeatedly to discover these?"),
  
  (20, "Creating a chart is tougher than it seems."),
  (20, "A chart editor is an even more horrifying idea than coding this as your first game."),
  (20, "One day, the hitline will multiply."),
  (20, "Just hear me out on this – what if notes could span multiple lanes?"),
  (20, "Adding click notes to this game would be evil. Maybe we should do it?"),
  (15, "Colour interpolation is surprisingly problematic."),
  (15, "What hue does black have in HSV and HSL?"),
  (15, "Rumour has it pressing a specific key combination here lets you skip the loading screen. No idea why you would want to do that though."),
  (15, "Legend has it all this typing while playing Algorhythm is executing an algorithm to hack into the mainframe."),
  (15, "If you’re really, really good, you might be able to reach a chain higher than the total number of notes in the chart."),
  
  (10, "Uh, we’re not actually loading anything. Just to be clear. Enjoy the experience."),
  (10, "These flavours probably make Algorhythm a whole lot less professional. But hey, we’re here to have fun, so whatever :v"),
  (10, "If rhythm games have huge collections of soundtracks, shouldn’t their file size be huge too?"),
  (10, "Praise be to Stack Exchange, without which this project would have been mildly more difficult."),
  (10, "Just because it’s open source doesn’t mean you should peak at the code. Shoo, you."),
  
  (8, "These are called flavours, just for fun. No, not flavour text, just flavours. Yum."),
  (8, "We could get so weird with these."),
  (8, "What’s your favourite flavour?"),
  (8, "The flavours just keep on coming."),
  (8, "This is the 26th flavour. (not really)"),
  (8, "Divulging Algorhythm’s secrets through these is fun."),
  (8, "Kinda out of ideas. Flavours, anyone?"),
  (8, "One day there’ll be so many of these that seeing the same one again would itself be an achievement."),
  (10, "This is a rare flavour. Or is it?"),
  (2, "This is a rare flavour."),
  (2, "Is this load time even long enough to read all this text? Hey, what if I just write a thesis on audio analysis and automated syncing right here, then..."),
  
  (10, "Screw PEP 8."),
  (5, "Always and forever, till the end of time."),
  (4, "sup"), # FIXME
  (4, "I love technical redstone."),
  (4, "Hey, capitalising the S in InSane looks cool."),
  (4, "Mushroom soup is heavenly, en dash."),
  (4, "WHERE THE CLUTCH CATALYST AT"),
  (4, "Is this background true black? Hmmm..."),
  (4, "This loading music’s pretty dope, I wonder who made it?"),
  (4, "Everything is a human construct...?"),
  (3, "We can solve this with geometric construction."),
  (3, "So, is it pronounced ‘fee-grow’, ‘figh-grow’, ‘figh-gross’, ‘figh-groze’? ‘figh-g-ross’, anyone??"),
  (3, "Yo pigeons, I got your hair growth – wait no, that’s my web fluid. Never mind."),

)
