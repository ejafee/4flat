"""Data loading and transformation utilities for structured and unstructured datasets."""

import random
import pandas as pd

class DataHandler:
    def __init__(self):
        # 1. EXTRACT: Memuat dataset ke dalam Pandas DataFrame (Pastikan file CSV ada di direktori)
        # Gunakan try-except agar aplikasi tidak crash jika CSV belum diunduh
        try:
            self.df_tiktok = pd.read_csv('tiktok_dataset.csv')
            self.df_sales = pd.read_csv('fashion_retail_sales.csv')
            self.df_reviews = pd.read_csv('womens_ecommerce_clothing_reviews.csv')
            self.data_loaded = True
        except FileNotFoundError:
            self.data_loaded = False
            print("Peringatan: File CSV tidak ditemukan. Menggunakan fallback data.")

    def get_structured_data(self, user_id):
        """
        TRANSFORM: Memproses Data Terstruktur (Keuangan & Inventaris)
        """
        # Skenario studi kasus: Data statis untuk baseline keuangan (bisa dari API Bank/ERP)
        bank_balance = 500
        rent_due = 3000
        days_until_rent = 4
        
        # Dinamis: Mengekstrak data sisa inventaris dari df_sales
        if self.data_loaded and 'Item_Name' in self.df_sales.columns:
            # Mencari sisa stok (contoh logika agregasi jika ada kolom 'Stock')
            # Catatan: Sesuaikan nama kolom ('Item_Name', 'Stock') dengan dataset Kaggle asli
            green_hijab_stock = len(self.df_sales[self.df_sales['Item_Name'].str.contains('Hijab', case=False, na=False)])
            blue_skirt_stock = len(self.df_sales[self.df_sales['Item_Name'].str.contains('Skirt', case=False, na=False)])
        else:
            # Fallback ke studi kasus jika dataset tidak sesuai format
            green_hijab_stock = 100
            blue_skirt_stock = 50

        return {
            "bank_balance": bank_balance,
            "rent_due": rent_due,
            "days_until_rent": days_until_rent,
            "inventory": {
                "green_hijabs": green_hijab_stock,
                "blue_skirts": blue_skirt_stock
            }
        }

    def get_unstructured_data(self, user_id):
        """
        TRANSFORM: Memproses Data Tidak Terstruktur (Tren & Sentimen)
        Untuk disuntikkan ke prompt Z.AI agar reasoning memiliki konteks dunia nyata.
        """
        urgent_messages = ["Landlord (WhatsApp): Bayar sewa dalam 4 hari atau butik ini saya segel!"]
        social_trends = []
        customer_reviews = []

        if self.data_loaded:
            # --- TIKTOK DATASET PROCESSING ---
            # Mengambil baris dengan views/engagement tertinggi untuk mencari tren
            # Sesuaikan kolom 'Hashtags' atau 'Description' dengan CSV asli
            if 'Hashtags' in self.df_tiktok.columns:
                top_tiktok = self.df_tiktok.sort_values(by='Views', ascending=False).head(5)
                trends = top_tiktok['Hashtags'].dropna().tolist()
                social_trends.append(f"Trending hashtags based on top TikTok views: {', '.join(trends)}")
            else:
                social_trends.append("TikTok data shows high engagement in 'Earth Tone' and 'Modest Wear'.")

            # --- E-COMMERCE REVIEWS PROCESSING ---
            # Mengambil review spesifik yang menyebutkan produk yang nyangkut di inventory (dead-stock)
            # Sesuaikan kolom 'Review Text' dengan CSV asli
            if 'Review Text' in self.df_reviews.columns:
                hijab_reviews = self.df_reviews[self.df_reviews['Review Text'].str.contains('hijab|green', case=False, na=False)]
                skirt_reviews = self.df_reviews[self.df_reviews['Review Text'].str.contains('skirt|blue', case=False, na=False)]
                
                # Mengambil 1-2 sampel acak sebagai konteks masalah produk
                if not hijab_reviews.empty:
                    customer_reviews.append(f"Customer feedback on similar hijabs: '{hijab_reviews.iloc[0]['Review Text']}'")
                if not skirt_reviews.empty:
                    customer_reviews.append(f"Customer feedback on similar skirts: '{skirt_reviews.iloc[0]['Review Text']}'")
        else:
            social_trends.append("Data TikTok menunjukkan outfit 'Earth Tone' sedang viral minggu ini.")
            customer_reviews.append("Review E-commerce: Hijab hijau agak susah dipadukan, tapi rok biru sangat nyaman.")

        return {
            "urgent_messages": urgent_messages,
            "social_trends": social_trends,
            "customer_reviews": customer_reviews
        }