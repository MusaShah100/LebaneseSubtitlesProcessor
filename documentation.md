# Lebanese Subtitle Processor Documentation

## Overview

`process_subtitles.py` is a Python script designed to process subtitle files (SRT format) from Lebanese movies and dramas, extracting conversational dialogues and non-responded lines. The script processes Arabic subtitles from 10 specified Lebanese productions, cleans the subtitle text, identifies conversations based on timing, and saves the results into two CSV files: `all_movies_conversations.csv` for dialogues and `all_movies_no_response.csv` for lines without responses. The script is tailored to handle Arabic text encoding and provides a user-friendly console output with colored formatting for better tracking of the processing workflow.

## Purpose

The script was developed to analyze subtitle files from Lebanese movies and dramas, focusing on conversational dynamics. It extracts two types of data:
- **Conversations**: Identifies two-person and multi-person dialogues based on timing gaps between subtitle lines.
- **Non-Responded Lines**: Captures standalone subtitle lines that do not have a conversational response within a specified time window.

This data can be used for linguistic analysis, dialogue pattern studies, or training conversational models with Arabic text from Lebanese productions.

## Dependencies

The script relies on the following Python libraries:
- `pysrt>=1.1.2`: For reading and parsing SRT subtitle files.
- `charset-normalizer>=3.3.2`: For detecting the encoding of SRT files, especially Arabic text.
- `colorama>=0.4.6`: For adding colored output to the console for better user experience.
- Standard Python libraries: `csv`, `os`, `re`, `uuid` (for generating unique conversation IDs).

### Installation

1. **Set Up a Virtual Environment**:
   - Create a virtual environment in your project directory:
     ```bash
     python -m venv D:\Projects\Office Work\LebaneseSubtitlesProcessor\.venv
     ```
   - Activate the virtual environment:
     ```bash
     D:\Projects\Office Work\LebaneseSubtitlesProcessor\.venv\Scripts\activate
     ```

2. **Install Dependencies**:
   - Install the dependencies using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

## Project Structure

- **Script**: `process_subtitles.py` (main script for processing subtitles).
- **Data Folder**: `D:\Projects\Office Work\LebaneseSubtitlesProcessor\Data` (stores SRT files for each movie/drama).
- **Output Files**:
  - `all_movies_conversations.csv`: Contains extracted dialogues (two-person and multi-person conversations).
  - `all_movies_no_response.csv`: Contains subtitle lines without a conversational response.

### Movies/Shows Processed

The script processes the following 10 Lebanese productions (movies and dramas) with Arabic subtitles:
1. *Where Do We Go Now?* (2011) - Movie
2. *Al Hayba (S5E1)* (2021) - Drama Series (Season 5, Episode 1)
3. *West Beirut* (1998) - Movie
4. *Capernaum* (2018) - Movie
5. *The Kite* (2003) - Movie
6. *Zozo* (2005) - Movie
7. *Perfect Strangers* (2022) - Movie (Lebanese version)
8. *Very Big Shot* (2015) - Movie
9. *Stray Bullet* (2010) - Movie
10. *The Salt of This Sea* (2008) - Movie (Palestinian-Lebanese co-production)

The corresponding SRT files are stored in the `Data` folder with the following filenames:
- `where_do_we_go_now.srt`
- `Al Hayba S05E01.ar.srt`
- `West.Beirut.WEBRip.Netflix.ar.srt`
- `Capernaum (2018).srt`
- `the_kite.srt`
- `zozo_arabic_only.srt`
- `Perfect Strangers 2022.srt`
- `Very.Big.Shot.2015.srt`
- `Stray.Bullet.2010.srt`
- `The Salt of This Sea (2008).srt`

## Usage

1. **Prepare SRT Files**:
   - Ensure all SRT files listed above are placed in the `Data` folder (`D:\Projects\Office Work\LebaneseSubtitlesProcessor\Data`).
   - Verify that the SRT files contain Arabic text by opening them in a text editor (e.g., Notepad++). Look for Arabic characters (e.g., `مرحبا`).

2. **Run the Script**:
   - Activate your virtual environment (see Installation section).
   - Execute the script:
     ```bash
     D:\Projects\Office Work\LebaneseSubtitlesProcessor\.venv\Scripts\python.exe D:\Projects\Office Work\LebaneseSubtitlesProcessor\process_subtitles.py
     ```

3. **Monitor Console Output**:
   - The script provides a formatted console output with colored text to track progress:
     - **Blue**: Indicates the start of processing for each movie (e.g., `[1/10] Processing 'Where Do We Go Now?'...`).
     - **Green**: Confirms successful completion (e.g., `✓ Movie 'Where Do We Go Now?' done!`).
     - **Yellow**: Shows transitions or warnings (e.g., `Processing next movie...` or encoding fallback messages).
     - **Cyan**: Displays headers and summary information (e.g., `Starting Subtitle Processing for 10 Movies/Shows`).
     - **Red**: Highlights errors (e.g., if an SRT file is missing).
   - A final summary shows the total movies processed, conversations extracted, and non-responded lines saved.

## Output Files

The script generates two CSV files in the project directory:

### 1. `all_movies_conversations.csv`

This file contains extracted dialogues from the subtitles, categorized into two types: two-person conversations and multi-person conversations.

#### Structure
- **Two-Person Conversations**:
  - Columns: `movie_title`, `timestamp`, `input`, `output`
  - Description: Captures dialogues where one subtitle line (input) is followed by another (output) within a 5-second gap, indicating a conversational exchange between two speakers.
  - Example:
    ```
    movie_title,timestamp,input,output
    "Where Do We Go Now?","00:01:23,456 --> 00:01:25,789","هل يمكننا الذهاب الآن؟","نعم، لنذهب!"
    ```

- **Multi-Person Conversations** (separated by a blank line in the CSV):
  - Columns: `movie_title`, `timestamp`, `speaker_id`, `dialogue`, `conversation_id`
  - Description: Captures dialogues involving more than two speakers, where multiple subtitle lines are part of the same conversation (within 5-second gaps). The `conversation_id` groups lines belonging to the same exchange.
  - Example:
    ```
    movie_title,timestamp,speaker_id,dialogue,conversation_id
    "Al Hayba (S5E1)","00:05:12,345 --> 00:05:14,678","Speaker_1","من سيذهب إلى السوق؟","550e8400-e29b-41d4-a716-446655440000"
    "Al Hayba (S5E1)","00:05:15,012 --> 00:05:17,234","Speaker_2","أنا سأذهب.","550e8400-e29b-41d4-a716-446655440000"
    "Al Hayba (S5E1)","00:05:18,567 --> 00:05:20,890","Speaker_1","خذ المال معك.","550e8400-e29b-41d4-a716-446655440000"
    ```

#### Column Explanations
- `movie_title`: The title of the movie or drama (e.g., "Where Do We Go Now?").
- `timestamp`: The time range of the subtitle line (e.g., "00:01:23,456 --> 00:01:25,789").
- `input` (Two-Person only): The first speaker’s dialogue in a two-person conversation.
- `output` (Two-Person only): The second speaker’s response in a two-person conversation.
- `speaker_id` (Multi-Person only): Identifies the speaker (e.g., "Speaker_1", "Speaker_2"). Assigned based on dialogue order.
- `dialogue` (Multi-Person only): The subtitle text spoken by the identified speaker.
- `conversation_id` (Multi-Person only): A unique UUID to group lines belonging to the same multi-person conversation.

### 2. `all_movies_no_response.csv`

This file contains subtitle lines that do not have a conversational response within the 5-second gap, indicating standalone lines or monologue-like text.

#### Structure
- Columns: `movie_title`, `timestamp`, `dialogue`
- Example:
  ```
  movie_title,timestamp,dialogue
  "Capernaum","00:10:34,123 --> 00:10:36,456","أعيش في هذا العالم وحيدًا."
  ```

#### Column Explanations
- `movie_title`: The title of the movie or drama (e.g., "Capernaum").
- `timestamp`: The time range of the subtitle line (e.g., "00:10:34,123 --> 00:10:36,456").
- `dialogue`: The subtitle text that did not have a response within 5 seconds.

## Key Features

- **Encoding Detection**: Uses `charset-normalizer` to detect the encoding of SRT files, defaulting to `windows-1256` for Arabic text if detection fails.
- **Text Cleaning**: Removes HTML tags, extra whitespace, unwanted characters (e.g., "PDF", "RLE"), and "Translated By" lines from subtitles.
- **Conversation Detection**: Identifies conversations by checking if subtitle lines are within a 5-second gap of each other.
- **User-Friendly Output**: Provides colored console output using `colorama`, with progress indicators, completion messages, and a final summary.
- **Error Handling**: Includes checks for missing SRT files and encoding issues, with suggestions for resolution.

## Troubleshooting

- **SRT File Not Found**:
  - Ensure all SRT files are in the `Data` folder with the exact filenames specified in the `movies` list.
  - Check the file path in the script (`Data/<filename>.srt`).

---
*Last Updated: May 09, 2025*