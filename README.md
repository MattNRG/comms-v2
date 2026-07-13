# Server & Client Handler
Updated version of NRG RoboCup Wi-Fi Handler. This is under development and research thus It's not yet on the main repository.

<img width="2500" height="500" alt="Banner (2500 x 500 px)" src="https://github.com/user-attachments/assets/28f648a0-d93e-4b2f-8866-cc844aa6deb1" />


## What changed?

Got rid of _Tie 'n' Pair_ replacing it with a new system. Using a static IP, the robots send connection requests themselves, avoiding the problem of looking for robots only at the start of the program. Likewise, using STREAM, not DGRAM, we can leave the connections open for easier messaging. 

Everything is threaded (Maybe a bit too much), making sure everything gets through and processed.

And finally, we no longer use JSON to save the IP's (Since the robots can connect at any time), and it's replaced with classes.


> "If I’ve learned one thing, it’s that before you get anywhere in life, you have to stop listening to yourself"
Jerry Smith

That being said, the old code is rubbish and the newer is way more modular. (Hopefully)


## Testing Equipment

- TP-Link TL-WR844N

- MacBook Pro 2020

- Raspberry Pi 4

## Updates

- **Threads and Heartbeat**: *Moved to classes, and now using a heartbeat to check if the robot is still connected.*
- **Pack and Unpack [WORKING ON IT]**: *Implemented Structs to pack and unpack data.*
