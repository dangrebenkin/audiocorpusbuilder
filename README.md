# About

Audiocorpusbuilder-package was made to automatically create a russian language audio corpus from YouTube videotracks playlists: it downloads video's audio and subtitles, makes pairs "sound-text" and saves them in the directory. If there are not subtitles for the video, audiocorpusbuilder misses it.

# Installing

For installation you need Python 3.6 or later and OC Linux on your local machine. You can install audiocorpusbuilder from the PyPi using the following command:

pip3 install audiocorpusbuilder

# Start

To run audiocorpusbuilder you shoild prepare directories for audiotracks, subtitles, results (directories should be like '/home/Audio/'). Also you need to create playlists.txt with playlists' links, every link should be on the separate line.

# Arguments

All arguments are required for program use.

1. -p URL_list

Playlists txt-file path.

2. -a directory_audio

Path to download audiotracks.

3. -s directory_subtitles

Path to download subtitles.

4. -r directory_results

Path to results.

# Usage

python3 acbr [-p URL_list] [-a directory_audio] [-s directory_subtitles] [-r directory_results] 

# Example

acbr -p playlists.txt -a Audio -s Subs -r Results
