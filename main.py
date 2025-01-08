import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import json
from datetime import datetime
from ttkthemes import ThemedTk
import os
import webbrowser
from threading import Thread
from queue import Queue
import csv
import queue 

class ModernNewsSummarizer:
    def __init__(self):
        self.window = ThemedTk(theme="arc")
        self.window.title("News Analyzer Pro")
        self.window.geometry("1200x800")
        self.window.configure(bg="#2C3E50")
        
        # Create main scrollable canvas
        self.main_canvas = tk.Canvas(self.window, bg="#2C3E50")
        self.scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack main scrollable elements
        self.scrollbar.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        
        # Initialize variables
        self.history = []
        self.data_folder = "saved_data"
        self.ensure_data_folders()
        self.queue = Queue()
        
        self.create_styles()
        self.create_gui()
        self.load_history()
        
        # Bind mousewheel scrolling
        self.window.bind("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def ensure_data_folders(self):
        """Create necessary folders for data storage"""
        folders = [self.data_folder, 
                  os.path.join(self.data_folder, "articles"),
                  os.path.join(self.data_folder, "exports")]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)
    
    def create_styles(self):
        style = ttk.Style()
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 28, "bold"), 
                       background="#2C3E50", 
                       foreground="white")
        
        style.configure("Header.TLabel", 
                       font=("Segoe UI", 14, "bold"), 
                       background="#2C3E50", 
                       foreground="white")
        
        style.configure("Modern.TButton",
                       font=("Segoe UI", 12),
                       padding=10)
    
    def create_gui(self):
        # Title and Description
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill="x", pady=20)
        
        title_label = ttk.Label(title_frame, 
                               text="News Analyzer Pro", 
                               style="Title.TLabel")
        title_label.pack(pady=5)
        
        description = ttk.Label(title_frame,
                              text="Advanced news analysis and summarization tool",
                              font=("Segoe UI", 12),
                              foreground="white",
                              background="#2C3E50")
        description.pack()
        
        # URL Entry Frame
        input_frame = ttk.Frame(self.scrollable_frame)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        url_label = ttk.Label(input_frame, 
                             text="Enter News URL:", 
                             style="Header.TLabel")
        url_label.pack(side="left", padx=5)
        
        self.url_entry = ttk.Entry(input_frame, width=80, font=("Segoe UI", 12))
        self.url_entry.pack(side="left", padx=10)
        
        # Buttons Frame
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side="left", padx=5)
        
        self.create_button_set(button_frame)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.scrollable_frame, 
                                      orient="horizontal", 
                                      length=300, 
                                      mode="determinate")
        self.progress.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.create_all_tabs()
        
    def create_button_set(self, parent):
        buttons = [
            ("Summarize", self.summarize_article),
            ("Save", self.save_article),
            ("Export CSV", self.export_to_csv),
            ("Clear", self.clear_all),
            ("Help", self.show_help)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(parent, 
                           text=text, 
                           style="Modern.TButton",
                           command=command)
            btn.pack(side="left", padx=5)
    
    def create_all_tabs(self):
        # Summary Tab
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Summary")
        self.create_summary_tab(summary_frame)
        
        # Analysis Tab
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="Analysis")
        self.create_analysis_tab(analysis_frame)
        
        # History Tab
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="History")
        self.create_history_tab(history_frame)
        
        # Statistics Tab
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="Statistics")
        self.create_statistics_tab(stats_frame)

    def create_summary_tab(self, parent):
        self.create_text_widget(parent, "Title", "title_text", height=2)
        self.create_text_widget(parent, "Author", "author_text", height=1)
        self.create_text_widget(parent, "Published Date", "date_text", height=1)
        self.create_text_widget(parent, "Summary", "summary_text", height=10)
        self.create_text_widget(parent, "Sentiment Analysis", "sentiment_text", height=3)

    def create_analysis_tab(self, parent):
        self.create_text_widget(parent, "Key Points", "keypoints_text", height=8)
        self.create_text_widget(parent, "Named Entities", "entities_text", height=5)
        self.create_text_widget(parent, "Topic Analysis", "topics_text", height=5)

    def create_history_tab(self, parent):
        self.history_list = tk.Listbox(parent,
                                     font=("Segoe UI", 12),
                                     bg="#ECF0F1",
                                     fg="#2C3E50",
                                     selectmode="single")
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_list.bind('<<ListboxSelect>>', self.load_from_history)

    def create_statistics_tab(self, parent):
        self.create_text_widget(parent, "Reading Statistics", "reading_stats_text", height=5)
        self.create_text_widget(parent, "Content Statistics", "content_stats_text", height=5)
        self.create_text_widget(parent, "Language Statistics", "language_stats_text", height=5)

    def create_text_widget(self, parent, label_text, attr_name, height):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=10, pady=5)
        
        label = ttk.Label(frame, text=label_text, style="Header.TLabel")
        label.pack(anchor="w")
        
        text_widget = scrolledtext.ScrolledText(
            frame,
            height=height,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            bg="#ECF0F1",
            fg="#2C3E50"
        )
        text_widget.pack(fill="both", expand=True, pady=(0, 10))
        
        setattr(self, attr_name, text_widget)

    def extract_author_date(self, soup):
        # Try to find author
        author = None
        author_elements = soup.find_all(['a', 'span', 'div'], 
                                      class_=re.compile(r'author|byline', re.I))
        for element in author_elements:
            if element.text.strip():
                author = element.text.strip()
                break
        
        # Try to find date
        date = None
        date_elements = soup.find_all(['time', 'span', 'div'], 
                                    class_=re.compile(r'date|time|published', re.I))
        for element in date_elements:
            if element.text.strip():
                date = element.text.strip()
                break
        
        return author or "Unknown", date or "Unknown"

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.3:
            sentiment = "Very Positive"
        elif polarity > 0:
            sentiment = "Slightly Positive"
        elif polarity < -0.3:
            sentiment = "Very Negative"
        elif polarity < 0:
            sentiment = "Slightly Negative"
        else:
            sentiment = "Neutral"
        
        return (f"Overall Sentiment: {sentiment}\n"
                f"Polarity Score: {polarity:.2f} (-1 to 1)\n"
                f"Subjectivity Score: {subjectivity:.2f} (0 to 1)")

    def extract_key_points(self, text):
        # Extract sentences with important indicators
        sentences = text.split('.')
        indicators = ['most important', 'significant', 'crucial', 'key', 'major', 
                     'essential', 'fundamental', 'primary']
        
        scored_sentences = []
        for sentence in sentences:
            score = 0
            for indicator in indicators:
                if indicator in sentence.lower():
                    score += 1
            if score > 0:
                scored_sentences.append((score, sentence.strip()))
        
        scored_sentences.sort(reverse=True)
        key_points = [s[1] for s in scored_sentences[:5]]
        
        return "• " + "\n• ".join(key_points) if key_points else "No key points identified."

    def generate_statistics(self, text):
        words = text.split()
        sentences = text.split('.')
        paragraphs = text.split('\n\n')
        
        # Basic stats
        stats = {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_words_per_sentence': len(words) / max(len(sentences), 1),
            'avg_sentences_per_paragraph': len(sentences) / max(len(paragraphs), 1),
            'reading_time': len(words) / 200  # Average reading speed of 200 wpm
        }
        
        return stats

    def summarize_article(self):
        try:
            url = self.url_entry.get()
            if not url:
                messagebox.showerror("Error", "Please enter a URL")
                return
            
            # Show loading state
            self.progress['value'] = 0
            self.window.config(cursor="wait")
            self.window.update()
            
            # Start processing in a thread
            thread = Thread(target=self._process_article, args=(url,))
            thread.start()
            
            # Check queue periodically
            self.window.after(100, self._check_processing_queue)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process article: {str(e)}")
            self.window.config(cursor="")

    def _process_article(self, url):
        try:
            # Fetch and parse webpage
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            self.queue.put(('progress', 20))
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract content
            title = soup.find('h1').text if soup.find('h1') else soup.title.string
            author, date = self.extract_author_date(soup)
            
            self.queue.put(('progress', 40))
            
            # Clean and extract main content
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()
            
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text() for p in paragraphs)
            content = re.sub(r'\s+', ' ', content).strip()
            
            self.queue.put(('progress', 60))
            
            # Analyze content
            summary = self.get_important_sentences(content)
            sentiment = self.analyze_sentiment(content)
            key_points = self.extract_key_points(content)
            stats = self.generate_statistics(content)
            
            self.queue.put(('progress', 80))
            
            # Save results
            result = {
                'title': title,
                'author': author,
                'date': date,
                'summary': summary,
                'sentiment': sentiment,
                'key_points': key_points,
                'stats': stats,
                'url': url
            }
            
            self.queue.put(('result', result))
            self.queue.put(('progress', 100))
            
        except Exception as e:
            self.queue.put(('error', str(e)))


    def _check_processing_queue(self):
        try:
            while True:
                msg_type, data = self.queue.get_nowait()
                
                if msg_type == 'progress':
                    self.progress['value'] = data
                elif msg_type == 'result':
                    self._update_gui_with_results(data)
                elif msg_type == 'error':
                    messagebox.showerror("Error", f"Failed to process article: {data}")
                    self.window.config(cursor="")
                    return
                
        except queue.Empty:
            if self.progress['value'] != 100:
                self.window.after(100, self._check_processing_queue)
            else:
                self.window.config(cursor="")

    def _update_gui_with_results(self, data):
        # Clear existing content
        self.clear_all()
        
        # Update Summary tab
        self.title_text.insert("1.0", data['title'])
        self.author_text.insert("1.0", data['author'])
        self.date_text.insert("1.0", data['date'])
        self.summary_text.insert("1.0", data['summary'])
        self.sentiment_text.insert("1.0", data['sentiment'])
        
        # Update Analysis tab
        self.keypoints_text.insert("1.0", data['key_points'])
        
        # Update Statistics tab
        stats = data['stats']
        reading_stats = (f"Word Count: {stats['word_count']}\n"
                        f"Estimated Reading Time: {stats['reading_time']:.1f} minutes")
        
        content_stats = (f"Sentence Count: {stats['sentence_count']}\n"
                        f"Paragraph Count: {stats['paragraph_count']}\n"
                        f"Average Words per Sentence: {stats['avg_words_per_sentence']:.1f}")
        
        self.reading_stats_text.insert("1.0", reading_stats)
        self.content_stats_text.insert("1.0", content_stats)
        
        # Add to history
        self.add_to_history(data)

    def get_important_sentences(self, text, num_sentences=5):
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        scored_sentences = []
        for sentence in sentences:
            # Base score is word count (longer sentences often more important)
            score = len(sentence.split()) * 0.1
            
            # Boost score for sentences with numbers
            if re.search(r'\d+', sentence):
                score += 2
                
            # Boost score for sentences with quotes
            if '"' in sentence or '"' in sentence:
                score += 2
                
            # Boost score for sentences with important keywords
            keywords = ['important', 'significant', 'crucial', 'findings', 'results', 
                       'concluded', 'research', 'study', 'analysis', 'report']
            for keyword in keywords:
                if keyword in sentence.lower():
                    score += 1.5
            
            scored_sentences.append((score, sentence))
        
        scored_sentences.sort(reverse=True)
        return "\n\n".join(s[1] for s in scored_sentences[:num_sentences])

    def clear_all(self):
        """Clear all text widgets"""
        text_widgets = [
            'title_text', 'author_text', 'date_text', 'summary_text',
            'sentiment_text', 'keypoints_text', 'entities_text', 'topics_text',
            'reading_stats_text', 'content_stats_text', 'language_stats_text'
        ]
        
        for widget_name in text_widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                widget.delete("1.0", tk.END)
        
        self.progress['value'] = 0

    def add_to_history(self, data):
        """Add analyzed article to history"""
        self.history.append(data)
        self.history_list.insert(tk.END, data['title'])
        
        # Save to file
        history_file = os.path.join(self.data_folder, "articles", 
                                  f"article_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_history(self):
        """Load history from saved files"""
        history_dir = os.path.join(self.data_folder, "articles")
        if not os.path.exists(history_dir):
            return
            
        for filename in os.listdir(history_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(history_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.history.append(data)
                        self.history_list.insert(tk.END, data['title'])
                except Exception as e:
                    print(f"Error loading history file {filename}: {str(e)}")

    def load_from_history(self, event):
        """Load article from history when selected"""
        selection = self.history_list.curselection()
        if selection:
            index = selection[0]
            data = self.history[index]
            self._update_gui_with_results(data)
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, data['url'])

    def export_to_csv(self):
        """Export analyzed articles to CSV"""
        try:
            filepath = os.path.join(self.data_folder, "exports", 
                                  f"news_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Title', 'URL', 'Author', 'Date', 'Summary', 
                               'Sentiment', 'Key Points', 'Word Count', 'Reading Time'])
                
                for article in self.history:
                    writer.writerow([
                        article['title'],
                        article['url'],
                        article['author'],
                        article['date'],
                        article['summary'][:500],  # First 500 chars of summary
                        article['sentiment'].split('\n')[0],  # Overall sentiment only
                        article['key_points'][:500],  # First 500 chars of key points
                        article['stats']['word_count'],
                        f"{article['stats']['reading_time']:.1f} min"
                    ])
            
            messagebox.showinfo("Success", 
                              f"Data exported to {filepath}\nOpening folder location...")
            webbrowser.open(os.path.dirname(filepath))
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

    def save_article(self):
        """Save current article explicitly"""
        try:
            title = self.title_text.get("1.0", tk.END).strip()
            if not title:
                messagebox.showerror("Error", "No article to save")
                return
            
            data = {
                'url': self.url_entry.get(),
                'title': title,
                'author': self.author_text.get("1.0", tk.END).strip(),
                'date': self.date_text.get("1.0", tk.END).strip(),
                'summary': self.summary_text.get("1.0", tk.END).strip(),
                'sentiment': self.sentiment_text.get("1.0", tk.END).strip(),
                'key_points': self.keypoints_text.get("1.0", tk.END).strip(),
                'stats': {
                    'word_count': len(self.summary_text.get("1.0", tk.END).split()),
                    'reading_time': len(self.summary_text.get("1.0", tk.END).split()) / 200
                }
            }
            
            self.add_to_history(data)
            messagebox.showinfo("Success", "Article saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save article: {str(e)}")

    def show_help(self):
        """Show help documentation"""
        help_text = """
        News Analyzer Pro - Help Guide
        
        1. Basic Usage:
           - Paste a news article URL in the input field
           - Click "Summarize" to analyze the article
           - View results in different tabs
        
        2. Features:
           - Article summarization
           - Sentiment analysis
           - Key points extraction
           - Reading statistics
           - Export to CSV
           - Article history
        
        3. Tips:
           - Save important articles for later reference
           - Use the history tab to access previous analyses
           - Export data for further analysis in spreadsheets
        
        4. Troubleshooting:
           - Ensure you have an active internet connection
           - Use complete URLs including 'http://' or 'https://'
           - Some websites may block automated access
           
        5. About:
           - This tool uses natural language processing to analyze news articles
           - Sentiment analysis is performed using TextBlob
           - Summaries are generated using an extractive method
        """
        
        help_window = tk.Toplevel(self.window)
        help_window.title("Help - News Analyzer Pro")
        help_window.geometry("600x700")
        
        text_widget = scrolledtext.ScrolledText(
            help_window,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

    def run(self):
        """Start the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ModernNewsSummarizer()
    app.run()
