"""
File: data_cleaning.py
Author: Student Name
Index Number: AI_20240001
Course: CS4241 - Introduction to Artificial Intelligence
Purpose: Data cleaning for Ghana Election CSV and Budget PDF
"""

import pandas as pd
import re
import PyPDF2
from typing import Tuple, Dict, Any

class GhanaDataCleaner:
    """Clean and preprocess Ghana election and budget data"""
    
    def __init__(self):
        self.cleaning_log = []
    
    def clean_election_data(self, csv_path: str) -> pd.DataFrame:
        """
        Clean Ghana Election Results CSV
        """
        print("🟡 Cleaning Ghana election data...")
        
        # Load data
        df = pd.read_csv(csv_path)
        self.cleaning_log.append(f"Loaded {len(df)} rows from election CSV")
        
        # Remove duplicate rows
        initial_rows = len(df)
        df = df.drop_duplicates()
        self.cleaning_log.append(f"Removed {initial_rows - len(df)} duplicate rows")
        
        # Standardize column names (lowercase, underscores)
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        
        # Fill missing values
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna("unknown")
            else:
                df[col] = df[col].fillna(0)
        
        # Remove special characters from text columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
        
        # Standardize Ghana region names
        region_mapping = {
            'greater accra': 'Greater Accra',
            'ashanti': 'Ashanti',
            'western': 'Western',
            'eastern': 'Eastern',
            'central': 'Central',
            'volta': 'Volta',
            'northern': 'Northern',
            'upper east': 'Upper East',
            'upper west': 'Upper West',
            'bono': 'Bono',
            'ahafo': 'Ahafo',
            'savannah': 'Savannah',
            'north east': 'North East',
            'oti': 'Oti',
            'western north': 'Western North'
        }
        
        if 'region' in df.columns:
            df['region'] = df['region'].str.lower().map(region_mapping).fillna(df['region'])
        
        # Standardize party names
        party_mapping = {
            'npp': 'NPP',
            'ndc': 'NDC',
            'independent': 'Independent',
            'cpp': 'CPP',
            'pnc': 'PNC',
            'gcp': 'GCP',
            'apc': 'APC'
        }
        
        party_cols = [col for col in df.columns if 'party' in col or 'winner' in col]
        for col in party_cols:
            if col in df.columns:
                df[col] = df[col].str.lower().map(party_mapping).fillna(df[col])
        
        self.cleaning_log.append(f"Cleaning complete. Final shape: {df.shape}")
        
        return df
    
    def extract_pdf_text(self, pdf_path: str) -> str:
        """
        Extract text from Ghana Budget Statement PDF
        """
        print("🟡 Extracting text from Ghana Budget PDF...")
        
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            self.cleaning_log.append(f"PDF has {num_pages} pages")
            
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += page_text + "\n"
                
                if (i + 1) % 50 == 0:
                    print(f"  Extracted page {i+1}/{num_pages}")
        
        # Clean extracted text
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove excessive newlines
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        
        self.cleaning_log.append(f"Extracted {len(text)} characters from PDF")
        
        return text
    
    def save_cleaned_data(self, df: pd.DataFrame, text: str):
        """Save cleaned data to processed folder"""
        df.to_csv("data/processed/cleaned_election_data.csv", index=False)
        
        with open("data/processed/extracted_budget_text.txt", "w", encoding='utf-8') as f:
            f.write(text)
        
        # Save cleaning log
        with open("data/processed/cleaning_log.txt", "w") as f:
            for log in self.cleaning_log:
                f.write(log + "\n")
        
        print("✅ Cleaned data saved to data/processed/")
    
    def get_cleaning_summary(self) -> Dict[str, Any]:
        """Return summary of cleaning operations"""
        return {
            "total_operations": len(self.cleaning_log),
            "logs": self.cleaning_log
        }


if __name__ == "__main__":
    cleaner = GhanaDataCleaner()
    
    # Clean election data
    election_df = cleaner.clean_election_data("data\\raw\\Ghana_Election_Result.csv")
    
    # Extract PDF text - USE YOUR EXACT FILENAME
    budget_text = cleaner.extract_pdf_text("data\\raw\\2025-Budget-Statement-and-Economic-Policy_v4.pdf")
    
    # Save cleaned data
    cleaner.save_cleaned_data(election_df, budget_text)
    
    # Print summary
    print("\n📊 Cleaning Summary:")
    for log in cleaner.cleaning_log:
        print(f"  • {log}")