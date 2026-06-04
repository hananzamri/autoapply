import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

config = rx.Config(
    app_name="autoapply_ai",
    plugins=[
        rx.plugins.RadixThemesPlugin(),  
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)