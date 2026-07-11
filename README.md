# comms-v2
Updated version of NRG RoboCup Wifi Handler. This is under development and research thus It's not yet on the main repository.

**What changed?**
Got rid of _Tie 'n' Pair_ replacing it with a new system. Using a static IP, the robots send connection requests themselves avoiding the problem of looking for robots only at the start of the program. Likewise using STREAM not DGRAM we can leave the connections open for easier messaging. 

Everything is threaded (Maybe a bit too much), making sure everything gets through and processed.

And finally, we no longer use json to save the IP's (Since the robots can connect at any time) and is replaced with a simple directory.


"If I’ve learned one thing, it’s that before you get anywhere in life, you gotta stop listening to yourself"

That being said, the old code is rubbish and the newer is way more modular. (Hopefully)
