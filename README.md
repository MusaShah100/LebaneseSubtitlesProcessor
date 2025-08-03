<img width="1417" height="479" alt="{0E439FE7-D05B-438E-AC63-1579D36F65A6}" src="https://github.com/user-attachments/assets/6057a4c9-3de2-44b4-9ee3-caa87116d3b5" /># 🇱🇧 Lebanese Subtitles Processor

## 📌 Overview

The **Lebanese Subtitles Processor** is a Python tool designed to extract and analyze conversational dialogues from Lebanese movies and drama subtitles. It processes `.srt` files containing Arabic text, identifies conversations based on timing, and organizes the data into structured CSV files for further analysis.

---

## ✨ Features

- **Subtitle Processing** — Extracts dialogues from SRT files with automatic encoding detection  
- **Conversation Detection** — Identifies two-person and multi-person conversations based on timing  
- **Text Cleaning** — Removes HTML tags, extra whitespace, and unwanted characters  
- **User-Friendly Output** — Provides colored console output for better tracking of the processing workflow  
- **Error Handling** — Includes checks for missing files and encoding issues with resolution suggestions  

---

## 📁 Project Structure

```
Lebanese-Subtitles-Processor/
├── Data/                            # Directory containing SRT subtitle files
├── process_subtitles.py            # Main script for processing subtitles
├── documentation.md                # Detailed documentation
├── requirements.txt                # Project dependencies
├── all_movies_conversations.csv    # Output: extracted conversations (auto-generated)
└── all_movies_no_response.csv      # Output: non-responded subtitle lines (auto-generated)
```

---

## 🎬 Movies/Shows Processed

The script processes Arabic-subtitled SRT files from the following Lebanese productions:

1. *Where Do We Go Now?* (2011)  
2. *Al Hayba* (S5E1) (2021)  
3. *West Beirut* (1998)  
4. *Capernaum* (2018)  
5. *The Kite* (2003)  
6. *Zozo* (2005)  
7. *Perfect Strangers* (2022)  
8. *Very Big Shot* (2015)  
9. *Stray Bullet* (2010)  
10. *The Salt of This Sea* (2008)  

---

## ⚙️ Requirements

- Python >= 3.6  
- `pysrt>=1.1.2`  
- `charset-normalizer>=3.3.2`  
- `colorama>=0.4.6`  

---

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/lebanese-subtitles-processor.git
   cd lebanese-subtitles-processor
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # OR
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. Place all `.srt` files in the `Data/` folder.

2. Run the script:
   ```bash
   python process_subtitles.py
   ```

3. After processing, check the generated output:

   - `all_movies_conversations.csv`: Contains structured dialogue exchanges.
   - `all_movies_no_response.csv`: Contains subtitle lines without a response.

---

## 📊 Output Files

### 📁 all_movies_conversations.csv

Includes:

- **Two-Person Conversations**  
  | movie_title | timestamp | input | output |

- **Multi-Person Conversations**  
  | movie_title | timestamp | speaker_id | dialogue | conversation_id |

---

### 📁 all_movies_no_response.csv

Contains standalone lines with no conversational reply.  
| movie_title | timestamp | dialogue |

---

## 🛠 Troubleshooting

- **SRT File Not Found**  
  Ensure all `.srt` files are located in the `Data/` directory and match the filenames expected by the script.

- **Encoding Issues**  
  The script uses automatic encoding detection. If detection fails, it defaults to `windows-1256` (commonly used for Arabic).

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

If you use this project, **you must provide attribution** by stating:
> "This project is based on code created by Moosa Ali – [https://github.com/MusaShah100/LebaneseSubtitlesProcessor]".

---

## 👤 Author

**Syed Moosa Ali**
