import reflex as rx

config = rx.Config(
    app_name="autoapply_ai",
    plugins=[
        rx.plugins.RadixThemesPlugin(),  
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)