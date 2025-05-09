import pysrt
import csv
import os
import re
from uuid import uuid4
from charset_normalizer import detect
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init(autoreset=True)

# Movie details (SRT files in Data folder)
movies = [
    {"title": "Where Do We Go Now?", "srt_file": "Data/where_do_we_go_now.srt"},
    {"title": "Al Hayba (S5E1)", "srt_file": "Data/Al Hayba S05E01.ar.srt"},
    {"title": "West Beirut", "srt_file": "Data/West.Beirut.WEBRip.Netflix.ar.srt"},
    {"title": "Capernaum", "srt_file": "Data/Capernaum (2018).srt"},
    {"title": "The Kite", "srt_file": "Data/the_kite.srt"},
    {"title": "Zozo", "srt_file": "Data/zozo_arabic_only.srt"},
    {"title": "Perfect Strangers", "srt_file": "Data/Perfect Strangers 2022.srt"},
    {"title": "Very Big Shot", "srt_file": "Data/Very.Big.Shot.2015.srt"},
    {"title": "Stray Bullet", "srt_file": "Data/Stray.Bullet.2010.srt"},
    {"title": "The Salt of This Sea", "srt_file": "Data/The Salt of This Sea (2008).srt"}
]


def sanitize_filename(filename):
    """Remove invalid characters from filename for Windows compatibility."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename


def detect_encoding(file_path):
    """Detect the encoding of a file using charset-normalizer."""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        if encoding and confidence > 0.5:
            print(f"{Fore.BLUE}Detected encoding for {file_path}: {encoding}{Style.RESET_ALL}")
            return encoding
        print(
            f"{Fore.YELLOW}Could not detect encoding for {file_path}. Defaulting to 'windows-1256' (common for Arabic).{Style.RESET_ALL}")
        return 'windows-1256'  # Default to windows-1256 for Arabic subtitles


def clean_text(text):
    """Remove formatting tags and extra whitespace from subtitle text."""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags like <i>, <b>
    text = re.sub(r'\n+', ' ', text)  # Replace newlines with space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'RLE|PDF|[^A-Za-z0-9\u0600-\u06FF\s]', '', text)  # Remove unwanted characters
    text = re.sub(r'(?i)translated by.*', '', text)  # Remove "Translated By" lines
    text = text.strip()
    return text


def is_conversational_response(sub1, sub2, max_gap_seconds=5):
    """Determine if sub2 is a response to sub1 based on timing."""
    if not sub2:
        return False
    end_time = sub1.end.to_time()
    start_time = sub2.start.to_time()
    gap = (start_time.hour * 3600 + start_time.minute * 60 + start_time.second +
           start_time.microsecond / 1000000) - \
          (end_time.hour * 3600 + end_time.minute * 60 + end_time.second +
           end_time.microsecond / 1000000)
    return 0 <= gap <= max_gap_seconds


def process_subtitles(movie, two_person_convos, multi_person_convos, no_response_lines):
    """Process subtitles for a movie and append data to shared lists."""
    title = movie["title"]
    srt_file = movie["srt_file"]

    # Check if SRT file exists
    if not os.path.exists(srt_file):
        print(
            f"{Fore.RED}Error: SRT file '{srt_file}' not found. Please ensure it is in the Data folder.{Style.RESET_ALL}")
        return

    # Detect file encoding
    detected_encoding = detect_encoding(srt_file)
    if not detected_encoding:
        print(
            f"{Fore.YELLOW}Could not detect encoding for {srt_file}. Trying 'windows-1256' (common for Arabic).{Style.RESET_ALL}")
        detected_encoding = 'windows-1256'

    # Load SRT file with detected encoding
    try:
        subs = pysrt.open(srt_file, encoding=detected_encoding)
    except Exception as e:
        print(f"{Fore.RED}Error reading SRT file for {title}: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Possible causes: Incorrect encoding or malformed SRT file.{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Try opening the SRT file in a text editor (e.g., Notepad++) to verify its encoding.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Common Arabic encodings to try: 'windows-1256', 'iso-8859-6', 'utf-8'.{Style.RESET_ALL}")
        return

    # Initialize conversation tracking
    conversation_id = str(uuid4())  # Unique ID for each conversation group
    current_convo = []
    last_sub = None

    for i, sub in enumerate(subs):
        text = clean_text(sub.text)
        if not text:
            continue

        timestamp = f"{sub.start} --> {sub.end}"

        # Check if this subtitle is part of a conversation
        next_sub = subs[i + 1] if i + 1 < len(subs) else None

        if last_sub and is_conversational_response(last_sub, sub):
            current_convo.append({
                "timestamp": timestamp,
                "dialogue": text,
                "speaker_id": f"Speaker_{(len(current_convo) % 2) + 1}"
            })
        else:
            # End of a conversation or no conversation
            if current_convo:
                # Process the completed conversation
                if len(current_convo) == 2:
                    two_person_convos.append({
                        "movie_title": title,
                        "timestamp": current_convo[0]["timestamp"],
                        "input": current_convo[0]["dialogue"],
                        "output": current_convo[1]["dialogue"]
                    })
                elif len(current_convo) > 2:
                    for j, convo_line in enumerate(current_convo):
                        multi_person_convos.append({
                            "movie_title": title,
                            "timestamp": convo_line["timestamp"],
                            "speaker_id": convo_line["speaker_id"],
                            "dialogue": convo_line["dialogue"],
                            "conversation_id": conversation_id
                        })
                conversation_id = str(uuid4())  # New conversation ID
                current_convo = []

            # If no response follows, store as no-response line
            if not next_sub or not is_conversational_response(sub, next_sub):
                no_response_lines.append({
                    "movie_title": title,
                    "timestamp": timestamp,
                    "dialogue": text
                })
            else:
                current_convo.append({
                    "timestamp": timestamp,
                    "dialogue": text,
                    "speaker_id": "Speaker_1"
                })

        last_sub = sub

    # Handle any remaining conversation
    if current_convo:
        if len(current_convo) == 2:
            two_person_convos.append({
                "movie_title": title,
                "timestamp": current_convo[0]["timestamp"],
                "input": current_convo[0]["dialogue"],
                "output": current_convo[1]["dialogue"]
            })
        elif len(current_convo) > 2:
            for j, convo_line in enumerate(current_convo):
                multi_person_convos.append({
                    "movie_title": title,
                    "timestamp": convo_line["timestamp"],
                    "speaker_id": convo_line["speaker_id"],
                    "dialogue": convo_line["dialogue"],
                    "conversation_id": conversation_id
                })
        elif len(current_convo) == 1:
            no_response_lines.append({
                "movie_title": title,
                "timestamp": current_convo[0]["timestamp"],
                "dialogue": current_convo[0]["dialogue"]
            })


def main():
    """Process subtitles for all movies and save to shared CSV files with enhanced output."""
    # Shared lists for all movies' data
    two_person_convos = []
    multi_person_convos = []
    no_response_lines = []

    total_movies = len(movies)
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Starting Subtitle Processing for {total_movies} Movies/Shows{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")

    # Process each movie
    for idx, movie in enumerate(movies, 1):
        print(f"{Fore.BLUE}[{idx}/{total_movies}] Processing '{movie['title']}'...{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'---' * 20}{Style.RESET_ALL}")

        process_subtitles(movie, two_person_convos, multi_person_convos, no_response_lines)

        print(f"\n{Fore.GREEN}✓ Movie '{movie['title']}' done!{Style.RESET_ALL}")
        if idx < total_movies:
            print(f"{Fore.YELLOW}Processing next movie...{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'---' * 20}{Style.RESET_ALL}\n")

    # Write all conversations to a single CSV
    if two_person_convos or multi_person_convos:
        convo_file = "all_movies_conversations.csv"
        with open(convo_file, 'w', newline='', encoding='utf-8') as f:
            if two_person_convos:
                writer = csv.DictWriter(f, fieldnames=["movie_title", "timestamp", "input", "output"])
                writer.writeheader()
                writer.writerows(two_person_convos)
            if multi_person_convos:
                if two_person_convos:
                    f.write("\n")  # Separator between two-person and multi-person
                writer = csv.DictWriter(f, fieldnames=["movie_title", "timestamp", "speaker_id", "dialogue",
                                                       "conversation_id"])
                writer.writeheader()
                writer.writerows(multi_person_convos)
        print(
            f"{Fore.GREEN}All conversations saved to '{convo_file}' (Two-person: {len(two_person_convos)}, Multi-person: {len(multi_person_convos)}){Style.RESET_ALL}")

    # Write all non-responded lines to a single CSV
    if no_response_lines:
        no_response_file = "all_movies_no_response.csv"
        with open(no_response_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["movie_title", "timestamp", "dialogue"])
            writer.writeheader()
            writer.writerows(no_response_lines)
        print(
            f"{Fore.GREEN}All non-responded lines saved to '{no_response_file}' (Total: {len(no_response_lines)}){Style.RESET_ALL}")

    # Final summary
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Processing Complete!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Movies/Shows Processed: {total_movies}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Two-Person Conversations: {len(two_person_convos)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Multi-Person Conversation Lines: {len(multi_person_convos)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Total Non-Responded Lines: {len(no_response_lines)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()